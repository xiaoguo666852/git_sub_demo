import csv
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from driver.data_thread import DataThread


class HandleDataThread(Thread):
    def __init__(self, canvas_forty_list:list, figure_forty_list, axes_forty_list):
        super().__init__()
        # self.is_paused = False
        # self.canvas_forty_list = canvas_forty_list
        # self.figure_forty_list = figure_forty_list
        # self.axes_forty_list = axes_forty_list
        # self.executor = ThreadPoolExecutor(max_workers=5)
        # self.data_thread = DataThread()
        # self.thread_event = threading.Event()
        # self.lock_list = []
        # for i in range(len(self.canvas_forty_list)):
        #     row_lock = []
        #     for j in range(len(self.canvas_forty_list[i])):
        #         row_lock.append(threading.Lock())
        #     self.lock_list.append(row_lock)
        # self.signal_slot_bind()
        pass

    def signal_slot_bind(self):
        self.data_thread.dataEmit.connect(self.data_receive)

    def stop(self):
        self.thread_event.clear()
        self.thread_event.wait()

    def run(self):
        self.data_thread.start()
        time.sleep(5)

        while True:
            print(self.thread_event.is_set())
            self.data_thread.is_paused = True



    def data_receive(self, data_list):
        self.executor.submit(self.handle_data, data_list)
        pass

    def handle_data(self, data_list):
        path = r"C:\Users\21276\Desktop\data_output\\"
        self.test_save_text(path, data_list)
        self.test_save_img(path, data_list)
        pass

    def test_save_text(self, dir_name, data_list):
        dir_path = dir_name + f'{data_list[0]["die_id"]}_{data_list[0]["subdie_id"]}\\'
        if os.path.exists(dir_path):
            pass
        else:
            os.makedirs(dir_path)
        with open(dir_path + f'{data_list[0]["die_id"]}_{data_list[0]["subdie_id"]}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for data in data_list:
                for row in zip(data['x_data'], data['y_data']):
                    writer.writerow(row)
        pass

    # 40canvas的保存图片
    def test_save_img(self, dir_name, data_list):
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
