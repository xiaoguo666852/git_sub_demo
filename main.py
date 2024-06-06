import sys
from PyQt5.QtWidgets import QApplication

from driver.driver import Driver

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Driver()
    window.showMaximized()
    sys.exit(app.exec_())
    pass