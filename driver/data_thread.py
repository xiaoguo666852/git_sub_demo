import ast
import random
import threading
import time
from queue import Queue

import numpy

from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition


class DataThread(QThread):
    dataEmit = pyqtSignal(list)

    def __init__(self, lock:threading.Lock):
        super().__init__()
        self.is_paused = False
        self.lock = lock
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.join_count = 0
        pass

    def run(self):
        for i in range(1000):
            # 数据格式：[{'x_data':[], 'y_data':[], 'die_id':i, 'subdie_id':j}, {}]
            for j in range(400):
                data_list = []
                for k in range(40):
                    data_dict = {'x_data': None, 'y_data': None}
                    x_data = numpy.linspace(i, 500 + i, 10)
                    y_data = x_data ** 2
                    data_dict['x_data'] = list(x_data)
                    data_dict['y_data'] = list(y_data)
                    data_dict['die_id'] = i
                    data_dict['subdie_id'] = j
                    data_list.append(data_dict)

                    if self.is_paused:
                        self.mutex.lock()
                        self.condition.wait(self.mutex)
                        self.mutex.unlock()
                while self.join_count >= 10:
                    time.sleep(0)
                    pass
                self.dataEmit.emit(data_list)
                self.join_count += 1

        pass
