# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'consolewidget.ui'
#
# Created: Thu Jul 29 22:32:42 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ConsoleWidget(object):
    def setupUi(self, ConsoleWidget):
        ConsoleWidget.setObjectName("ConsoleWidget")
        ConsoleWidget.resize(563, 343)
        self.verticalLayout = QtGui.QVBoxLayout(ConsoleWidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setMargin(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text_area = QtGui.QPlainTextEdit(ConsoleWidget)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.text_area.setFont(font)
        self.text_area.setObjectName("text_area")
        self.verticalLayout.addWidget(self.text_area)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_save = QtGui.QPushButton(ConsoleWidget)
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.button_save.setFont(font)
        self.button_save.setObjectName("button_save")
        self.horizontalLayout.addWidget(self.button_save)
        self.button_back = QtGui.QPushButton(ConsoleWidget)
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.button_back.setFont(font)
        self.button_back.setObjectName("button_back")
        self.horizontalLayout.addWidget(self.button_back)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ConsoleWidget)
        QtCore.QMetaObject.connectSlotsByName(ConsoleWidget)

    def retranslateUi(self, ConsoleWidget):
        ConsoleWidget.setWindowTitle(QtGui.QApplication.translate("ConsoleWidget", "DropN900 - Log", None, QtGui.QApplication.UnicodeUTF8))
        ConsoleWidget.setStyleSheet(QtGui.QApplication.translate("ConsoleWidget", "QWidget#ConsoleWidget {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(6, 6, 6, 255), stop:1 rgba(45, 45, 45, 255));\n"
"}\n"
"\n"
"QLabel#title_download_folder, #title_authentication, #title_sync {\n"
"    color: #0099FF;\n"
"    font-size: 16pt;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPlainTextEdit#text_area {\n"
"    background-color: white;\n"
"    border: 2px solid rgba(255,255,255,200);\n"
"    border-radius: 10px;\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"QPushButton {\n"
"    min-height: 65px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid rgba(255,255,255,200);\n"
"    color: rgb(230, 230, 230);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(16, 16, 16, 255), stop:0.5 rgba(55, 55, 55, 210), stop:1 rgba(36, 36, 36, 255));\n"
"    font: Arial;\n"
"    font-size: 19pt;\n"
"}\n"
"\n"
"QPushButton#button_save{\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"    border-right: 0px;\n"
"}\n"
"\n"
"QPushButton#button_back {\n"
"    border-top-left-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(59, 59, 59, 255), stop:0.5 rgba(82, 82, 82, 255), stop:1 rgba(68, 68, 68, 255));\n"
"    color: #0099FF;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.button_save.setText(QtGui.QApplication.translate("ConsoleWidget", "SAVE LOG TO FILE", None, QtGui.QApplication.UnicodeUTF8))
        self.button_back.setText(QtGui.QApplication.translate("ConsoleWidget", "RETURN", None, QtGui.QApplication.UnicodeUTF8))

