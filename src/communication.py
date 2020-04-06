'''
Copyright 2020 YutoWatanabe
'''
from typing import Optional, Any

import requests


def get_requests(link: str) -> Any:
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
