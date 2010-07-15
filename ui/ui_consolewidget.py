# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'consolewidget.ui'
#
# Created: Thu Jul 15 03:24:04 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ConsoleWidget(object):
    def setupUi(self, ConsoleWidget):
        ConsoleWidget.setObjectName("ConsoleWidget")
        ConsoleWidget.resize(386, 230)
        self.verticalLayout = QtGui.QVBoxLayout(ConsoleWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text_area = QtGui.QPlainTextEdit(ConsoleWidget)
        self.text_area.setObjectName("text_area")
        self.verticalLayout.addWidget(self.text_area)
        self.button_back = QtGui.QPushButton(ConsoleWidget)
        self.button_back.setObjectName("button_back")
        self.verticalLayout.addWidget(self.button_back)

        self.retranslateUi(ConsoleWidget)
        QtCore.QMetaObject.connectSlotsByName(ConsoleWidget)

    def retranslateUi(self, ConsoleWidget):
        ConsoleWidget.setWindowTitle(QtGui.QApplication.translate("ConsoleWidget", "ConsoleWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.button_back.setText(QtGui.QApplication.translate("ConsoleWidget", "Back", None, QtGui.QApplication.UnicodeUTF8))

