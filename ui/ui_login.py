# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Tue Jul 13 18:19:50 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LoginWidget(object):
    def setupUi(self, LoginWidget):
        LoginWidget.setObjectName("LoginWidget")
        LoginWidget.resize(537, 412)
        font = QtGui.QFont()
        font.setPointSize(14)
        LoginWidget.setFont(font)
        LoginWidget.setStyleSheet("QWidget#LoginWidget {\n"
"    background-color: black;\n"
"}\n"
"\n"
"QFrame#webview_container {\n"
"    border: 2px solid white;\n"
"    border-radius: 10px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"    padding-bottom: 8px;\n"
"}\n"
"\n"
"QLabel#label_info {\n"
"    color: #0099FF;\n"
"}\n"
"\n"
"QLabel#webview_status_label {\n"
"    color: white;\n"
"}")
        self.verticalLayout = QtGui.QVBoxLayout(LoginWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_info = QtGui.QLabel(LoginWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_info.setFont(font)
        self.label_info.setAlignment(QtCore.Qt.AlignCenter)
        self.label_info.setObjectName("label_info")
        self.verticalLayout.addWidget(self.label_info)
        self.url_line_edit = QtGui.QLineEdit(LoginWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.url_line_edit.setFont(font)
        self.url_line_edit.setText("")
        self.url_line_edit.setObjectName("url_line_edit")
        self.verticalLayout.addWidget(self.url_line_edit)
        self.webview = QtWebKit.QWebView(LoginWidget)
        self.webview.setUrl(QtCore.QUrl("about:blank"))
        self.webview.setObjectName("webview")
        self.verticalLayout.addWidget(self.webview)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.webview_status_label = QtGui.QLabel(LoginWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webview_status_label.sizePolicy().hasHeightForWidth())
        self.webview_status_label.setSizePolicy(sizePolicy)
        self.webview_status_label.setMinimumSize(QtCore.QSize(150, 0))
        self.webview_status_label.setText("")
        self.webview_status_label.setObjectName("webview_status_label")
        self.horizontalLayout.addWidget(self.webview_status_label)
        self.button_done = QtGui.QPushButton(LoginWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.button_done.setFont(font)
        self.button_done.setObjectName("button_done")
        self.horizontalLayout.addWidget(self.button_done)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LoginWidget)
        QtCore.QMetaObject.connectSlotsByName(LoginWidget)

    def retranslateUi(self, LoginWidget):
        LoginWidget.setWindowTitle(QtGui.QApplication.translate("LoginWidget", "LoginWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.label_info.setText(QtGui.QApplication.translate("LoginWidget", "Please authenticate yourself to DropBox", None, QtGui.QApplication.UnicodeUTF8))
        self.button_done.setText(QtGui.QApplication.translate("LoginWidget", "Continue", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
