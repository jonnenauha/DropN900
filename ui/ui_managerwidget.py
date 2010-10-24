# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'managerwidget.ui'
#
# Created: Sun Oct 24 22:18:58 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ManagerWidget(object):
    def setupUi(self, ManagerWidget):
        ManagerWidget.setObjectName("ManagerWidget")
        ManagerWidget.resize(800, 474)
        ManagerWidget.setMaximumSize(QtCore.QSize(800, 16777215))
        ManagerWidget.setStyleSheet("QFrame#frame_controls_bottom, #frame_controls_right {\n"
"    background: black;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #0099FF;\n"
"}\n"
"\n"
"QLabel#thumb_container {\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QPushButton {\n"
"    min-height: 60px;\n"
"    border-radius: 0px;\n"
"    border: 2px solid rgba(255,255,255,200);\n"
"    border-left: 0px;\n"
"    color: rgb(230, 230, 230);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(16, 16, 16, 255), stop:0.5 rgba(55, 55, 55, 210), stop:1 rgba(36, 36, 36, 255));\n"
"    font-size: 16pt;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(59, 59, 59, 255), stop:0.5 rgba(82, 82, 82, 255), stop:1 rgba(68, 68, 68, 255));\n"
"    color: #0099FF;\n"
"}\n"
"\n"
"QPushButton::disabled {\n"
"    color: grey;\n"
"    background-color: black;\n"
"}\n"
"\n"
"QPushButton#button_download {\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"}\n"
"\n"
"QPushButton#button_new_folder, #button_open_public_link {\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 15px;\n"
"}\n"
"\n"
"QPushButton#button_remove {\n"
"    border-top: 0px;\n"
"    border-right: 0px;\n"
"}\n"
"\n"
"QPushButton#button_rename, #button_new_folder, #button_upload, #button_copy_public_link, #button_open_public_link {\n"
"    border-top: 0px;\n"
"}\n"
"\n"
"QPushButton#button_rename {\n"
"    border-left: 2px solid rgba(255,255,255,200);\n"
"}\n"
"\n"
"QTreeWidget {\n"
"    show-decoration-selected: 1;\n"
"    background-color: black;\n"
"    alternate-background-color: rgb(36, 36, 36);\n"
"    color: rgb(235, 235, 235);\n"
"    font-size: 15pt;\n"
"    border: 0px;\n"
"    border-bottom: 2px solid rgba(255,255,255,200);\n"
"    border-right: 2px solid rgba(255,255,255,200);\n"
"    border-top: 2px solid rgba(255,255,255,200);\n"
"    border-bottom-right-radius: 15px;\n"
"    padding-bottom: 15px;\n"
"}\n"
"\n"
"QTreeWidget::item {\n"
"    background-color: transparent;\n"
"    border: 0px;\n"
"    height: 70px;\n"
"    min-height: 70px;\n"
"    max-height: 70px;\n"
"    padding-left: 5px;\n"
"}\n"
"\n"
"QTreeView::item:selected {\n"
"    background-color: #404040;\n"
"    border: 0px;\n"
"}\n"
"\n"
"QTreeView::branch {\n"
"    border: 0px;\n"
"}\n"
"\n"
"QTreeView::branch:selected {\n"
"    background-color: #404040;\n"
"    border: 0px;\n"
"}\n"
"\n"
"QTreeView::branch:has-siblings:!adjoins-item {\n"
"    border-image: url(/opt/dropn900/ui/images/vline.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:has-siblings:adjoins-item {\n"
"    border-image: url(/opt/dropn900/ui/images/hmid.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:!has-children:!has-siblings:adjoins-item {\n"
"    border-image: url(/opt/dropn900/ui/images/hend.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:has-children:!has-siblings:closed {\n"
"    border-image: none;\n"
"    image: url(/opt/dropn900/ui/images/arrow_right_small.png);\n"
"}\n"
"\n"
"QTreeView::branch:closed:has-children:has-siblings {\n"
"    border-image: url(/opt/dropn900/ui/images/vline-cap.png) 0;\n"
"    image: url(/opt/dropn900/ui/images/arrow_right_small.png);\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:!has-siblings {\n"
"    border-image: none;\n"
"    image: url(/opt/dropn900/ui/images/arrow_down_small.png);\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:has-siblings  {\n"
"    border-image: url(/opt/dropn900/ui/images/vline-cap.png) 0;\n"
"    image: url(/opt/dropn900/ui/images/arrow_down_small.png);\n"
"}")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(ManagerWidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tree_widget = QtGui.QTreeWidget(ManagerWidget)
        self.tree_widget.setMaximumSize(QtCore.QSize(500, 16777215))
        self.tree_widget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.tree_widget.setFrameShadow(QtGui.QFrame.Sunken)
        self.tree_widget.setLineWidth(1)
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setIndentation(25)
        self.tree_widget.setUniformRowHeights(True)
        self.tree_widget.setAnimated(True)
        self.tree_widget.setObjectName("tree_widget")
        self.tree_widget.header().setVisible(True)
        self.tree_widget.header().setDefaultSectionSize(380)
        self.tree_widget.header().setMinimumSectionSize(40)
        self.verticalLayout.addWidget(self.tree_widget)
        self.frame_controls_bottom = QtGui.QFrame(ManagerWidget)
        self.frame_controls_bottom.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_controls_bottom.setLineWidth(0)
        self.frame_controls_bottom.setObjectName("frame_controls_bottom")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame_controls_bottom)
        self.verticalLayout_3.setContentsMargins(8, 8, 0, 8)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.selected_icon_label = QtGui.QLabel(self.frame_controls_bottom)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selected_icon_label.sizePolicy().hasHeightForWidth())
        self.selected_icon_label.setSizePolicy(sizePolicy)
        self.selected_icon_label.setMinimumSize(QtCore.QSize(24, 24))
        self.selected_icon_label.setMaximumSize(QtCore.QSize(24, 24))
        self.selected_icon_label.setText("")
        self.selected_icon_label.setObjectName("selected_icon_label")
        self.horizontalLayout_4.addWidget(self.selected_icon_label)
        self.selected_name_label = QtGui.QLabel(self.frame_controls_bottom)
        self.selected_name_label.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.selected_name_label.setFont(font)
        self.selected_name_label.setText("")
        self.selected_name_label.setObjectName("selected_name_label")
        self.horizontalLayout_4.addWidget(self.selected_name_label)
        spacerItem = QtGui.QSpacerItem(40, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.modified_label = QtGui.QLabel(self.frame_controls_bottom)
        self.modified_label.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.modified_label.setFont(font)
        self.modified_label.setText("")
        self.modified_label.setObjectName("modified_label")
        self.horizontalLayout_4.addWidget(self.modified_label)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addWidget(self.frame_controls_bottom)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.frame_controls_right = QtGui.QFrame(ManagerWidget)
        self.frame_controls_right.setMinimumSize(QtCore.QSize(300, 0))
        self.frame_controls_right.setMaximumSize(QtCore.QSize(275, 16777215))
        self.frame_controls_right.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_controls_right.setLineWidth(0)
        self.frame_controls_right.setObjectName("frame_controls_right")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame_controls_right)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 8)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.button_download = QtGui.QPushButton(self.frame_controls_right)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.button_download.setFont(font)
        self.button_download.setStyleSheet("None")
        self.button_download.setObjectName("button_download")
        self.verticalLayout_2.addWidget(self.button_download)
        self.layout_buttons = QtGui.QHBoxLayout()
        self.layout_buttons.setSpacing(0)
        self.layout_buttons.setObjectName("layout_buttons")
        self.button_remove = QtGui.QPushButton(self.frame_controls_right)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.button_remove.setFont(font)
        self.button_remove.setObjectName("button_remove")
        self.layout_buttons.addWidget(self.button_remove)
        self.button_rename = QtGui.QPushButton(self.frame_controls_right)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.button_rename.setFont(font)
        self.button_rename.setObjectName("button_rename")
        self.layout_buttons.addWidget(self.button_rename)
        self.verticalLayout_2.addLayout(self.layout_buttons)
        self.button_upload = QtGui.QPushButton(self.frame_controls_right)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.button_upload.setFont(font)
        self.button_upload.setObjectName("button_upload")
        self.verticalLayout_2.addWidget(self.button_upload)
        self.button_new_folder = QtGui.QPushButton(self.frame_controls_right)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.button_new_folder.setFont(font)
        self.button_new_folder.setObjectName("button_new_folder")
        self.verticalLayout_2.addWidget(self.button_new_folder)
        self.button_copy_public_link = QtGui.QPushButton(self.frame_controls_right)
        self.button_copy_public_link.setMinimumSize(QtCore.QSize(70, 62))
        self.button_copy_public_link.setObjectName("button_copy_public_link")
        self.verticalLayout_2.addWidget(self.button_copy_public_link)
        self.button_open_public_link = QtGui.QPushButton(self.frame_controls_right)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.button_open_public_link.setFont(font)
        self.button_open_public_link.setObjectName("button_open_public_link")
        self.verticalLayout_2.addWidget(self.button_open_public_link)
        self.action_layout = QtGui.QVBoxLayout()
        self.action_layout.setSpacing(0)
        self.action_layout.setContentsMargins(8, -1, 8, -1)
        self.action_layout.setObjectName("action_layout")
        spacerItem1 = QtGui.QSpacerItem(1, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.action_layout.addItem(spacerItem1)
        self.thumb_container = QtGui.QLabel(self.frame_controls_right)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thumb_container.sizePolicy().hasHeightForWidth())
        self.thumb_container.setSizePolicy(sizePolicy)
        self.thumb_container.setLineWidth(0)
        self.thumb_container.setText("")
        self.thumb_container.setAlignment(QtCore.Qt.AlignCenter)
        self.thumb_container.setObjectName("thumb_container")
        self.action_layout.addWidget(self.thumb_container)
        spacerItem2 = QtGui.QSpacerItem(1, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.action_layout.addItem(spacerItem2)
        spacerItem3 = QtGui.QSpacerItem(1, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.action_layout.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.action_layout)
        self.layout_user_info = QtGui.QHBoxLayout()
        self.layout_user_info.setSpacing(8)
        self.layout_user_info.setContentsMargins(8, -1, 8, -1)
        self.layout_user_info.setObjectName("layout_user_info")
        spacerItem4 = QtGui.QSpacerItem(1, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layout_user_info.addItem(spacerItem4)
        self.label_username = QtGui.QLabel(self.frame_controls_right)
        self.label_username.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_username.setFont(font)
        self.label_username.setText("")
        self.label_username.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_username.setWordWrap(True)
        self.label_username.setObjectName("label_username")
        self.layout_user_info.addWidget(self.label_username)
        self.label_username_icon = QtGui.QLabel(self.frame_controls_right)
        self.label_username_icon.setMinimumSize(QtCore.QSize(24, 24))
        self.label_username_icon.setMaximumSize(QtCore.QSize(24, 16777215))
        self.label_username_icon.setText("")
        self.label_username_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.label_username_icon.setObjectName("label_username_icon")
        self.layout_user_info.addWidget(self.label_username_icon)
        self.sync_button = QtGui.QPushButton(self.frame_controls_right)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sync_button.sizePolicy().hasHeightForWidth())
        self.sync_button.setSizePolicy(sizePolicy)
        self.sync_button.setMinimumSize(QtCore.QSize(0, 14))
        self.sync_button.setMaximumSize(QtCore.QSize(16777215, 35))
        self.sync_button.setStyleSheet("QPushButton#sync_button {\n"
"    min-height: 0px;\n"
"    border: 1px solid #0099FF; \n"
"    border-radius: 3px;\n"
"    color: rgb(230, 230, 230);\n"
"    font-size: 14pt;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton#sync_button::pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(59, 59, 59, 255), stop:0.5 rgba(82, 82, 82, 255), stop:1 rgba(68, 68, 68, 255));\n"
"    color: #0099FF;\n"
"}")
        self.sync_button.setObjectName("sync_button")
        self.layout_user_info.addWidget(self.sync_button)
        self.sync_label = QtGui.QLabel(self.frame_controls_right)
        self.sync_label.setMinimumSize(QtCore.QSize(0, 30))
        self.sync_label.setMaximumSize(QtCore.QSize(16777215, 35))
        self.sync_label.setStyleSheet("color: white; font-size: 14pt; padding-left: 6px; padding-right: 6px; border: 1px solid #0099FF; border-radius: 3px;")
        self.sync_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sync_label.setWordWrap(True)
        self.sync_label.setObjectName("sync_label")
        self.layout_user_info.addWidget(self.sync_label)
        self.verticalLayout_2.addLayout(self.layout_user_info)
        self.horizontalLayout_2.addWidget(self.frame_controls_right)

        self.retranslateUi(ManagerWidget)
        QtCore.QMetaObject.connectSlotsByName(ManagerWidget)

    def retranslateUi(self, ManagerWidget):
        ManagerWidget.setWindowTitle(QtGui.QApplication.translate("ManagerWidget", "ManagerWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.tree_widget.headerItem().setText(0, QtGui.QApplication.translate("ManagerWidget", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.tree_widget.headerItem().setText(1, QtGui.QApplication.translate("ManagerWidget", "Size", None, QtGui.QApplication.UnicodeUTF8))
        self.button_download.setText(QtGui.QApplication.translate("ManagerWidget", "DOWNLOAD", None, QtGui.QApplication.UnicodeUTF8))
        self.button_remove.setText(QtGui.QApplication.translate("ManagerWidget", "REMOVE", None, QtGui.QApplication.UnicodeUTF8))
        self.button_rename.setText(QtGui.QApplication.translate("ManagerWidget", "RENAME", None, QtGui.QApplication.UnicodeUTF8))
        self.button_upload.setText(QtGui.QApplication.translate("ManagerWidget", "UPLOAD FILE", None, QtGui.QApplication.UnicodeUTF8))
        self.button_new_folder.setText(QtGui.QApplication.translate("ManagerWidget", "NEW FOLDER", None, QtGui.QApplication.UnicodeUTF8))
        self.button_copy_public_link.setText(QtGui.QApplication.translate("ManagerWidget", "COPY PUBLIC LINK", None, QtGui.QApplication.UnicodeUTF8))
        self.button_open_public_link.setText(QtGui.QApplication.translate("ManagerWidget", "OPEN PUBLIC LINK", None, QtGui.QApplication.UnicodeUTF8))
        self.sync_button.setText(QtGui.QApplication.translate("ManagerWidget", "SYNC NOW", None, QtGui.QApplication.UnicodeUTF8))
        self.sync_label.setText(QtGui.QApplication.translate("ManagerWidget", "SYNCHRONIZING", None, QtGui.QApplication.UnicodeUTF8))

