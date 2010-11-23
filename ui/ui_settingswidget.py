# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingswidget.ui'
#
# Created: Tue Nov 23 03:27:49 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SettingsWidget(object):
    def setupUi(self, SettingsWidget):
        SettingsWidget.setObjectName("SettingsWidget")
        SettingsWidget.resize(1009, 561)
        SettingsWidget.setStyleSheet("QLineEdit {\n"
"    background-color: white;\n"
"    color: black;\n"
"}")
        self.verticalLayout = QtGui.QVBoxLayout(SettingsWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtGui.QScrollArea(SettingsWidget)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 991, 963))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setSpacing(10)
        self.main_layout.setObjectName("main_layout")
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.downloading_icon = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloading_icon.sizePolicy().hasHeightForWidth())
        self.downloading_icon.setSizePolicy(sizePolicy)
        self.downloading_icon.setMinimumSize(QtCore.QSize(48, 84))
        self.downloading_icon.setText("")
        self.downloading_icon.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.downloading_icon.setObjectName("downloading_icon")
        self.horizontalLayout_4.addWidget(self.downloading_icon)
        self.title_download_folder = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_download_folder.sizePolicy().hasHeightForWidth())
        self.title_download_folder.setSizePolicy(sizePolicy)
        self.title_download_folder.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.title_download_folder.setIndent(0)
        self.title_download_folder.setObjectName("title_download_folder")
        self.horizontalLayout_4.addWidget(self.title_download_folder)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem = QtGui.QSpacerItem(1, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.frame = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.frame.setMinimumSize(QtCore.QSize(0, 26))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3.addWidget(self.frame)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.main_layout.addLayout(self.horizontalLayout_4)
        self.label = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.main_layout.addWidget(self.label)
        self.download_layout = QtGui.QHBoxLayout()
        self.download_layout.setSpacing(10)
        self.download_layout.setObjectName("download_layout")
        self.lineedit_default_download_folder = QtGui.QLineEdit(self.scrollAreaWidgetContents)
        self.lineedit_default_download_folder.setMinimumSize(QtCore.QSize(0, 65))
        self.lineedit_default_download_folder.setObjectName("lineedit_default_download_folder")
        self.download_layout.addWidget(self.lineedit_default_download_folder)
        self.button_browse_folder = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.button_browse_folder.setMinimumSize(QtCore.QSize(200, 65))
        self.button_browse_folder.setStyleSheet("")
        self.button_browse_folder.setObjectName("button_browse_folder")
        self.download_layout.addWidget(self.button_browse_folder)
        self.main_layout.addLayout(self.download_layout)
        self.checkbox_no_dl_dialog = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.checkbox_no_dl_dialog.setMinimumSize(QtCore.QSize(0, 65))
        self.checkbox_no_dl_dialog.setObjectName("checkbox_no_dl_dialog")
        self.main_layout.addWidget(self.checkbox_no_dl_dialog)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.authentication_icon = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.authentication_icon.sizePolicy().hasHeightForWidth())
        self.authentication_icon.setSizePolicy(sizePolicy)
        self.authentication_icon.setMinimumSize(QtCore.QSize(48, 84))
        self.authentication_icon.setText("")
        self.authentication_icon.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.authentication_icon.setObjectName("authentication_icon")
        self.horizontalLayout_5.addWidget(self.authentication_icon)
        self.title_authentication = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_authentication.sizePolicy().hasHeightForWidth())
        self.title_authentication.setSizePolicy(sizePolicy)
        self.title_authentication.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.title_authentication.setIndent(0)
        self.title_authentication.setObjectName("title_authentication")
        self.horizontalLayout_5.addWidget(self.title_authentication)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem1 = QtGui.QSpacerItem(1, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.frame_2 = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 26))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_4.addWidget(self.frame_2)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.main_layout.addLayout(self.horizontalLayout_5)
        self.auth_layout = QtGui.QHBoxLayout()
        self.auth_layout.setSpacing(10)
        self.auth_layout.setObjectName("auth_layout")
        self.checkbox_enable_store_auth = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkbox_enable_store_auth.sizePolicy().hasHeightForWidth())
        self.checkbox_enable_store_auth.setSizePolicy(sizePolicy)
        self.checkbox_enable_store_auth.setMinimumSize(QtCore.QSize(0, 65))
        self.checkbox_enable_store_auth.setChecked(True)
        self.checkbox_enable_store_auth.setObjectName("checkbox_enable_store_auth")
        self.auth_layout.addWidget(self.checkbox_enable_store_auth)
        self.button_reset_auth = QtGui.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_reset_auth.sizePolicy().hasHeightForWidth())
        self.button_reset_auth.setSizePolicy(sizePolicy)
        self.button_reset_auth.setMinimumSize(QtCore.QSize(0, 65))
        self.button_reset_auth.setObjectName("button_reset_auth")
        self.auth_layout.addWidget(self.button_reset_auth)
        self.main_layout.addLayout(self.auth_layout)
        self.sync_title_layout = QtGui.QHBoxLayout()
        self.sync_title_layout.setSpacing(10)
        self.sync_title_layout.setObjectName("sync_title_layout")
        self.sync_icon = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sync_icon.sizePolicy().hasHeightForWidth())
        self.sync_icon.setSizePolicy(sizePolicy)
        self.sync_icon.setMinimumSize(QtCore.QSize(48, 84))
        self.sync_icon.setText("")
        self.sync_icon.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.sync_icon.setObjectName("sync_icon")
        self.sync_title_layout.addWidget(self.sync_icon)
        self.title_sync = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_sync.sizePolicy().hasHeightForWidth())
        self.title_sync.setSizePolicy(sizePolicy)
        self.title_sync.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.title_sync.setIndent(0)
        self.title_sync.setObjectName("title_sync")
        self.sync_title_layout.addWidget(self.title_sync)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem2 = QtGui.QSpacerItem(1, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.frame_3 = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 26))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_5.addWidget(self.frame_3)
        self.sync_title_layout.addLayout(self.verticalLayout_5)
        self.main_layout.addLayout(self.sync_title_layout)
        self.label_2 = QtGui.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.main_layout.addWidget(self.label_2)
        self.sync_buttons_layout = QtGui.QHBoxLayout()
        self.sync_buttons_layout.setSpacing(10)
        self.sync_buttons_layout.setObjectName("sync_buttons_layout")
        self.main_layout.addLayout(self.sync_buttons_layout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkbox_only_wlan_sync = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.checkbox_only_wlan_sync.setMinimumSize(QtCore.QSize(0, 65))
        self.checkbox_only_wlan_sync.setObjectName("checkbox_only_wlan_sync")
        self.horizontalLayout_2.addWidget(self.checkbox_only_wlan_sync)
        self.button_sync_now = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.button_sync_now.setMinimumSize(QtCore.QSize(0, 65))
        self.button_sync_now.setObjectName("button_sync_now")
        self.horizontalLayout_2.addWidget(self.button_sync_now)
        self.main_layout.addLayout(self.horizontalLayout_2)
        self.sync_layout = QtGui.QHBoxLayout()
        self.sync_layout.setSpacing(10)
        self.sync_layout.setObjectName("sync_layout")
        self.checkbox_enable_sync = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkbox_enable_sync.sizePolicy().hasHeightForWidth())
        self.checkbox_enable_sync.setSizePolicy(sizePolicy)
        self.checkbox_enable_sync.setMinimumSize(QtCore.QSize(0, 65))
        self.checkbox_enable_sync.setObjectName("checkbox_enable_sync")
        self.sync_layout.addWidget(self.checkbox_enable_sync)
        self.main_layout.addLayout(self.sync_layout)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.sync_frame = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.sync_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.sync_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.sync_frame.setObjectName("sync_frame")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.sync_frame)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setMargin(15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_update_every = QtGui.QLabel(self.sync_frame)
        self.label_update_every.setEnabled(True)
        self.label_update_every.setMinimumSize(QtCore.QSize(0, 65))
        self.label_update_every.setObjectName("label_update_every")
        self.horizontalLayout.addWidget(self.label_update_every)
        self.spinbox_sync_interval = QtGui.QSpinBox(self.sync_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox_sync_interval.sizePolicy().hasHeightForWidth())
        self.spinbox_sync_interval.setSizePolicy(sizePolicy)
        self.spinbox_sync_interval.setMinimumSize(QtCore.QSize(0, 65))
        self.spinbox_sync_interval.setAlignment(QtCore.Qt.AlignCenter)
        self.spinbox_sync_interval.setMinimum(10)
        self.spinbox_sync_interval.setMaximum(120)
        self.spinbox_sync_interval.setObjectName("spinbox_sync_interval")
        self.horizontalLayout.addWidget(self.spinbox_sync_interval)
        self.label_min = QtGui.QLabel(self.sync_frame)
        self.label_min.setMinimumSize(QtCore.QSize(0, 65))
        self.label_min.setObjectName("label_min")
        self.horizontalLayout.addWidget(self.label_min)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_7.addWidget(self.sync_frame)
        self.main_layout.addLayout(self.horizontalLayout_7)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.main_layout.addItem(spacerItem3)
        self.horizontalLayout_3.addLayout(self.main_layout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.buttoon_layout = QtGui.QHBoxLayout()
        self.buttoon_layout.setSpacing(0)
        self.buttoon_layout.setContentsMargins(10, 0, 10, 10)
        self.buttoon_layout.setObjectName("buttoon_layout")
        self.button_cancel = QtGui.QPushButton(SettingsWidget)
        self.button_cancel.setMinimumSize(QtCore.QSize(0, 69))
        self.button_cancel.setObjectName("button_cancel")
        self.buttoon_layout.addWidget(self.button_cancel)
        self.button_save = QtGui.QPushButton(SettingsWidget)
        self.button_save.setMinimumSize(QtCore.QSize(0, 69))
        self.button_save.setObjectName("button_save")
        self.buttoon_layout.addWidget(self.button_save)
        self.verticalLayout.addLayout(self.buttoon_layout)

        self.retranslateUi(SettingsWidget)
        QtCore.QMetaObject.connectSlotsByName(SettingsWidget)

    def retranslateUi(self, SettingsWidget):
        SettingsWidget.setWindowTitle(QtGui.QApplication.translate("SettingsWidget", "DropN900 - Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.downloading_icon.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "padding-bottom: 2px;", None, QtGui.QApplication.UnicodeUTF8))
        self.title_download_folder.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QLabel#title_download_folder, #title_authentication, #title_sync {\n"
"    color: #0099FF;\n"
"    font-size: 20pt;\n"
"    padding-top: 40px;\n"
"    padding-bottom: 10px;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.title_download_folder.setText(QtGui.QApplication.translate("SettingsWidget", "Downloading", None, QtGui.QApplication.UnicodeUTF8))
        self.frame.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QFrame {\n"
"    border: 0px;\n"
"    border-top: 2px solid #0099FF;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QLabel {\n"
"    color: white;\n"
"    font-size: 19pt;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SettingsWidget", "Default Download Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.lineedit_default_download_folder.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QLineEdit {\n"
"    border: 1px solid gray;\n"
"    border-radius: 7px;\n"
"    padding: 5px;\n"
"    font-size: 19pt;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.button_browse_folder.setText(QtGui.QApplication.translate("SettingsWidget", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_no_dl_dialog.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QCheckBox {\n"
"    color: white;\n"
"    font-size: 19pt;\n"
"}\n"
"\n"
"QCheckBox::disabled {\n"
"    color: grey;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_no_dl_dialog.setText(QtGui.QApplication.translate("SettingsWidget", "Don\'t show dialog on download, always use default folder", None, QtGui.QApplication.UnicodeUTF8))
        self.authentication_icon.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "padding-bottom: 2px;", None, QtGui.QApplication.UnicodeUTF8))
        self.title_authentication.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QLabel#title_download_folder, #title_authentication, #title_sync {\n"
"    color: #0099FF;\n"
"    font-size: 20pt;\n"
"    padding-top: 40px;\n"
"    padding-bottom: 10px;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.title_authentication.setText(QtGui.QApplication.translate("SettingsWidget", "Authentication", None, QtGui.QApplication.UnicodeUTF8))
        self.frame_2.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QFrame {\n"
"    border: 0px;\n"
"    border-top: 2px solid #0099FF;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_enable_store_auth.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QCheckBox {\n"
"    color: white;\n"
"    font-size: 19pt;\n"
"}\n"
"\n"
"QCheckBox::disabled {\n"
"    color: grey;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_enable_store_auth.setText(QtGui.QApplication.translate("SettingsWidget", "Store for next sessions", None, QtGui.QApplication.UnicodeUTF8))
        self.button_reset_auth.setText(QtGui.QApplication.translate("SettingsWidget", "Reset Current Authentication", None, QtGui.QApplication.UnicodeUTF8))
        self.sync_icon.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "padding-bottom: 2px;", None, QtGui.QApplication.UnicodeUTF8))
        self.title_sync.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QLabel#title_download_folder, #title_authentication, #title_sync {\n"
"    color: #0099FF;\n"
"    font-size: 20pt;\n"
"    padding-top: 40px;\n"
"    padding-bottom: 10px;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.title_sync.setText(QtGui.QApplication.translate("SettingsWidget", "Synchronizing", None, QtGui.QApplication.UnicodeUTF8))
        self.frame_3.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QFrame {\n"
"    border: 0px;\n"
"    border-top: 2px solid #0099FF;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "color: white;", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SettingsWidget", "In order to select sync path you first need to be connected with a DropBox account. Secondly you need to have traveled to the desired path in the content view. The selection tool will be populated with the current sessions metadata. This is the only way to be sure that the sync location is valid.", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_only_wlan_sync.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QCheckBox {\n"
"    color: white;\n"
"    font-size: 19pt;\n"
"}\n"
"\n"
"QCheckBox::disabled {\n"
"    color: grey;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_only_wlan_sync.setText(QtGui.QApplication.translate("SettingsWidget", "Only sync while on WLAN", None, QtGui.QApplication.UnicodeUTF8))
        self.button_sync_now.setText(QtGui.QApplication.translate("SettingsWidget", "Sync Folder Now", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_enable_sync.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QCheckBox {\n"
"    color: white;\n"
"    font-size: 19pt;\n"
"}\n"
"\n"
"QCheckBox::disabled {\n"
"    color: grey;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_enable_sync.setText(QtGui.QApplication.translate("SettingsWidget", "Enable automated sync", None, QtGui.QApplication.UnicodeUTF8))
        self.sync_frame.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QFrame#sync_frame {\n"
"    background-color: transparent;\n"
"    border: 2px solid rgba(255,255,255,150);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QFrame:disabled#sync_frame {\n"
"    border: 2px solid rgba(255,255,255,70);\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.label_update_every.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QLabel {\n"
"    color: white;\n"
"    font-size: 19pt;\n"
"}\n"
"\n"
"QLabel::disabled {\n"
"    color: grey;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.label_update_every.setText(QtGui.QApplication.translate("SettingsWidget", "Sync folder every", None, QtGui.QApplication.UnicodeUTF8))
        self.label_min.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QLabel {\n"
"    color: white;\n"
"    font-size: 19pt;\n"
"}\n"
"\n"
"QLabel::disabled {\n"
"    color: grey;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.label_min.setText(QtGui.QApplication.translate("SettingsWidget", "minutes", None, QtGui.QApplication.UnicodeUTF8))
        self.button_cancel.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QPushButton#button_cancel, #button_save {\n"
"    min-height: 65px;\n"
"    border-radius: 0px;\n"
"    border: 2px solid rgba(255,255,255,200);\n"
"    color: rgb(230, 230, 230);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(16, 16, 16, 255), stop:0.5 rgba(55, 55, 55, 210), stop:1 rgba(36, 36, 36, 255));\n"
"    font: Arial;\n"
"    font-size: 19pt;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton#button_cancel {\n"
"    border-top-left-radius: 10px;\n"
"    border-bottom-left-radius: 10px;\n"
"    border-right: 0px;\n"
"}\n"
"\n"
"QPushButton#button_save {\n"
"    border-top-right-radius: 10px;\n"
"    border-bottom-right-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:pressed#button_cancel, :pressed#button_save {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(59, 59, 59, 255), stop:0.5 rgba(82, 82, 82, 255), stop:1 rgba(68, 68, 68, 255));\n"
"    color: #0099FF;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.button_cancel.setText(QtGui.QApplication.translate("SettingsWidget", "CANCEL", None, QtGui.QApplication.UnicodeUTF8))
        self.button_save.setStyleSheet(QtGui.QApplication.translate("SettingsWidget", "QPushButton#button_cancel, #button_save {\n"
"    min-height: 65px;\n"
"    border-radius: 0px;\n"
"    border: 2px solid rgba(255,255,255,200);\n"
"    color: rgb(230, 230, 230);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(16, 16, 16, 255), stop:0.5 rgba(55, 55, 55, 210), stop:1 rgba(36, 36, 36, 255));\n"
"    font: Arial;\n"
"    font-size: 19pt;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton#button_cancel {\n"
"    border-top-left-radius: 10px;\n"
"    border-bottom-left-radius: 10px;\n"
"    border-right: 0px;\n"
"}\n"
"\n"
"QPushButton#button_save {\n"
"    border-top-right-radius: 10px;\n"
"    border-bottom-right-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:pressed#button_cancel, :pressed#button_save {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(59, 59, 59, 255), stop:0.5 rgba(82, 82, 82, 255), stop:1 rgba(68, 68, 68, 255));\n"
"    color: #0099FF;\n"
"}", None, QtGui.QApplication.UnicodeUTF8))
        self.button_save.setText(QtGui.QApplication.translate("SettingsWidget", "SAVE CHANGES", None, QtGui.QApplication.UnicodeUTF8))

