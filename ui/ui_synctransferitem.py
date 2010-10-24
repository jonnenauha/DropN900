# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'synctransferitem.ui'
#
# Created: Sun Oct 24 18:35:48 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SyncTransferItem(object):
    def setupUi(self, SyncTransferItem):
        SyncTransferItem.setObjectName("SyncTransferItem")
        SyncTransferItem.resize(745, 87)
        SyncTransferItem.setStyleSheet("QFrame#content_frame {\n"
"    border: 0px;\n"
"    border-bottom: 1px solid grey;\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.466182, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255), stop:0.462312 rgba(34, 34, 34, 255), stop:1 rgba(22, 22, 22, 255));\n"
"}\n"
"\n"
"QLabel {\n"
"    color: rgb(218, 218, 218);\n"
"    font-size: 13pt;\n"
"}\n"
"\n"
"QLabel#dl_present, #dl_total, #dl_separator, #dl_separator2 {\n"
"    color: rgb(33, 198, 61);\n"
"}\n"
"\n"
"QLabel#ul_present, #ul_total, #ul_separator, #ul_separator2 {\n"
"    color: rgb(209, 18, 22);\n"
"}\n"
"\n"
"QLabel#status_label {\n"
"    font-size: 15pt;\n"
"    color: white;\n"
"}\n"
"\n"
"QLabel#dl_status, #ul_status {\n"
"    font-size: 11pt;\n"
"}\n"
"\n"
"QLabel#label_dl, #label_ul {\n"
"    color: #0099FF;\n"
"    font: arial;\n"
"    font-size: 13pt;\n"
"}")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(SyncTransferItem)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.content_frame = QtGui.QFrame(SyncTransferItem)
        self.content_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.content_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.content_frame.setObjectName("content_frame")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.content_frame)
        self.horizontalLayout_3.setContentsMargins(0, 6, 10, 6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.main_icon = QtGui.QLabel(self.content_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_icon.sizePolicy().hasHeightForWidth())
        self.main_icon.setSizePolicy(sizePolicy)
        self.main_icon.setMinimumSize(QtCore.QSize(64, 0))
        self.main_icon.setMaximumSize(QtCore.QSize(64, 16777215))
        self.main_icon.setText("")
        self.main_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.main_icon.setIndent(0)
        self.main_icon.setObjectName("main_icon")
        self.horizontalLayout_3.addWidget(self.main_icon)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.status_label = QtGui.QLabel(self.content_frame)
        self.status_label.setObjectName("status_label")
        self.verticalLayout.addWidget(self.status_label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_dl = QtGui.QLabel(self.content_frame)
        self.label_dl.setMinimumSize(QtCore.QSize(120, 0))
        self.label_dl.setObjectName("label_dl")
        self.horizontalLayout.addWidget(self.label_dl)
        self.dl_present = QtGui.QLabel(self.content_frame)
        self.dl_present.setMinimumSize(QtCore.QSize(35, 0))
        self.dl_present.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dl_present.setObjectName("dl_present")
        self.horizontalLayout.addWidget(self.dl_present)
        self.dl_separator = QtGui.QLabel(self.content_frame)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.dl_separator.setFont(font)
        self.dl_separator.setObjectName("dl_separator")
        self.horizontalLayout.addWidget(self.dl_separator)
        self.dl_total = QtGui.QLabel(self.content_frame)
        self.dl_total.setMinimumSize(QtCore.QSize(35, 0))
        self.dl_total.setObjectName("dl_total")
        self.horizontalLayout.addWidget(self.dl_total)
        self.dl_status = QtGui.QLabel(self.content_frame)
        self.dl_status.setObjectName("dl_status")
        self.horizontalLayout.addWidget(self.dl_status)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.dl_timer_label = QtGui.QLabel(self.content_frame)
        self.dl_timer_label.setMinimumSize(QtCore.QSize(60, 0))
        self.dl_timer_label.setText("")
        self.dl_timer_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dl_timer_label.setObjectName("dl_timer_label")
        self.horizontalLayout.addWidget(self.dl_timer_label)
        self.dl_separator2 = QtGui.QLabel(self.content_frame)
        self.dl_separator2.setMinimumSize(QtCore.QSize(20, 0))
        self.dl_separator2.setAlignment(QtCore.Qt.AlignCenter)
        self.dl_separator2.setObjectName("dl_separator2")
        self.horizontalLayout.addWidget(self.dl_separator2)
        self.dl_size = QtGui.QLabel(self.content_frame)
        self.dl_size.setMinimumSize(QtCore.QSize(70, 0))
        self.dl_size.setText("")
        self.dl_size.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.dl_size.setObjectName("dl_size")
        self.horizontalLayout.addWidget(self.dl_size)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_ul = QtGui.QLabel(self.content_frame)
        self.label_ul.setMinimumSize(QtCore.QSize(120, 0))
        self.label_ul.setObjectName("label_ul")
        self.horizontalLayout_4.addWidget(self.label_ul)
        self.ul_present = QtGui.QLabel(self.content_frame)
        self.ul_present.setMinimumSize(QtCore.QSize(35, 0))
        self.ul_present.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ul_present.setObjectName("ul_present")
        self.horizontalLayout_4.addWidget(self.ul_present)
        self.ul_separator = QtGui.QLabel(self.content_frame)
        self.ul_separator.setObjectName("ul_separator")
        self.horizontalLayout_4.addWidget(self.ul_separator)
        self.ul_total = QtGui.QLabel(self.content_frame)
        self.ul_total.setMinimumSize(QtCore.QSize(35, 0))
        self.ul_total.setObjectName("ul_total")
        self.horizontalLayout_4.addWidget(self.ul_total)
        self.ul_status = QtGui.QLabel(self.content_frame)
        self.ul_status.setObjectName("ul_status")
        self.horizontalLayout_4.addWidget(self.ul_status)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.ul_timer_label = QtGui.QLabel(self.content_frame)
        self.ul_timer_label.setMinimumSize(QtCore.QSize(60, 0))
        self.ul_timer_label.setText("")
        self.ul_timer_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ul_timer_label.setObjectName("ul_timer_label")
        self.horizontalLayout_4.addWidget(self.ul_timer_label)
        self.ul_separator2 = QtGui.QLabel(self.content_frame)
        self.ul_separator2.setMinimumSize(QtCore.QSize(20, 0))
        self.ul_separator2.setAlignment(QtCore.Qt.AlignCenter)
        self.ul_separator2.setObjectName("ul_separator2")
        self.horizontalLayout_4.addWidget(self.ul_separator2)
        self.ul_size = QtGui.QLabel(self.content_frame)
        self.ul_size.setMinimumSize(QtCore.QSize(70, 0))
        self.ul_size.setText("")
        self.ul_size.setObjectName("ul_size")
        self.horizontalLayout_4.addWidget(self.ul_size)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addWidget(self.content_frame)

        self.retranslateUi(SyncTransferItem)
        QtCore.QMetaObject.connectSlotsByName(SyncTransferItem)

    def retranslateUi(self, SyncTransferItem):
        SyncTransferItem.setWindowTitle(QtGui.QApplication.translate("SyncTransferItem", "SyncTransferItem", None, QtGui.QApplication.UnicodeUTF8))
        self.status_label.setText(QtGui.QApplication.translate("SyncTransferItem", "Sync in progress...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_dl.setText(QtGui.QApplication.translate("SyncTransferItem", "Downloads", None, QtGui.QApplication.UnicodeUTF8))
        self.dl_present.setText(QtGui.QApplication.translate("SyncTransferItem", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.dl_separator.setText(QtGui.QApplication.translate("SyncTransferItem", "/", None, QtGui.QApplication.UnicodeUTF8))
        self.dl_total.setText(QtGui.QApplication.translate("SyncTransferItem", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.dl_status.setText(QtGui.QApplication.translate("SyncTransferItem", "status", None, QtGui.QApplication.UnicodeUTF8))
        self.dl_separator2.setText(QtGui.QApplication.translate("SyncTransferItem", "|", None, QtGui.QApplication.UnicodeUTF8))
        self.label_ul.setText(QtGui.QApplication.translate("SyncTransferItem", "Uploads", None, QtGui.QApplication.UnicodeUTF8))
        self.ul_present.setText(QtGui.QApplication.translate("SyncTransferItem", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.ul_separator.setText(QtGui.QApplication.translate("SyncTransferItem", "/", None, QtGui.QApplication.UnicodeUTF8))
        self.ul_total.setText(QtGui.QApplication.translate("SyncTransferItem", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.ul_status.setText(QtGui.QApplication.translate("SyncTransferItem", "status", None, QtGui.QApplication.UnicodeUTF8))
        self.ul_separator2.setText(QtGui.QApplication.translate("SyncTransferItem", "|", None, QtGui.QApplication.UnicodeUTF8))

