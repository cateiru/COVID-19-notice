import datetime
import json
import os
import time
from typing import Dict

import click
import requests
import schedule


@click.command()
@click.option('--line-token', 'line_token', prompt=True, hide_input=True, help='line access token.')
def main(line_token: str):
    '''
    1時間ごとに動作させる

    Args:
        line_token (str): LINE notifyのアクセストークン
    '''
    connect(line_token)

    schedule.every(1).hours.do(connect, line_token=line_token)
    while(True):
        schedule.run_pending()
        time.sleep(1)


def connect(line_token: str):
    '''
    APIに接続し前回取得した情報と比較し日時が変更されている場合LINE notifyにpostする

    Args:
        line_token (str): LINE notifyのアクセストークン
    '''
    body = get_requests('https://covid19-japan-web-api.now.sh/api/v1/total')
    day = body['date']

    directory = os.path.dirname(__file__)
    save_dir = os.path.join(directory, 'saves')
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    save_file_path = os.path.join(save_dir, 'save.json')

    if os.path.isfile(save_file_path):
        old_body = json_read(save_file_path)
        old_day = old_body['date']
        difference = body['positive'] - old_body['positive']
    else:
        old_day = None
        difference = 0

    if day != old_day:
        day_obj = datetime.datetime.strptime(str(day), r'%Y%m%d')
        text = f'''
{day_obj.month}月{day_obj.day}日 更新

感染者: {body['positive']}人 (前日比: {difference})
  - 退院: {body['discharge']}人
  - 入院中: {body['hospitalize']}人
    * 軽中度・無症状: {body['mild']}人
    * 人工呼吸・ICU: {body['severe']}人
    * 確認中: {body['confirming']}人
    * 待機中: {body['waiting']}人
    * 症状有無確認中: {body['symtomConfirming']}人
  - 死亡: {body['death']}人

  source by: https://covid-2019.live/'''
        status = post_line(line_token, text)
        print(text)
        print('-' * 30)
        print(status)
        print('\n\n')
        json_write(body, save_file_path)


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


def post_line(line_token: str, text: str) -> str:
    '''
    LINE notifyにpostする

    Args:
        line_token (str): LINE notifyのアクセストークン
        text (str): postする内容
    '''
    line_access_url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + line_token}
    payload = {'message': text}
    status = requests.post(line_access_url, headers=headers, params=payload,)
    return status


def json_write(body: str, save_file_path: str) -> None:
    '''
    Jsonファイルに保存する

    Args:
        body (str): Jsonの内容
        save_dir (str): 保存するファイルパス
    '''
    with open(save_file_path, mode='w') as contents:
        json.dump(body, contents, indent=4, ensure_ascii=False)


def json_read(save_file_path: str) -> Dict[str, int]:
    '''
    Jsonファイルを読み込む

    Args:
        save_file_path (str): 保存するファイルパス

    Returns:
        Dict[str, int]: Jsonの内容
    '''
    with open(save_file_path, mode='r') as contents:
        body = json.load(contents)

    return body


if __name__ == "__main__":
    main()
