import spider
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow



app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = spider.Ui_Form()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())