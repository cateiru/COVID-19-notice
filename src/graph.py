'''
Copyright 2020 YutoWatanabe
'''
import datetime
from typing import Dict, List

import numpy as np
from matplotlib import pyplot


def make_graph(statistics: List[Dict[str, int]], image_save_path: str, title: str) -> None:
    '''
    国内の日別感染者数をグラフにして保存する

    Args:
        statistics (List[Dict[str, int]]): 感染者のデータ
        image_save_path (str): 出力する画像を保存するパス
    '''
    y_value = []

    for element in statistics:
        y_value.append(element['positive'])

    date_first = datetime.datetime.strptime(str(statistics[0]['date']), r'%Y%m%d')
    date_end = datetime.datetime.strptime(str(statistics[-1]['date']), r'%Y%m%d')

    text = f'({date_first.month}/{date_first.day}~{date_end.month}/{date_end.day})'

    width = 6.4
    height = 4.8

    x_loc = np.array(range(len(y_value)))

    pyplot.figure(figsize=(width, height))
    pyplot.title(title + text)
    pyplot.xlabel('date')
    pyplot.ylabel('people')
    pyplot.bar(x_loc, y_value, color='#fa6843')
    pyplot.xticks(color="None")
    pyplot.tick_params(length=0)

    pyplot.savefig(image_save_path)
