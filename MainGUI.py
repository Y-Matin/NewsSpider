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
        MainText.resize(805, 447)
        MainText.setStyleSheet("background-image: url(:/images/qian.png);")
        self.centralwidget = QtWidgets.QWidget(MainText)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(180, 40, 531, 51))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 40, 101, 51))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(-10, 180, 821, 211))
        self.textBrowser.setObjectName("textBrowser")
        MainText.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainText)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 29))
        self.menubar.setObjectName("menubar")
        self.menusetting = QtWidgets.QMenu(self.menubar)
        self.menusetting.setObjectName("menusetting")
        self.menus = QtWidgets.QMenu(self.menubar)
        self.menus.setObjectName("menus")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainText.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainText)
        self.statusbar.setObjectName("statusbar")
        MainText.setStatusBar(self.statusbar)
        self.action_3 = QtWidgets.QAction(MainText)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainText)
        self.action_4.setObjectName("action_4")
        self.action_5 = QtWidgets.QAction(MainText)
        self.action_5.setObjectName("action_5")
        self.action = QtWidgets.QAction(MainText)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainText)
        self.action_2.setObjectName("action_2")
        self.action_6 = QtWidgets.QAction(MainText)
        self.action_6.setObjectName("action_6")
        self.action_7 = QtWidgets.QAction(MainText)
        self.action_7.setObjectName("action_7")
        self.menusetting.addAction(self.action)
        self.menusetting.addAction(self.action_2)
        self.menus.addAction(self.action_6)
        self.menus.addAction(self.action_7)
        self.menu.addAction(self.action_3)
        self.menu.addAction(self.action_4)
        self.menu.addAction(self.action_5)
        self.menubar.addAction(self.menusetting.menuAction())
        self.menubar.addAction(self.menus.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainText)
        QtCore.QMetaObject.connectSlotsByName(MainText)

    def retranslateUi(self, MainText):
        _translate = QtCore.QCoreApplication.translate
        MainText.setWindowTitle(_translate("MainText", "MainText"))
        self.label.setText(_translate("MainText", "网页地址："))
        self.textBrowser.setHtml(_translate("MainText", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9.07563pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9.07563pt;\">***********************控制台信息******************</span></p></body></html>"))
        self.menusetting.setTitle(_translate("MainText", "爬取方式"))
        self.menus.setTitle(_translate("MainText", "设置"))
        self.menu.setTitle(_translate("MainText", "帮助"))
        self.action_3.setText(_translate("MainText", "关于"))
        self.action_4.setText(_translate("MainText", "帮助"))
        self.action_5.setText(_translate("MainText", "更新"))
        self.action.setText(_translate("MainText", "单次爬取"))
        self.action_2.setText(_translate("MainText", "批量爬取"))
        self.action_6.setText(_translate("MainText", "新增配置文件"))
        self.action_7.setText(_translate("MainText", "修改配置文件"))

import images_rc
