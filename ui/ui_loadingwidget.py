# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadingwidget.ui'
#
# Created: Tue Jul 13 17:43:48 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LoadingWidget(object):
    def setupUi(self, LoadingWidget):
        LoadingWidget.setObjectName("LoadingWidget")
        LoadingWidget.resize(176, 50)
        LoadingWidget.setStyleSheet("QLabel {\n"
"    color: rgb(221, 221, 221);\n"
"}")
        self.verticalLayout_2 = QtGui.QVBoxLayout(LoadingWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.info_label = QtGui.QLabel(LoadingWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.info_label.setFont(font)
        self.info_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.info_label.setWordWrap(True)
        self.info_label.setObjectName("info_label")
        self.horizontalLayout.addWidget(self.info_label)
        self.info_label_icon = QtGui.QLabel(LoadingWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_label_icon.sizePolicy().hasHeightForWidth())
        self.info_label_icon.setSizePolicy(sizePolicy)
        self.info_label_icon.setMinimumSize(QtCore.QSize(24, 24))
        self.info_label_icon.setMaximumSize(QtCore.QSize(24, 24))
        self.info_label_icon.setText("")
        self.info_label_icon.setObjectName("info_label_icon")
        self.horizontalLayout.addWidget(self.info_label_icon)
        self.load_animation_label = QtGui.QLabel(LoadingWidget)
        self.load_animation_label.setMinimumSize(QtCore.QSize(48, 48))
        self.load_animation_label.setMaximumSize(QtCore.QSize(48, 48))
        self.load_animation_label.setText("")
        self.load_animation_label.setAlignment(QtCore.Qt.AlignCenter)
        self.load_animation_label.setObjectName("load_animation_label")
        self.horizontalLayout.addWidget(self.load_animation_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(LoadingWidget)
        QtCore.QMetaObject.connectSlotsByName(LoadingWidget)

    def retranslateUi(self, LoadingWidget):
        LoadingWidget.setWindowTitle(QtGui.QApplication.translate("LoadingWidget", "LoadingWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.info_label.setText(QtGui.QApplication.translate("LoadingWidget", "Info label", None, QtGui.QApplication.UnicodeUTF8))

