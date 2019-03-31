import shlex
import threading
import traceback

from PyQt5.QtCore import *
from MainGUI import *
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget
import NewsSpider.settings
import NewsSpider.spiders

import scrapy.spiderloader
import scrapy.statscollectors
import scrapy.logformatter
import scrapy.dupefilters
import scrapy.squeues
import scrapy.extensions.spiderstate
import scrapy.extensions.corestats
import scrapy.extensions.telnet
import scrapy.extensions.logstats
import scrapy.extensions.memusage
import scrapy.extensions.memdebug
import scrapy.extensions.feedexport
import scrapy.extensions.closespider
import scrapy.extensions.debug
import scrapy.extensions.httpcache
import scrapy.extensions.statsmailer
import scrapy.extensions.throttle
import scrapy.core.scheduler
import scrapy.core.engine
import scrapy.core.scraper
import scrapy.core.spidermw
import scrapy.core.downloader
import scrapy.downloadermiddlewares.stats
import scrapy.downloadermiddlewares.httpcache
import scrapy.downloadermiddlewares.cookies
import scrapy.downloadermiddlewares.useragent
import scrapy.downloadermiddlewares.httpproxy
import scrapy.downloadermiddlewares.ajaxcrawl
import scrapy.downloadermiddlewares.decompression
import scrapy.downloadermiddlewares.defaultheaders
import scrapy.downloadermiddlewares.downloadtimeout
import scrapy.downloadermiddlewares.httpauth
import scrapy.downloadermiddlewares.httpcompression
import scrapy.downloadermiddlewares.redirect
import scrapy.downloadermiddlewares.retry
import scrapy.downloadermiddlewares.robotstxt
import scrapy.spidermiddlewares.depth
import scrapy.spidermiddlewares.httperror
import scrapy.spidermiddlewares.offsite
import scrapy.spidermiddlewares.referer
import scrapy.spidermiddlewares.urllength
import scrapy.pipelines
import scrapy.core.downloader.handlers.http
import scrapy.core.downloader.contextfactory

from NewsSpider.endHandle.handler import parseLocalFile
from setting import Ui_settings


