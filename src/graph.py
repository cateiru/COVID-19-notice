'''
Copyright 2020 YutoWatanabe
'''
import datetime
from typing import Dict, List

import numpy as np
from matplotlib import pyplot


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
