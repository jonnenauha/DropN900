# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'transferwidget.ui'
#
# Created: Fri Jul 30 03:10:39 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TransferWidget(object):
    def setupUi(self, TransferWidget):
        TransferWidget.setObjectName("TransferWidget")
        TransferWidget.resize(831, 399)
        self.verticalLayout = QtGui.QVBoxLayout(TransferWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtGui.QScrollArea(TransferWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 829, 397))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.item_layout = QtGui.QVBoxLayout()
        self.item_layout.setSpacing(0)
        self.item_layout.setObjectName("item_layout")
        self.label_first_time_icon = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_first_time_icon.sizePolicy().hasHeightForWidth())
        self.label_first_time_icon.setSizePolicy(sizePolicy)
        self.label_first_time_icon.setMinimumSize(QtCore.QSize(0, 168))
        self.label_first_time_icon.setMaximumSize(QtCore.QSize(16777215, 168))
        self.label_first_time_icon.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_first_time_icon.setObjectName("label_first_time_icon")
        self.item_layout.addWidget(self.label_first_time_icon)
        self.label_first_time_note = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_first_time_note.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.label_first_time_note.setFont(font)
        self.label_first_time_note.setAlignment(QtCore.Qt.AlignCenter)
        self.label_first_time_note.setObjectName("label_first_time_note")
        self.item_layout.addWidget(self.label_first_time_note)
        spacerItem = QtGui.QSpacerItem(1, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.item_layout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.item_layout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(TransferWidget)
        QtCore.QMetaObject.connectSlotsByName(TransferWidget)

    def retranslateUi(self, TransferWidget):
        TransferWidget.setWindowTitle(QtGui.QApplication.translate("TransferWidget", "DropN900 - Transfers", None, QtGui.QApplication.UnicodeUTF8))
        self.label_first_time_note.setStyleSheet(QtGui.QApplication.translate("TransferWidget", "color: rgb(231, 231, 231);", None, QtGui.QApplication.UnicodeUTF8))
        self.label_first_time_note.setText(QtGui.QApplication.translate("TransferWidget", "This session has no tranfer history", None, QtGui.QApplication.UnicodeUTF8))

