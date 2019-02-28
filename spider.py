# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spider.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(777, 372)
        Form.setStyleSheet("background-image: url(:/images/qian.png);")
        self.url = QtWidgets.QLabel(Form)
        self.url.setGeometry(QtCore.QRect(40, 90, 72, 15))
        self.url.setObjectName("url")
        self.clear = QtWidgets.QPushButton(Form)
        self.clear.setGeometry(QtCore.QRect(260, 310, 92, 28))
        self.clear.setObjectName("clear")
        self.submit = QtWidgets.QPushButton(Form)
        self.submit.setGeometry(QtCore.QRect(420, 310, 92, 28))
        self.submit.setObjectName("submit")
        self.input_url = QtWidgets.QTextEdit(Form)
        self.input_url.setGeometry(QtCore.QRect(130, 80, 581, 41))
        self.input_url.setObjectName("input_url")
        self.once = QtWidgets.QRadioButton(Form)
        self.once.setGeometry(QtCore.QRect(30, 30, 112, 19))
        self.once.setObjectName("once")
        self.input_filePath = QtWidgets.QTextEdit(Form)
        self.input_filePath.setGeometry(QtCore.QRect(130, 220, 581, 41))
        self.input_filePath.setObjectName("input_filePath")
        self.filePath = QtWidgets.QLabel(Form)
        self.filePath.setGeometry(QtCore.QRect(40, 230, 72, 15))
        self.filePath.setStyleSheet("")
        self.filePath.setObjectName("filePath")
        self.batch = QtWidgets.QRadioButton(Form)
        self.batch.setGeometry(QtCore.QRect(30, 190, 112, 19))
        self.batch.setObjectName("batch")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "爬取新闻正文"))
        self.url.setText(_translate("Form", "网页地址："))
        self.clear.setText(_translate("Form", "重置"))
        self.submit.setText(_translate("Form", "爬取"))
        self.once.setText(_translate("Form", "单次爬取"))
        self.filePath.setText(_translate("Form", "导入文件："))
        self.batch.setText(_translate("Form", "批量爬取"))

import images_rc
