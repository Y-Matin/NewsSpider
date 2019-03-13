from scrapy import cmdline

import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from MainGUI import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


# app = QApplication(sys.argv)
# MainWindow = QMainWindow()
# # ui = spider.Ui_Form()
# ui = MainGUI.Ui_MainText()
# ui.setupUi(MainWindow)
# MainWindow.show()
# sys.exit(app.exec_())
from NewsSpider.endHandle.handler import parseLocalFile


class MainScreen(QMainWindow,Ui_MainText):
    successCount = 0
    failedCount = 0
    # inputType  代表导入方式：三种状态，单次，批量，本地// once,more,local
    inputTpye= 'once'
    def __init__(self,parent= None):
        super(MainScreen, self).__init__(parent)
        self.setupUi(self)
        # 默认显示 ‘单次爬取’，将toolButton 不显示在界面，界面上
        self.toolButton.setFixedSize(0,0)
        # 关联触发事件：signals && slots // 信号&&槽
        self.more.triggered.connect(self.clickOnMore)
        self.once.triggered.connect(self.clickOnOnce)
        self.local.triggered.connect(self.clickOnLocal)
        self.reset.clicked.connect(self.clickOnReset)
        self.extract.clicked.connect(self.clickOnExtract)
        self.toolButton.clicked.connect(self.clickOnChooseFile)

    def clickOnMore(self):
        '''
        在点击菜单栏中 '爬取方式'->'批量爬取' 后触发。
        :return:none
        '''
        print('检测到点击more事件')
        self.inputTpye='more'
        self.once.setEnabled(True)
        self.more.setEnabled(False)
        self.local.setEnabled(True)
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
        self.inputTpye='once'
        self.once.setEnabled(False)
        self.more.setEnabled(True)
        word = '网站地址:'
        self.label.setText(word)
        # 将 toolButton 控件长宽都设为 0 ，目的 不让其显示在界面上
        self.toolButton.setFixedSize(0, 0)

    def clickOnLocal(self):
        print('检测到点击local事件')
        self.once.setEnabled(True)
        self.more.setEnabled(True)
        self.local.setEnabled(False)
        if self.inputTpye.__eq__('once'):
            word = '导入文件:'
            self.label.setText(word)
            # 恢复toolButton 控件的大小
            self.toolButton.setMinimumSize(QtCore.QSize(50, 10))
            self.toolButton.setMaximumSize(16777215, 16777215)
        self.inputTpye = 'local'
        pass

    def clickOnReset(self):
        print('检测到点击reset事件')
        self.lineEdit.setText('')

    def clickOnExtract(self):
        print('检测到点击extract事件')
        if self.inputTpye.__eq__('more'):
            print('当前的爬取方式是 批量爬取')
            filePath = self.lineEdit.text()
            try:
                cmd = "scrapy crawl argumentsSpider -a flag=file -a data="
                # cmdline.execute((cmd + filePath).split())
                os.system(cmd+filePath)
                self.successCount = self.successCount + 1
            except BaseException as e:
                self.failedCount = self.failedCount+1
            self.statusbar.showMessage('结果(成功：'+str(self.successCount)+', 失败：'+str(self.failedCount)+')', 0)

        elif self.inputTpye.__eq__('once'):
            print('当前的爬取方式是 单次爬取')
            url = self.lineEdit.text()
            cmd = "scrapy crawl argumentsSpider -a flag=url -a data="
            # cmdline.execute((cmd + url).split())
            try:
                os.system(cmd + url)
                self.successCount = self.successCount + 1
            except BaseException as e:
                self.failedCount = self.failedCount+1
            self.statusbar.showMessage('结果(成功：'+str(self.successCount)+', 失败：'+str(self.failedCount)+')', 0)
        elif self.inputTpye.__eq__('local'):
            print('当前的爬取方式是 本地导入')
            filePath = self.lineEdit.text()
            parseLocalFile(filePath)
        else:
            pass


    def clickOnChooseFile(self):
        fileType = ''
        if self.inputTpye.__eq__('more'):
            fileType ="excle files (*.xlsx)"
        elif self.inputTpye.__eq__('local'):
            fileType = "html files (*.html)"
        absolute_path = QFileDialog.getOpenFileName(self, 'Open file','/', fileType)
        filePath = absolute_path[0];
        self.lineEdit.setText(filePath)
        pass


def main():
    app = QApplication(sys.argv)
    ui = MainScreen()
    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


