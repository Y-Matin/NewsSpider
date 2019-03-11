from scrapy import cmdline

import spider
from MainGUI import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

# app = QApplication(sys.argv)
# MainWindow = QMainWindow()
# # ui = spider.Ui_Form()
# ui = MainGUI.Ui_MainText()
# ui.setupUi(MainWindow)
# MainWindow.show()
# sys.exit(app.exec_())


class MainScreen(QMainWindow,Ui_MainText):
    def __init__(self,parent= None):
        super(MainScreen, self).__init__(parent)
        self.setupUi(self)
        # 默认显示 ‘单次爬取’，将toolButton 不显示在界面，界面上
        self.toolButton.setFixedSize(0,0)
        # 关联触发事件：signals && slots // 信号&&槽
        self.more.triggered.connect(self.clickOnMore)
        self.once.triggered.connect(self.clickOnOnce)
        self.reset.clicked.connect(self.clickOnReset)
        self.extract.clicked.connect(self.clickOnExtract)

    def clickOnMore(self):
        '''
        在点击菜单栏中 '爬取方式'->'批量爬取' 后触发。
        :return:none
        '''
        print('检测到点击more事件')
        self.once.setEnabled(True)
        self.more.setEnabled(False)
        word = '导入文件:'
        self.label.setText(word)
        # 恢复toolButton 控件的大小
        self.toolButton.setMinimumSize(QtCore.QSize(50, 10))
        self.toolButton.setMaximumSize(16777215,16777215)

    def clickOnOnce(self):
        '''
        在点击菜单栏中 '爬取方式'->'单次爬取' 后触发。
        :return:
        '''
        print('检测到点击once事件')
        self.once.setEnabled(False)
        self.more.setEnabled(True)
        word = '网站地址:'
        self.label.setText(word)
        # 将 toolButton 控件长宽都设为 0 ，目的 不让其显示在界面上
        self.toolButton.setFixedSize(0, 0)

    def clickOnReset(self):
        print('检测到点击reset事件')
        self.lineEdit.setText('')

    def clickOnExtract(self):
        print('检测到点击extract事件')
        status = self.once.isEnabled()
        # status 如果为true,代表当前是批量爬取方式,可以点击 '单次爬取'切换爬取方式
        if status:
            print('当前的爬取方式是 批量爬取')
        else:
            print('当前的爬取方式是 单次爬取')
            url = self.lineEdit.text()
            cmd = "scrapy crawl argumentsSpider -a flag=url -a data="
            cmdline.execute(( cmd + url).split())

def main():
    app = QApplication(sys.argv)
    ui = MainScreen()
    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


