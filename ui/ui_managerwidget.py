# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'managerwidget.ui'
#
# Created: Thu Jul 29 04:43:23 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ManagerWidget(object):
    def setupUi(self, ManagerWidget):
        ManagerWidget.setObjectName("ManagerWidget")
        ManagerWidget.resize(800, 562)
        ManagerWidget.setMaximumSize(QtCore.QSize(800, 16777215))
        ManagerWidget.setStyleSheet("""QFrame#frame_controls_bottom, #frame_controls_right {
    background: black;
}

QLabel {
    color: #0099FF;
}

QLabel#thumb_container {
    background-color: transparent;
}

QPushButton {
    min-height: 60px;
    border-radius: 0px;
    border: 2px solid rgba(255,255,255,200);
    border-left: 0px;
    color: rgb(230, 230, 230);
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(16, 16, 16, 255), stop:0.5 rgba(55, 55, 55, 210), stop:1 rgba(36, 36, 36, 255));
    font-size: 16pt;
}

QPushButton:hover {
    color: white;
}

QPushButton:pressed {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(59, 59, 59, 255), stop:0.5 rgba(82, 82, 82, 255), stop:1 rgba(68, 68, 68, 255));
    color: #0099FF;
}

QPushButton::disabled {
    color: grey;
    background-color: black;
}

QPushButton#button_download {
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}

QPushButton#button_new_folder, #button_open_public_link {
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 15px;
}

QPushButton#button_remove {
    border-top: 0px;
    border-right: 0px;
}

QPushButton#button_rename, #button_new_folder, #button_upload, #button_copy_public_link, #button_open_public_link {
    border-top: 0px;
}

QPushButton#button_rename {
    border-left: 2px solid rgba(255,255,255,200);
}

QTreeWidget {
    show-decoration-selected: 1;
    background-color: black;
    alternate-background-color: rgb(36, 36, 36);
    color: rgb(235, 235, 235);
    font-size: 17px;
    border: 0px;
    border-bottom: 2px solid rgba(255,255,255,200);
    border-right: 2px solid rgba(255,255,255,200);
    border-top: 2px solid rgba(255,255,255,200);
    border-bottom-right-radius: 15px;
    padding-bottom: 15px;
}

QTreeWidget::item {
    background-color: transparent;
    border: 0px;
    height: 60px;
    min-height: 60px;
    max-height: 60px;
    padding-left: 5px;
}

QTreeView::item:selected {
    background-color: #404040;
    border: 0px;
}

QTreeView::branch {
    border: 0px;
}

QTreeView::branch:selected {
    background-color: #404040;
    border: 0px;
}

QTreeView::branch:has-siblings:!adjoins-item {
    border-image: url(/opt/dropn900/ui/images/vline.png) 0;
}

QTreeView::branch:has-siblings:adjoins-item {
    border-image: url(/opt/dropn900/ui/images/hmid.png) 0;
}

QTreeView::branch:!has-children:!has-siblings:adjoins-item {
    border-image: url(/opt/dropn900/ui/images/hend.png) 0;
}

QTreeView::branch:has-children:!has-siblings:closed {
    border-image: none;
    image: url(/opt/dropn900/ui/images/arrow_right_small.png);
}

QTreeView::branch:closed:has-children:has-siblings {
    border-image: url(/opt/dropn900/ui/images/vline-cap.png) 0;
    image: url(/opt/dropn900/ui/images/arrow_right_small.png);
}

QTreeView::branch:open:has-children:!has-siblings {
    border-image: none;
    image: url(/opt/dropn900/ui/images/arrow_down_small.png);
}

QTreeView::branch:open:has-children:has-siblings  {
    border-image: url(/opt/dropn900/ui/images/vline-cap.png) 0;
    image: url(/opt/dropn900/ui/images/arrow_down_small.png);
}""")
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
        self.selected_icon_label.setObjectName("selected_icon_label")
        self.horizontalLayout_4.addWidget(self.selected_icon_label)
        self.selected_name_label = QtGui.QLabel(self.frame_controls_bottom)
        self.selected_name_label.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.selected_name_label.setFont(font)
        self.selected_name_label.setObjectName("selected_name_label")
        self.horizontalLayout_4.addWidget(self.selected_name_label)
        spacerItem = QtGui.QSpacerItem(40, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.modified_label = QtGui.QLabel(self.frame_controls_bottom)
        self.modified_label.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.modified_label.setFont(font)
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
        font.setFamily("Arial")
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
        self.label_username.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_username.setFont(font)
        self.label_username.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_username.setObjectName("label_username")
        self.layout_user_info.addWidget(self.label_username)
        self.label_username_icon = QtGui.QLabel(self.frame_controls_right)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_username_icon.sizePolicy().hasHeightForWidth())
        self.label_username_icon.setSizePolicy(sizePolicy)
        self.label_username_icon.setMinimumSize(QtCore.QSize(24, 24))
        self.label_username_icon.setMaximumSize(QtCore.QSize(24, 24))
        self.label_username_icon.setObjectName("label_username_icon")
        self.layout_user_info.addWidget(self.label_username_icon)
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

