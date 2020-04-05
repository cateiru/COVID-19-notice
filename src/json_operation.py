import json
from typing import Dict


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
