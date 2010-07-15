# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'browserwidget.ui'
#
# Created: Thu Jul 15 02:58:52 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_BrowserWidget(object):
    def setupUi(self, BrowserWidget):
        BrowserWidget.setObjectName("BrowserWidget")
        BrowserWidget.resize(537, 412)
        font = QtGui.QFont()
        font.setPointSize(14)
        BrowserWidget.setFont(font)
        BrowserWidget.setStyleSheet("QWidget#BrowserWidget {\n"
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
        self.verticalLayout = QtGui.QVBoxLayout(BrowserWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_info = QtGui.QLabel(BrowserWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_info.setFont(font)
        self.label_info.setAlignment(QtCore.Qt.AlignCenter)
        self.label_info.setObjectName("label_info")
        self.verticalLayout.addWidget(self.label_info)
        self.url_line_edit = QtGui.QLineEdit(BrowserWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.url_line_edit.setFont(font)
        self.url_line_edit.setText("")
        self.url_line_edit.setObjectName("url_line_edit")
        self.verticalLayout.addWidget(self.url_line_edit)
        self.webview = QtWebKit.QWebView(BrowserWidget)
        self.webview.setUrl(QtCore.QUrl("about:blank"))
        self.webview.setObjectName("webview")
        self.verticalLayout.addWidget(self.webview)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.webview_status_label = QtGui.QLabel(BrowserWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webview_status_label.sizePolicy().hasHeightForWidth())
        self.webview_status_label.setSizePolicy(sizePolicy)
        self.webview_status_label.setMinimumSize(QtCore.QSize(150, 0))
        self.webview_status_label.setText("")
        self.webview_status_label.setObjectName("webview_status_label")
        self.horizontalLayout.addWidget(self.webview_status_label)
        self.button_done = QtGui.QPushButton(BrowserWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.button_done.setFont(font)
        self.button_done.setObjectName("button_done")
        self.horizontalLayout.addWidget(self.button_done)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(BrowserWidget)
        QtCore.QMetaObject.connectSlotsByName(BrowserWidget)

    def retranslateUi(self, BrowserWidget):
        BrowserWidget.setWindowTitle(QtGui.QApplication.translate("BrowserWidget", "BrowserWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.label_info.setText(QtGui.QApplication.translate("BrowserWidget", "Please authenticate yourself to DropBox", None, QtGui.QApplication.UnicodeUTF8))
        self.button_done.setText(QtGui.QApplication.translate("BrowserWidget", "Continue", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
