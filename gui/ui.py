import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QToolBar, QWidget, QVBoxLayout, QStatusBar, QLabel, QProgressBar, QGroupBox, \
    QHBoxLayout, QTableView, QAbstractItemView, QHeaderView, QFormLayout, QPushButton, QLineEdit, QTabWidget, \
    QButtonGroup, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        with open('./static/qss/text.qss', 'r') as file:
            self.setStyleSheet(file.read())
        self.setup_ui()
        pass

    # 初始化时的控件显示
    def setup_ui(self):
        # 工具栏
        self.tool_bar()

        # MainWindow的中心控件
        self.wd_central_widget = QWidget()
        self.setCentralWidget(self.wd_central_widget)
        self.vl_central_widget = QVBoxLayout(self.wd_central_widget)


        # # hl，数据显示部分
        self.hl_show_data = QHBoxLayout()

        # 文本数据
        self.sim_show_data_model = QStandardItemModel()
        self.tv_show_data_text = QTableView()
        self.tv_show_data_text.setModel(self.sim_show_data_model)
        self.tv_show_data_text.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tv_show_data_text.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hl_show_data.addWidget(self.tv_show_data_text)

        # self.forty_canvas()
        self.one_canvas()


        self.vl_central_widget.addLayout(self.hl_show_data, 1)

        pass

    def tool_bar(self):
        self.tb_whole = QToolBar()

        with open('./static/qss/tool_bar.qss', 'r') as file:
            self.tb_whole.setStyleSheet(file.read())

        self.addToolBar(self.tb_whole)
        start_icon = QIcon('./static/imgs/start.png')
        self.at_start = self.tb_whole.addAction(start_icon, '')
        self.at_start.setToolTip('Start')

        self.at_pause = self.tb_whole.addAction(QIcon('./static/imgs/pause.png'), '')
        self.at_pause.setToolTip('Pause')

        self.at_continue = self.tb_whole.addAction(QIcon('./static/imgs/continue.png'), '')
        self.at_continue.setToolTip('Continue')

        pass

    def insert_row_show_data(self, model: QStandardItemModel, row_data: iter):
        row_items = []
        for col in row_data:
            temp = QStandardItem(str(col))
            temp.setTextAlignment(Qt.AlignCenter)
            row_items.append(temp)
        model.insertRow(model.rowCount(), row_items)
        pass

    def set_header_show_data(self, model: QStandardItemModel, header: iter):
        model.setHorizontalHeaderLabels(header)
        pass

    def forty_canvas(self):
        self.canvas_forty_list = []
        self.figure_forty_list = []
        self.axes_forty_list = []

        for i in range(8):
            row_figure = []
            row_axes = []
            for j in range(5):
                figure = Figure((1, 1))
                axes = figure.add_subplot(111)
                row_figure.append(figure)
                row_axes.append(axes)
            self.axes_forty_list.append(row_axes)
            self.figure_forty_list.append(row_figure)

        for i in range(8):
            row_canvas = []
            for j in range(5):
                row_canvas.append(FigureCanvas(self.figure_forty_list[i][j]))
            self.canvas_forty_list.append(row_canvas)

        self.lock_list = []
        for i in range(len(self.canvas_forty_list)):
            row_lock = []
            for j in range(len(self.canvas_forty_list[i])):
                row_lock.append(threading.Lock())
            self.lock_list.append(row_lock)

        # 四十个canvas
        self.gl_canvas = QGridLayout()
        for i in range(8):
            for j in range(5):
                self.gl_canvas.addWidget(self.canvas_forty_list[i][j], i, j)

        self.hl_show_data.addLayout(self.gl_canvas)
        pass

    def one_canvas(self):
        self.lock = threading.Lock()
        self.figure_data = Figure((5, 3))
        self.canvas = FigureCanvas(self.figure_data)
        self.axes_list = self.figure_data.subplots(8, 5)
        self.hl_show_data.addWidget(self.canvas, 1)

