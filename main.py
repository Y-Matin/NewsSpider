import codecs
import configparser
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
from NewsSpider.endHandle.handler import sendEmail
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
    '''软件的主界面'''
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
        '''通过index参数决定显示配置界面的那个子页面'''
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
        '''点击菜单栏中 '爬取方式'->'本地导入' 后触发'''
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
        '''点击提取按钮后，触发'''
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
                # cmdline 调用scrapy，只能在该环境下运行
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
                    # 调试环境
                    line = p.stdout.readline().decode('utf-8',"ignore")
                    # 正式环境
                    # line = p.stdout.readline().decode('gb18030')
                    line = line.strip()
                    if line:
                        # print('output: [{}]'.format(line))
                        self.log.setText('{}'.format(line))
                        self.log.show()
                        # 实现实时刷新界面，一般用于耗时的程序或者会对界面修改的程序
                        QApplication.processEvents()
                if p.returncode == 0:
                    print('Subprogram success')
                    QMessageBox.information(self,'提示','批量爬取成功！')
                    self.successCount = self.successCount + 1
                else:
                    print('Subprogram failed')
                    QMessageBox.critical(self, '提示', '批量爬取失败！')
                    self.failedCount = self.failedCount + 1
            except BaseException as e:
                self.log.show('程序发生异常：\n', traceback.print_exc())
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
                    # 调试环境
                    line = p.stdout.readline().decode('utf-8', 'ignore')
                    # 正式环境
                    # line = p.stdout.readline().decode('gb18030')
                    line = line.strip()
                    if line:
                        print('output: [{}]'.format(line))
                        self.log.setText('{}'.format(line))
                        self.log.show()
                        # 实现实时刷新界面，一般用于耗时的程序或者会对界面修改的程序
                        QApplication.processEvents()
                if p.returncode == 0:
                    # print('Subprogram success')
                    QMessageBox.information(self, '提示', '爬取成功！')
                    self.successCount = self.successCount + 1
                else:
                    print('Subprogram failed')
                    QMessageBox.critical(self, '提示', '爬取失败！')
                    self.failedCount = self.failedCount + 1
            except BaseException as e:
                self.log.show('程序发生异常：\n',traceback.print_exc())
            self.statusbar.showMessage('结果(成功：'+str(self.successCount)+', 失败：'+str(self.failedCount)+')', 0)
        elif self.inputTpye.__eq__('local'):
            print('当前的爬取方式是 本地导入')
            try:

                filePath = self.lineEdit.text()
                fileList = filePath.split('|')

                self.log.setText('本地解析开始!!')
                self.log.show()
                # 实现实时刷新界面，一般用于耗时的程序或者会对界面修改的程序
                QApplication.processEvents()

                for path in fileList:
                    self.log.setText('正在解析"%s"' % path)
                    self.log.show()
                    # 实现实时刷新界面，一般用于耗时的程序或者会对界面修改的程序
                    QApplication.processEvents()
                    parseLocalFile(path)
                    self.log.setText("解析"+path + "完成！！")
                    self.log.show()
                self.log.setText("共" + str(len(fileList)) + "个文件,全部解析完成！！")
                self.log.show()
                # 实现实时刷新界面，一般用于耗时的程序或者会对界面修改的程序
                QApplication.processEvents()
            except BaseException as e:
                self.log.show('程序发生异常：', traceback.print_exc())
        else:
            pass

    def clickOnChooseFile(self):
        '''点击toolButton后，触发，显示文件对话框，供用户选择文件'''
        fileType = ''
        if self.inputTpye.__eq__('more'):
            # excle文件格式包含 xlsx 和 xls
            fileType ="excle files (*.xlsx *xls)"
        elif self.inputTpye.__eq__('local'):
            # 网页格式包括 html和 htm
            fileType = "html files (*.html *.htm)"
        absolute_path = QFileDialog.getOpenFileNames(self, 'Open file','/', fileType)
        filePath = absolute_path[0]
        self.lineEdit.setText('|'.join(filePath))

    def showLog(self, text):
        self.textBrowser.append(text)


