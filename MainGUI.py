# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainGUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainText(object):
    def setupUi(self, MainText):
        MainText.setObjectName("MainText")
        MainText.resize(548, 467)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/spider.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainText.setWindowIcon(icon)
        MainText.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainText)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, 5, 5, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.reset.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/reset.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reset.setIcon(icon1)
        self.reset.setObjectName("reset")
        self.horizontalLayout_2.addWidget(self.reset)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.extract = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.extract.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/extract.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.extract.setIcon(icon2)
        self.extract.setObjectName("extract")
        self.horizontalLayout_2.addWidget(self.extract)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        MainText.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainText)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 548, 29))
        self.menubar.setObjectName("menubar")
        self.menusetting = QtWidgets.QMenu(self.menubar)
        self.menusetting.setObjectName("menusetting")
        self.menus = QtWidgets.QMenu(self.menubar)
        self.menus.setObjectName("menus")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainText.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainText)
        self.statusbar.setObjectName("statusbar")
        MainText.setStatusBar(self.statusbar)
        self.about = QtWidgets.QAction(MainText)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/about.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.about.setIcon(icon3)
        self.about.setObjectName("about")
        self.help = QtWidgets.QAction(MainText)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help.setIcon(icon4)
        self.help.setObjectName("help")
        self.update = QtWidgets.QAction(MainText)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/update.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.update.setIcon(icon5)
        self.update.setObjectName("update")
        self.once = QtWidgets.QAction(MainText)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/once.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.once.setIcon(icon6)
        self.once.setObjectName("once")
        self.more = QtWidgets.QAction(MainText)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/images/more.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.more.setIcon(icon7)
        self.more.setObjectName("more")
        self.addFile = QtWidgets.QAction(MainText)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/images/addFile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addFile.setIcon(icon8)
        self.addFile.setObjectName("addFile")
        self.modifyFile = QtWidgets.QAction(MainText)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/images/modifyFile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.modifyFile.setIcon(icon9)
        self.modifyFile.setObjectName("modifyFile")
        self.feedBack = QtWidgets.QAction(MainText)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/images/feedBack.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.feedBack.setIcon(icon10)
        self.feedBack.setObjectName("feedBack")
        self.menusetting.addAction(self.once)
        self.menusetting.addAction(self.more)
        self.menus.addAction(self.addFile)
        self.menus.addAction(self.modifyFile)
        self.menu.addAction(self.help)
        self.menu.addAction(self.feedBack)
        self.menu_2.addAction(self.about)
        self.menu_2.addAction(self.update)
        self.menubar.addAction(self.menusetting.menuAction())
        self.menubar.addAction(self.menus.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainText)
        QtCore.QMetaObject.connectSlotsByName(MainText)

    def retranslateUi(self, MainText):
        _translate = QtCore.QCoreApplication.translate
        MainText.setWindowTitle(_translate("MainText", "MainText"))
        self.label.setText(_translate("MainText", "网页地址："))
        self.reset.setText(_translate("MainText", "重置"))
        self.extract.setText(_translate("MainText", "提取"))
        self.textBrowser.setHtml(_translate("MainText", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9.07563pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9.07563pt;\">*****************</span><span style=\" font-size:9.07563pt; font-weight:600;\">日志信息</span><span style=\" font-size:9.07563pt;\">******************</span></p></body></html>"))
        self.menusetting.setTitle(_translate("MainText", "爬取方式"))
        self.menus.setTitle(_translate("MainText", "设置"))
        self.menu.setTitle(_translate("MainText", "帮助"))
        self.menu_2.setTitle(_translate("MainText", "关于"))
        self.about.setText(_translate("MainText", "关于"))
        self.help.setText(_translate("MainText", "帮助"))
        self.update.setText(_translate("MainText", "更新"))
        self.once.setText(_translate("MainText", "单次爬取"))
        self.more.setText(_translate("MainText", "批量爬取"))
        self.addFile.setText(_translate("MainText", "新增配置文件"))
        self.modifyFile.setText(_translate("MainText", "修改配置文件"))
        self.feedBack.setText(_translate("MainText", "反馈"))

import images_rc
