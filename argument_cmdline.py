from scrapy import cmdline
import hello
import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow
# app = QApplication(sys.argv)
# MainWindow = QMainWindow()
# ui = hello.Ui_Form()
# ui.setupUi(MainWindow)
# MainWindow.show()
#sys.exit(app.exec_())

filePath = r'c:\Users\YDS\Desktop\urls.xlsx'
cmdline.execute(("scrapy crawl argumentsSpider -a flag=file -a data="+filePath).split())