import datetime
import os
import time
from typing import Dict, List

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
    while(True):
        schedule.run_pending()
        time.sleep(1)


def connect(line_token: str, save_dir: str):
    '''
    APIに接続し前回取得した情報と比較し日時が変更されている場合LINE notifyにpostする

    Args:
        line_token (str): LINE notifyのアクセストークン
    '''
    body = get_requests('https://covid19-japan-web-api.now.sh/api/v1/total')
    day = body['date']

    save_file_path = os.path.join(save_dir, 'save.json')
    daily_infections = os.path.join(save_dir, 'daily.json')
    graph_image_path = os.path.join(save_dir, 'igraph.png')

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

感染者: {body['positive']}人 (前日比: {difference:+})
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


def make_graph(daily: List[Dict[str, int]], image_save_path: str) -> None:
    '''
    国内の日別感染者数をグラフにして保存する

    Args:
        daily (List[Dict[str, int]]): 日別感染者数のデータ
        image_save_path (str): 出力する画像を保存するパス
    '''
    x = []
    y = []

    for element in daily:
        day = datetime.datetime.strptime(str(element['day']), r'%Y%m%d')
        x.append(f'{day.month}/{day.day}')
        y.append(element['infected'])

    x_loc = np.array(range(len(y)))

    pyplot.title('Daily infections')
    pyplot.xlabel('date')
    pyplot.ylabel('people')
    pyplot.bar(x_loc, y, color='#fa6843')
    pyplot.xticks(x_loc, x)

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


def post_line(line_token: str, text: str, image_save_path: str):
    '''
    LINE notifyにpostする

    Args:
        line_token (str): LINE notifyのアクセストークン
        text (str): postする内容
        image_save_path (str): 画像のパス
    '''
    line_access_url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + line_token}
    payload = {'message': text}
    files = {'imageFile': open(image_save_path, 'rb')}
    requests.post(line_access_url, headers=headers, params=payload, files=files)


if __name__ == "__main__":
    main()
