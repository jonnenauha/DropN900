# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'trustedloginwidget.ui'
#
# Created: Tue Nov 23 03:31:04 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TrustedLoginWidget(object):
    def setupUi(self, TrustedLoginWidget):
        TrustedLoginWidget.setObjectName("TrustedLoginWidget")
        TrustedLoginWidget.resize(824, 445)
        TrustedLoginWidget.setStyleSheet("QWidget#TrustedLoginWidget {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(6, 6, 6, 255), stop:1 rgba(45, 45, 45, 255));\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 1px solid gray;\n"
"    border-radius: 7px;\n"
"    padding: 5px;\n"
"    font-size: 19pt;\n"
"    background-color: white;\n"
"    color: black;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #0099FF;\n"
"    font-size: 19pt;\n"
"    min-height: 65px;\n"
"}\n"
"\n"
"QLabel#label_info {\n"
"    color: white;\n"
"}\n"
"\n"
"QLabel#label_icon {\n"
"    background-color: transparent;\n"
"    border: 0px;\n"
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
"QPushButton:hover {\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(59, 59, 59, 255), stop:0.5 rgba(82, 82, 82, 255), stop:1 rgba(68, 68, 68, 255));\n"
"    color: #0099FF;\n"
"}")
        self.verticalLayout_2 = QtGui.QVBoxLayout(TrustedLoginWidget)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setMargin(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_icon = QtGui.QLabel(TrustedLoginWidget)
        self.label_icon.setMinimumSize(QtCore.QSize(150, 65))
        self.label_icon.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_icon.setText("")
        self.label_icon.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_icon.setObjectName("label_icon")
        self.horizontalLayout_3.addWidget(self.label_icon)
        self.label_info = QtGui.QLabel(TrustedLoginWidget)
        self.label_info.setWordWrap(True)
        self.label_info.setObjectName("label_info")
        self.horizontalLayout_3.addWidget(self.label_info)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_email = QtGui.QLabel(TrustedLoginWidget)
        self.label_email.setMinimumSize(QtCore.QSize(150, 65))
        self.label_email.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_email.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_email.setObjectName("label_email")
        self.horizontalLayout.addWidget(self.label_email)
        self.line_edit_email = QtGui.QLineEdit(TrustedLoginWidget)
        self.line_edit_email.setMinimumSize(QtCore.QSize(0, 65))
        self.line_edit_email.setMaxLength(32767)
        self.line_edit_email.setFrame(False)
        self.line_edit_email.setObjectName("line_edit_email")
        self.horizontalLayout.addWidget(self.line_edit_email)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_password = QtGui.QLabel(TrustedLoginWidget)
        self.label_password.setMinimumSize(QtCore.QSize(150, 65))
        self.label_password.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_password.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_password.setObjectName("label_password")
        self.horizontalLayout_2.addWidget(self.label_password)
        self.line_edit_password = QtGui.QLineEdit(TrustedLoginWidget)
        self.line_edit_password.setMinimumSize(QtCore.QSize(0, 65))
        self.line_edit_password.setFrame(False)
        self.line_edit_password.setEchoMode(QtGui.QLineEdit.Password)
        self.line_edit_password.setObjectName("line_edit_password")
        self.horizontalLayout_2.addWidget(self.line_edit_password)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_error = QtGui.QLabel(TrustedLoginWidget)
        self.label_error.setText("")
        self.label_error.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_error.setObjectName("label_error")
        self.verticalLayout.addWidget(self.label_error)
        self.button_auth = QtGui.QPushButton(TrustedLoginWidget)
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.button_auth.setFont(font)
        self.button_auth.setObjectName("button_auth")
        self.verticalLayout.addWidget(self.button_auth)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(TrustedLoginWidget)
        QtCore.QMetaObject.connectSlotsByName(TrustedLoginWidget)

    def retranslateUi(self, TrustedLoginWidget):
        TrustedLoginWidget.setWindowTitle(QtGui.QApplication.translate("TrustedLoginWidget", "TrustedLoginWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.label_icon.setStyleSheet(QtGui.QApplication.translate("TrustedLoginWidget", "padding-right: 10px;", None, QtGui.QApplication.UnicodeUTF8))
        self.label_info.setText(QtGui.QApplication.translate("TrustedLoginWidget", "Please authenticate with your DropBox credentials", None, QtGui.QApplication.UnicodeUTF8))
        self.label_email.setText(QtGui.QApplication.translate("TrustedLoginWidget", "Email", None, QtGui.QApplication.UnicodeUTF8))
        self.label_password.setText(QtGui.QApplication.translate("TrustedLoginWidget", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label_error.setStyleSheet(QtGui.QApplication.translate("TrustedLoginWidget", "color: red;", None, QtGui.QApplication.UnicodeUTF8))
        self.button_auth.setText(QtGui.QApplication.translate("TrustedLoginWidget", "AUTHENTICATE", None, QtGui.QApplication.UnicodeUTF8))