class MainScreen(QMainWindow,Ui_MainText):
    successCount = 0
    failedCount = 0
    log = None

    # inputType  代表导入方式：三种状态，单次，批量，本地// once,more,local
    inputTpye= 'once'
    def __init__(self,parent= None):
        super(MainScreen, self).__init__(parent)
        self.setupUi(self)
        #  声明一个 backend 用他里面的update_date来关联界面类的函数，配合emit函数，用于显示日志
        self.log = Backend()
        self.log.update_date.connect(self.showLog)
        self.log.setText('一切准备就绪!!')
        self.log.show()
        # 声明一个 设置界面
        self.settingsGUI = settingsScreen()

        # 默认显示 ‘单次爬取’，将toolButton 不显示在界面，界面上
        self.toolButton.setFixedSize(0,0)
        # 设置textbrowser显示的最大行数
        # self.textBrowser.
        # 关联菜单触发事件：signals && slots // 信号&&槽
        self.more.triggered.connect(self.clickOnMore)
        self.once.triggered.connect(self.clickOnOnce)
        self.local.triggered.connect(self.clickOnLocal)
        self.database.triggered.connect(lambda:self.showSettingsByIndex(0))
        self.filePath.triggered.connect(lambda:self.showSettingsByIndex(0))
        self.update.triggered.connect(lambda:self.showSettingsByIndex(0))
        self.help.triggered.connect(lambda:self.showSettingsByIndex(2))
        self.feedBack.triggered.connect(lambda:self.showSettingsByIndex(1))
        self.about.triggered.connect(lambda:self.showSettingsByIndex(3))
        # 关联按钮事件
        self.reset.clicked.connect(self.clickOnReset)
        self.extract.clicked.connect(self.clickOnExtract)
        self.toolButton.clicked.connect(self.clickOnChooseFile)

    def showSettingsByIndex(self,index):
        self.settingsGUI.tabWidget.setCurrentIndex(index)
        # setWindowModality要写show函数之前，不然没用
        self.settingsGUI.setWindowModality(Qt.ApplicationModal)
        self.settingsGUI.show()

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
        # 清空输入栏
        self.clickOnReset()

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
        # 清空输入栏
        self.clickOnReset()

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
        # 清空输入栏
        self.clickOnReset()

    def clickOnReset(self):
        print('检测到点击reset事件')
        self.lineEdit.setText('')

    def clickOnExtract(self):
        print('检测到点击extract事件')
        # try:
        # process = CrawlerProcess(get_project_settings())   #程序意外出错。
        # except BaseException as e:
        #     self.textBrowser.append(e)
        self.textBrowser.setText('')
        # 实现实时刷新界面，一般用于耗时的程序或者会对界面修改的程序
        QApplication.processEvents()
        if self.inputTpye.__eq__('more'):
            print('当前的爬取方式是 批量爬取')
            filePath = self.lineEdit.text()
            try:
                cmd = "scrapy crawl argumentsSpider -a flag=file -a data="
                # cmdline 调用scrapy，只能在改目录下运行，不能剪切到其他环境下运行
                # cmdline.execute((cmd + filePath).split())
                # os方式调用，日志不能让日志显示在界面上
                # os.system(cmd+filePath)
                # process.crawl('argumentsSpider',flag='file',data=filePath )
                # process.start()
                # 现在采用 子进程的方式运行爬虫，获取进程标准输出，实现实时日志
                shell_cmd = cmd + filePath
                cmd = shlex.split(shell_cmd)
                import subprocess
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                while p.poll() is None:
                    line = p.stdout.readline().decode('utf-8', 'ignore')
                    line = line.strip()
                    if line:
                        print('output: [{}]'.format(line))
                        self.log.setText('{}'.format(line))
                        self.log.show()
                        # 实现实时刷新界面，一般用于耗时的程序或者会对界面修改的程序
                        QApplication.processEvents()
                if p.returncode == 0:
                    print('Subprogram success')
                    QMessageBox.information(self,'提示','批量爬取成功！')
                else:
                    print('Subprogram failed')
                    QMessageBox.critical(self, '提示', '批量爬取失败！')
                    self.failedCount = self.failedCount + 1
                self.successCount = self.successCount + 1
            except BaseException as e:
                self.log.show('程序发生异常：', traceback.print_exc())
            self.statusbar.showMessage('结果(成功：'+str(self.successCount)+', 失败：'+str(self.failedCount)+')', 0)
        elif self.inputTpye.__eq__('once'):
            print('当前的爬取方式是 单次爬取')
            url = self.lineEdit.text()
            cmd = "scrapy crawl argumentsSpider -a flag=url -a data="
            # cmdline.execute((cmd + url).split())
            try:
                # os.system(cmd + url)
                # process.crawl('argumentsSpider', flag='url', data=url)
                # process.start()

                shell_cmd = cmd + url
                cmd = shlex.split(shell_cmd)
                import subprocess
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while p.poll() is None:
                    line = p.stdout.readline().decode('utf-8', 'ignore')
                    line = line.strip()
                    if line:
                        print('output: [{}]'.format(line))
                        self.log.setText('{}'.format(line))
                        self.log.show()
                        # 实现实时刷新界面，一般用于耗时的程序或者会对界面修改的程序
                        QApplication.processEvents()
                if p.returncode == 0:
                    print('Subprogram success')
                    QMessageBox.information(self, '提示', '爬取成功！')
                    self.successCount = self.successCount + 1
                else:
                    print('Subprogram failed')
                    QMessageBox.critical(self, '提示', '爬取失败！')
                    self.failedCount = self.failedCount + 1
            except BaseException as e:
                self.log.show('程序发生异常：',traceback.print_exc())
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

    def showLog(self, text):
        self.textBrowser.append(text)


class settingsScreen(QWidget,Ui_settings):

    def __init__(self,parent= None):
        super(settingsScreen, self).__init__(parent)
        self.setupUi(self)
        # self.readConfig()

    def readConfig(self):
        settings = QSettings("data/config.ini", QSettings.IniFormat)
        # settings.setValue("pos", QVariant(self.pos()))
        # settings.setValue("size", QVariant(self.size()))


import  time
class Backend(QThread):
    update_date = pyqtSignal(str)
    text = 'init'
    last=''
    def show(self):
        # data = QDateTime.currentDateTime()
        self.update_date.emit((str(self.text)))
        self.text=''

    def setText(self,log):
        self.text = log



def main():
    app = QApplication(sys.argv)
    ui = MainScreen()
    # 采用 型号 和 槽的方式 , 将 日志 实时输出
    ui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


