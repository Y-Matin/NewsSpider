from scrapy import cmdline
import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow
# app = QApplication(sys.argv)
# MainWindow = QMainWindow()
# ui = hello.Ui_Form()
# ui.setupUi(MainWindow)
# MainWindow.show()
#sys.exit(app.exec_())

cmdline.execute("scrapy crawl getText".split())