class settingsScreen(QWidget,Ui_settings):
    '''软件的设置界面'''

    configFile = 'data/config.ini'
    configForDB = '数据库配置'
    linkDB = '连接数据库'
    database = '数据库'
    host ='hostname'
    databaseName = 'databasename'
    user = '用户名'
    passwd = '密码'
    file = '文件'
    fileP = '文件保存路径'
    update = '更新'
    checkForUpdate = '检测更新'
    updateSpace = '更新间隔'
    updateTime= '间隔时间'
    
    def __init__(self,parent= None):
        super(settingsScreen, self).__init__(parent)
        self.setupUi(self)
        self.readConfig()
        # 将 应用按钮 与 保存配置文件 关联
        self.apply.clicked.connect(self.writeConfig)
        self.toolButton.clicked.connect(self.clickOnChoose)
        self.reset.clicked.connect(self.clickOnReset)
        self.submit.clicked.connect(self.clickOnSubmit)

    def readConfig(self):
        '''读取配置，在创建配置界面时触发'''
        if not os.path.exists(self.configFile):
            self.createConfig()

        config = configparser.ConfigParser()
        # windows 记事本保存时只支持带BOM格式，为了兼容用记事本编辑过的文件能被正确读取，
        # 最好把编码指定为 utf-8-sig
        config.read(self.configFile,encoding="utf-8-sig")
        isLink = config.getboolean(self.configForDB,self.linkDB)
        dbtype = config.get(self.configForDB,self.database)
        host = config.get(self.configForDB,self.host)
        dbName = config.get(self.configForDB,self.databaseName)
        userN = config.get(self.configForDB,self.user)
        passW = config.get(self.configForDB,self.passwd)
        fileP = config.get(self.file,self.fileP)
        isCheckUpdate = config.getboolean(self.update,self.checkForUpdate)
        isCheckSpace = config.getboolean(self.update,self.updateSpace)
        updateSpace = config.getint(self.update,self.updateTime)

        self.groupDB.setChecked(isLink)
        # 获取下拉框的候选者，判断配置文件中的value是否在范围内
        count = self.databaseType.count()
        list = []
        for i in range(count):
            list.append(self.databaseType.itemText(i))
        index = list.index(dbtype)
        # self.databaseType.itemText(index)

        self.databaseType.setCurrentIndex(index)

        self.HostName.setText(host)
        self.DatabaseName.setText(dbName)
        self.userName.setText(userN)
        self.password.setText(passW)
        self.filePath.setText(fileP)
        self.groupUpdate.setChecked(isCheckUpdate)
        self.checkBox.setChecked(isCheckSpace)
        self.spinBox.setValue(updateSpace)

    def createConfig(self):
        '''默认的配置'''
        config = configparser.ConfigParser()
        config.read(self.configFile)
        config.add_section(self.configForDB)
        config.set(self.configForDB, self.linkDB, "false")
        config.set(self.configForDB, self.database, "MongoDB")
        config.set(self.configForDB, self.host, "")
        config.set(self.configForDB, self.databaseName, "")
        config.set(self.configForDB, self.user, "")
        config.set(self.configForDB, self.passwd, "")
        config.add_section(self.file)
        config.set(self.file, self.fileP, "新闻正文")
        config.add_section(self.update)
        config.set(self.update, self.checkForUpdate, "false")
        config.set(self.update, self.updateSpace, "false")
        config.set(self.update, self.updateTime, "24")
        curdir = os.getcwd()
        folderName = 'data'
        path = curdir + os.path.sep + folderName
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(self.configFile, 'w', encoding='utf-8')
        config.write(f)
        f.close()
    def writeConfig(self):
        '''将用户的配置修改保存下来'''
        config = configparser.ConfigParser()
        config.read(self.configFile, encoding="utf-8-sig")
        config.set(self.configForDB, self.linkDB, str(self.groupDB.isChecked()))
        config.set(self.configForDB, self.database, self.databaseType.currentText())
        config.set(self.configForDB, self.host, self.HostName.text())
        config.set(self.configForDB, self.databaseName, self.DatabaseName.text())
        config.set(self.configForDB, self.user, self.userName.text())
        config.set(self.configForDB, self.passwd, self.password.text())
        config.set(self.file, self.fileP, self.filePath.text())
        config.set(self.update, self.checkForUpdate, str(self.groupUpdate.isChecked()))
        config.set(self.update, self.updateSpace, str(self.checkBox.isChecked()))
        config.set(self.update, self.updateTime, str(self.spinBox.value()))
        f = open("data/Config.ini", 'w', encoding='utf-8')
        config.write(f)
        f.close()
        QMessageBox.information(self, '提示', '保存成功！')

    def clickOnChoose(self):
        '''通过文件对话框，确定文件保存路径'''
        absolute_path = QFileDialog.getExistingDirectory(self,'选择保存路径','/')
        self.filePath.setText(absolute_path)

    def clickOnReset(self):
        '''点击重置按钮，触发'''
        self.groupDB.setChecked(False)
        self.databaseType.setCurrentIndex(0)
        self.HostName.setText('')
        self.DatabaseName.setText('')
        self.userName.setText('')
        self.password.setText('')
        self.filePath.setText('新闻正文')
        self.groupUpdate.setChecked(False)
        self.checkBox.setChecked(False)
        self.spinBox.setValue(24)

    def clickOnSubmit(self):
        '''点击反馈功能后，触发 发邮件流程'''
        text = self.Feedback.toPlainText()
        if not text.strip():
            QMessageBox.information(self, '提示', '好像没有填写反馈信息哦！')
            return None
        ret  = sendEmail(text)
        if ret:
            print('反馈成功')
            QMessageBox.information(self, '提示', '发送成功！')
        else:
            print('反馈失败')
            QMessageBox.information(self, '提示', '发送失败！')


class Backend(QThread):
    '''用于发出更新text并发出信号，触发textbrowser更新显示'''
    update_date = pyqtSignal(str)
    text = 'init'
    def show(self):
        '''发出信号，触发与之关联的函数。'''
        # data = QDateTime.currentDateTime()
        self.update_date.emit((str(self.text)))
        self.text=''

    def setText(self,log):
        '''设置要显示的日志'''
        self.text = log



def main():
    app = QApplication(sys.argv)
    ui = MainScreen()
    # 采用 型号 和 槽的方式 , 将 日志 实时输出
    ui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()