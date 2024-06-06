import csv
import os
import random
import threading
import time
from configparser import ConfigParser

from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog

from gui.ui import UI
from driver.data_thread import DataThread
from concurrent.futures import ThreadPoolExecutor


class Driver(UI):
    def __init__(self):
        super().__init__()
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.data_thread = DataThread(lock=self.lock)
        self.singal_bind_slot()
        self.a = None
        pass

    # 统一信号绑定槽函数
    def singal_bind_slot(self):
        # 工具栏的信号绑定
        self.at_start.triggered.connect(self.tool_start)
        self.at_pause.triggered.connect(self.tool_pause)
        self.data_thread.dataEmit.connect(self.data_receive)
        self.data_thread.started.connect(self.thread_start)
        self.data_thread.finished.connect(self.thread_finished)
        pass

    def closeEvent(self, event):
        super().closeEvent(event)
        res = QMessageBox.question(self, '提示', '确定退出吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if res == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        pass

    def tool_start(self):
        self.data_thread.start()
        self.a = time.time()
        pass

    def tool_pause(self):
        # self.data_thread.is_paused = True
        print(self.data_thread.join_count)
        pass

    def thread_start(self):

        pass

    def thread_finished(self):
        pass

    def data_receive(self, data_list):
        # path = r"C:\Users\21276\Desktop\data_output\\"
        # self.one_save_img(path, data_list, self.figure_data)
        # self.forty_save_img(path, data_list)
        self.executor.submit(self.handle_data, data_list)
        pass

    def handle_data(self, data_list):

        path = r"C:\Users\21276\Desktop\data_output\\"
        # self.one_save_img(path, data_list, self.figure_data)
        # self.forty_save_img(path, data_list)
        self.test_save_text(path, data_list)
        pass

    def test_save_text(self, dir_name, data_list):
        with open(dir_name + f'{data_list[0]["die_id"]}_{data_list[0]["subdie_id"]}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for data in data_list:
                for row in zip(data['x_data'], data['y_data']):
                    writer.writerow(row)
        self.data_thread.join_count -= 1
        pass

    # 40canvas的保存图片
    def forty_save_img(self, dir_name, data_list):
        dir_path = dir_name + f'{data_list[0]["die_id"]}_{data_list[0]["subdie_id"]}'
        if os.path.exists(dir_path):
            pass
        else:
            os.makedirs(dir_path)

        for num, data in enumerate(data_list):
            i = 0
            j = num
            while j >= 5:
                i += 1
                j -= 5
            self.lock_list[i][j].acquire()
            self.axes_forty_list[i][j].plot(data['x_data'], data['y_data'])
            self.axes_forty_list[i][j].set_title(f'{data["die_id"]}_{data["subdie_id"]}')
            self.canvas_forty_list[i][j].draw()
            path = dir_path + f'\\{i}_{j}.png'
            self.figure_forty_list[i][j].savefig(path)
            self.lock_list[i][j].release()
        pass

    # 非40canvas的保存图片
    def one_save_img(self, dir_name, data_list, figure=None):
        self.lock.acquire()
        for num, data in enumerate(data_list):
            i = 0
            j = num
            while j >= 5:
                i += 1
                j -= 5
            self.axes_list[i][j].plot(data['x_data'], data['y_data'])
            self.axes_list[i][j].set_title(f'{data["die_id"]}_{data["subdie_id"]}')
        self.canvas.draw()
        path = dir_name + f'\\{data_list[0]["die_id"]}_{data_list[0]["subdie_id"]}.png'
        figure.savefig(path)
        self.lock.release()
        self.data_thread.join_count -= 1
        pass
