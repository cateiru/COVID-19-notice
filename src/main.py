'''
Copyright 2020 YutoWatanabe
'''
import datetime
import os
import time
from typing import Dict, List, Optional

import click
import numpy as np
import requests
import schedule
from matplotlib import pyplot

from json_operation import json_read, json_write


@click.command()
@click.option('--line-token', 'line_token', prompt=True, hide_input=True, help='line access token.')
def main(line_token: str):
    '''
    1時間ごとに動作させる

    Args:
        line_token (str): LINE notifyのアクセストークン
    '''
    directory = os.path.dirname(__file__)
    save_dir = os.path.join(directory, 'saves')
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    connect(line_token, save_dir)

    schedule.every(1).hours.do(connect, line_token=line_token)
    while(True):  # pylint: disable=C0325
        schedule.run_pending()
        time.sleep(1)


def connect(line_token: str, save_dir: str):
    '''
    複数のスプリントを実行させる。
    - Today total
    - Now total

    Args:
        line_token (str): LINEのアクセストークン
        save_dir (str): 一時データを保存するディレクトリパス
    '''
    today_total(line_token, save_dir)
    now_total(line_token, save_dir)


def today_total(line_token: str, save_dir: str):
    '''
    - 前回取得したデータと最新のデータを比較し日付が変わっている場合に
        - 前回取得したデータと最新の陽患者数の増加数の計算
        - その他様々なデータを取得
        - 増加数をグラフ描画し保存。メタデータをjsonで保存。
        - 増加数のグラフ描画とデータをLINEにpost

    Args:
        line_token (str): LINE notifyのアクセストークン
        save_dir (str): 一時データを保存するディレクトリパス
    '''
    body = get_requests('https://covid19-japan-web-api.now.sh/api/v1/total')
    day = body['date']

    save_file_path = os.path.join(save_dir, 'save.json')
    daily_infections = os.path.join(save_dir, 'daily.json')
    graph_image_path = os.path.join(save_dir, 'graph.png')

    if os.path.isfile(save_file_path):
        old_body = json_read(save_file_path)
        old_day = old_body['date']
        difference = body['positive'] - old_body['positive']
    else:
        old_day = None
        difference = 0

    if day != old_day:
        if os.path.isfile(daily_infections):
            daily = json_read(daily_infections)
        else:
            daily = []

        day_obj = datetime.datetime.strptime(str(day), r'%Y%m%d')
        daily.append({
            'day': day,
            'infected': difference
        })

        text = f'''
{day_obj.month}月{day_obj.day}日 更新

☣感染者: {body['positive']}人 (前日比: {difference:+})
  - 退院: {body['discharge']}人
  - 入院中: {body['hospitalize']}人
    * 軽中度・無症状: {body['mild']}人
    * 人工呼吸・ICU: {body['severe']}人
    * 確認中: {body['confirming']}人
    * 待機中: {body['waiting']}人
    * 症状有無確認中: {body['symtomConfirming']}人
  - 死亡: {body['death']}人

  source by: https://covid-2019.live/'''

        make_graph(daily, graph_image_path)
        post_line(line_token, text, graph_image_path)
        print(text)
        print('-' * 30)
        print('\n\n')

        json_write(daily, daily_infections)
        json_write(body, save_file_path)


def now_total(line_token: str, save_dir: str):
    '''
    感染者数の速報を通知する

    Args:
        line_token (str): LINEのアクセストークン
        save_dir (str): 一時データを保存するディレクトリパス
    '''
    body = get_requests('https://covid19-japan-web-api.now.sh/api/v1/prefectures')

    save_file_path = os.path.join(save_dir, 'now_total.json')
    save_statistics = os.path.join(save_dir, 'now_infected.json')

    if os.path.isfile(save_file_path):
        old_body = json_read(save_file_path)
        is_ratio = True
    else:
        old_body = {'patient': 0}
        is_ratio = False

    total_patient: int = 0
    for element in body:
        total_patient += int(element['cases'])

    if total_patient != old_body['patient']:
        if is_ratio:
            difference = total_patient - old_body['patient']
        else:
            difference = 0

        if os.path.isfile(save_statistics):
            now = json_read(save_statistics)
        else:
            now = []
        now.append({'day': datetime.datetime.now().strftime(r'%Y%m%d-%H'), 'infected': total_patient})

        text = f'\n⚠感染者数更新: {total_patient}人 ({difference:+})'
        post_line(line_token, text, None)
        save_body = {'patient': total_patient}

        json_write(save_body, save_file_path)
        json_write(now, save_statistics)


def make_graph(statistics: List[Dict[str, int]], image_save_path: str) -> None:
    '''
    国内の日別感染者数をグラフにして保存する

    Args:
        statistics (List[Dict[str, int]]): 感染者のデータ
        image_save_path (str): 出力する画像を保存するパス
    '''
    x_value = []
    y_value = []

    for element in statistics:
        day = datetime.datetime.strptime(str(element['day']), r'%Y%m%d')
        x_value.append(f'{day.month}/{day.day}')
        y_value.append(element['infected'])

    x_loc = np.array(range(len(y_value)))

    pyplot.title('Infected person graph')
    pyplot.xlabel('date')
    pyplot.ylabel('people')
    pyplot.bar(x_loc, y_value, color='#fa6843')
    pyplot.xticks(x_loc, x_value)

    pyplot.savefig(image_save_path)


def get_requests(link: str) -> Dict[str, int]:
    '''
    APIからデータを取得

    Args:
        link (str): リンク

    Returns:
        Dict[str, int]: 取得したデータ
    '''
    response = requests.get(link)
    return response.json()


def post_line(line_token: str, text: str, image_save_path: Optional[str]):
    '''
    LINE notifyにpostする

    Args:
        line_token (str): LINE notifyのアクセストークン
        text (str): postする内容
        image_save_path (Optional[str]): 画像のパス。Noneの場合はpostしない。
    '''
    line_access_url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + line_token}
    payload = {'message': text}
    if image_save_path is None:
        files = None
    else:
        files = {'imageFile': open(image_save_path, 'rb')}
    requests.post(line_access_url, headers=headers, params=payload, files=files)


if __name__ == "__main__":
    main()  # pylint: disable=E1120
