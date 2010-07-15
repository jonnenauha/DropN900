# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginwidget.ui'
#
# Created: Thu Jul 15 03:09:29 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LoginWidget(object):
    def setupUi(self, LoginWidget):
        LoginWidget.setObjectName("LoginWidget")
        LoginWidget.resize(396, 297)
        LoginWidget.setStyleSheet("QWidget#LoginWidget {\n"
"    background-color: black;\n"
"}\n"
"\n"
"QLabel#label_info {\n"
"    color: #0099FF;\n"
"}")
        self.verticalLayout_2 = QtGui.QVBoxLayout(LoginWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_info = QtGui.QLabel(LoginWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_info.setFont(font)
        self.label_info.setAlignment(QtCore.Qt.AlignCenter)
        self.label_info.setWordWrap(True)
        self.label_info.setObjectName("label_info")
        self.verticalLayout.addWidget(self.label_info)
        self.button_action = QtGui.QPushButton(LoginWidget)
        self.button_action.setObjectName("button_action")
        self.verticalLayout.addWidget(self.button_action)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(LoginWidget)
        QtCore.QMetaObject.connectSlotsByName(LoginWidget)

    def retranslateUi(self, LoginWidget):
        LoginWidget.setWindowTitle(QtGui.QApplication.translate("LoginWidget", "LoginWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.label_info.setText(QtGui.QApplication.translate("LoginWidget", "You need to authenticate yourself to DropBox once and give permission for DropN900 to access your account\n"
"\n"
"Once you have authenticated to DropBox in the browser return to DropN900 to continue", None, QtGui.QApplication.UnicodeUTF8))
        self.button_action.setText(QtGui.QApplication.translate("LoginWidget", "Take me to authentication page", None, QtGui.QApplication.UnicodeUTF8))

