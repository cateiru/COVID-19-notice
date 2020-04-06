'''
Copyright 2020 YutoWatanabe
'''
import datetime
import os
import time

import click
import schedule

from communication import get_requests, post_line
from graph import make_graph
from json_operation import json_read, json_write


@click.command()
@click.option('--line-token', 'line_token', prompt=True, hide_input=True, help='line access token.')
def main(line_token: str):
    '''
    - 現在の感染者数: 1時間ごとに動作させる
    - 日別統計: 毎日00:00に動作させる

    Args:
        line_token (str): LINE notifyのアクセストークン
    '''
    directory = os.path.dirname(__file__)
    save_dir = os.path.join(directory, 'saves')
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    today_total(line_token, save_dir)
    now_total(line_token, save_dir)

    # 実行するタイミングを変えたい場合はここを編集
    schedule.every().day.at('00:00').do(today_total, line_token=line_token, save_dir=save_dir)
    schedule.every(1).hours.do(now_total, line_token=line_token, save_dir=save_dir)
    # ここまで

    while(True):  # pylint: disable=C0325
        schedule.run_pending()
        time.sleep(1)


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
{day_obj.month}月{day_obj.day}日

☣感染者: {body['positive']}人
(前日比: {difference:+})
  - 退院: {body['discharge']}人
  - 入院中: {body['hospitalize']}人
    * 軽中度・無症状: {body['mild']}人
    * 人工呼吸・ICU: {body['severe']}人
    * 確認中: {body['confirming']}人
    * 待機中: {body['waiting']}人
  - 死亡: {body['death']}人

source by: https://covid-2019.live/ '''

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

    save_file_path = os.path.join(save_dir, 'day_before.json')

    if os.path.isfile(save_file_path):
        old_patient = json_read(save_file_path)
        is_ratio = True
    else:
        old_patient = {'patient': 0, 'before': 0, 'date': None}
        is_ratio = False

    total_patient = 0
    for body_metadata in body:
        total_patient += int(body_metadata['cases'])

    if total_patient != old_patient['before']:
        if is_ratio:
            difference = total_patient - old_patient['patient']
        else:
            difference = 0

        text = f'\n現在の感染者数: {total_patient}人\n(前日比: {difference:+})'
        post_line(line_token, text, None)

        date = datetime.datetime.now().strftime(r'%d')

        if old_patient['date'] != date:
            save_body_reset = {'patient': old_patient['before'], 'before': total_patient, 'date': date}
        else:
            save_body_reset = {'patient': old_patient['patient'], 'before': total_patient, 'date': date}

        json_write(save_body_reset, save_file_path)


if __name__ == "__main__":
    main()  # pylint: disable=E1120
