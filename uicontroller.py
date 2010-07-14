
import time
import os

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, QStringList, QTimer
from PyQt4.QtGui import QMainWindow, QWidget, QTreeWidgetItem, QDesktopServices
from PyQt4.QtGui import QImage, QPixmap, QIcon, QImageReader, QMovie
from PyQt4.QtGui import QInputDialog, QFileDialog, QMessageBox
from PyQt4.QtNetwork import QNetworkReply, QNetworkRequest

from ui.ui_mainwindow import Ui_DropN900Widget
from ui.ui_login import Ui_LoginWidget
from ui.ui_manager import Ui_ManagerWidget
from ui.ui_console import Ui_ConsoleWidget
from ui.ui_loadingwidget import Ui_LoadingWidget

""" UiController controls ui view switching and ui interactions """

class UiController:

    def __init__(self, controller, debug_mode = False):
        self.controller = controller
        self.debug_mode = debug_mode

        ### Main Window
        self.main_widget = QMainWindow()
        self.main_ui = Ui_DropN900Widget()
        self.main_ui.setupUi(self.main_widget)

        # Stacked layout for context switching
        self.stacked_layout = QtGui.QStackedLayout()
        self.main_ui.centralwidget.setLayout(self.stacked_layout)

        # Menu items
        self.action_console = QtGui.QAction("Show Console", self.main_widget)
        action_reset_auth = QtGui.QAction("Reset Auth", self.main_widget)
        action_exit = QtGui.QAction("Exit", self.main_widget)

        self.main_ui.menubar.addAction(self.action_console)
        self.main_ui.menubar.addAction(action_reset_auth)
        self.main_ui.menubar.addAction(action_exit)

        # Connects
        self.action_console.triggered.connect(self.show_console)
        action_reset_auth.triggered.connect(self.controller.reset_auth)
        action_exit.triggered.connect(self.shut_down)
        
        ### Login Widget
        self.login_widget = QWidget()
        self.login_ui = Ui_LoginWidget()
        self.login_ui.setupUi(self.login_widget)

        # Connects
        self.login_ui.button_done.clicked.connect(self.browser_control_clicked)
        self.login_ui.url_line_edit.returnPressed.connect(self.webview_load_url)
        self.login_ui.webview.loadStarted.connect(self.webview_load_started)
        self.login_ui.webview.loadProgress.connect(self.webview_load_progress)
        self.login_ui.webview.loadFinished.connect(self.webview_load_finished)
        
        network_manager = self.login_ui.webview.page().networkAccessManager()
        network_manager.sslErrors.connect(self.ssl_errors_occurred)
        network_manager.finished.connect(self.load_reply_recieved)

        ### Manager Widget
        self.manager_widget = QWidget()
        self.manager_ui = Ui_ManagerWidget()
        self.manager_ui.setupUi(self.manager_widget)

        tree = self.manager_ui.tree_widget
        self.tree_controller = TreeController(tree, self.manager_ui, self.controller.log)

        # Hide public link elements (not used yet)
        self.manager_ui.public_link_line_edit.hide()
        self.manager_ui.button_open_public_link.hide()
        
        # Connects
        self.manager_ui.button_open_public_link.clicked.connect(self.open_item_link)
        self.manager_ui.button_download.clicked.connect(self.item_download)
        self.manager_ui.button_upload.clicked.connect(self.item_upload)
        self.manager_ui.button_rename.clicked.connect(self.item_rename)
        self.manager_ui.button_remove.clicked.connect(self.item_remove)
        self.manager_ui.button_new_folder.clicked.connect(self.item_new_folder)

        ### Fill stacked layout
        self.stacked_layout.addWidget(self.login_widget)
        self.stacked_layout.addWidget(self.manager_widget)

        ### Console widget
        if self.debug_mode:
            self.console_widget = QWidget()
            self.console_ui = Ui_ConsoleWidget()
            self.console_ui.setupUi(self.console_widget)
            self.console_ui.button_back.clicked.connect(self.hide_console)
            self.stacked_layout.addWidget(self.console_widget)

        ### Loading Widget
        self.loading_widget = QWidget(self.manager_widget)
        self.loading_ui = Ui_LoadingWidget()
        self.loading_ui.setupUi(self.loading_widget)
        self.manager_ui.action_layout.insertWidget(3, self.loading_widget)
        self.loading_widget.hide()

        # Init loading animation
        self.loading_animation = QMovie("ui/images/loading.gif", "GIF", self.loading_ui.load_animation_label)
        self.loading_animation.setCacheMode(QMovie.CacheAll)
        self.loading_animation.setSpeed(150)
        self.loading_animation.setScaledSize(QtCore.QSize(48,48))
        self.loading_ui.load_animation_label.setMovie(self.loading_animation)

        # Init hide timer and icons for information messages
        self.information_message_timer = QTimer()
        self.information_message_timer.setSingleShot(True)
        self.information_message_timer.timeout.connect(self.hide_information_message)
        self.information_icon_ok = QPixmap("ui/icons/check.png").scaled(24,24)
        self.information_icon_error = QPixmap("ui/icons/cancel.png").scaled(24,24)

        self.log("UI initialised...")

    def show(self):
        # Nokia N900 screen resolution, full screen
        self.main_widget.resize(800, 480) 
        self.main_widget.show()

    def show_loading_ui(self, message = "", loading = True):
        self.loading_ui.info_label.setText(message)
        self.loading_ui.info_label_icon.hide()
        self.thumb_was_visible = self.manager_ui.thumb_container.isVisible()
        self.manager_ui.thumb_container.hide()
        self.loading_widget.show()

        self.loading_ui.load_animation_label.setVisible(loading)
        if loading:
            self.loading_animation.start()
        else:
            self.loading_animation.stop()

    def show_information_ui(self, message, succesfull):
        self.loading_ui.load_animation_label.hide()
        self.loading_ui.info_label.setText(message)
        if succesfull:
            icon = self.information_icon_ok
        else:
            icon = self.information_icon_error
        self.loading_ui.info_label_icon.setPixmap(icon)
        self.loading_ui.info_label_icon.show()
        self.loading_widget.show()
        self.information_message_timer.start(4000)

    def hide_loading_ui(self):
        if not self.information_message_timer.isActive():
            self.loading_widget.hide()
        if self.loading_animation.state() == QMovie.Running:
            self.loading_animation.stop()

    def hide_information_message(self):
        self.loading_ui.info_label_icon.hide()
        self.hide_loading_ui()
        self.manager_ui.thumb_container.setVisible(self.thumb_was_visible)

    def load_login(self, authurl):
        self.switch_context("browser")
        self.login_ui.url_line_edit.setText(QtCore.QUrl(authurl).toString())        
        self.webview_load_url()

    def switch_context(self, view = None):
        widget = None
        if view == "browser":
            widget = self.login_widget
        if view == "manager":
            widget = self.manager_widget
        if view == "console":
            widget = self.console_widget
        if view == None and self.last_view != None:
            widget = self.last_view
        if widget != None:
            self.last_view = self.stacked_layout.currentWidget()
            self.stacked_layout.setCurrentWidget(widget)
    
    def log(self, msg):
        if self.debug_mode:
            timestamp = "%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
            stamp_mgs = "%s %s" % (timestamp, msg)
            self.console_ui.text_area.appendPlainText(stamp_mgs)
            print "%s [DropN900]: %s" % (timestamp, msg)

    def get_selected_data(self):
        return self.tree_controller.selected_data
    
    # Signal handlers
            
    def shut_down(self):
        self.log("Shutting down...")
        self.main_widget.close()

    def show_console(self):
        if not self.debug_mode:
            return
        if self.action_console.text() == "Show Console":
            self.action_console.setText("Hide Console")
            self.switch_context("console")
        else:
            self.hide_console()
        
    def hide_console(self):
        if not self.debug_mode:
            return
        self.action_console.setText("Show Console")
        self.stacked_layout.setCurrentWidget(self.last_view)

    # We should not end here in the device as it has ssl libs in place
    # on windows youll have to have openssl libs in place or login via webauth wont work
    def ssl_errors_occurred(self, reply, errors):
        self.controller.log("NETWORK ERROR - SSL errors while loading", reply.url())
        print ">> SSL ERRORS LIST: ", errors
        
    def webview_load_url(self, url = None):
        if url == None:
            url = QtCore.QUrl(self.login_ui.url_line_edit.text())
        else:
            url = QtCore.QUrl(url)
        self.login_ui.webview.load(url)

    def webview_load_started(self):
        self.login_ui.webview_status_label.setText("Loading...")

    def webview_load_progress(self, progress):
        self.login_ui.webview_status_label.setText("Loading... " + str(progress) + "%")
        
    def webview_load_finished(self, succesfull):
        if succesfull:
            status = "Page loaded"
        else:
            status = "Page load failed"
        self.login_ui.webview_status_label.setText(status)
        self.login_ui.url_line_edit.setText(self.login_ui.webview.url().toString())

    def load_reply_recieved(self, reply):
        attr_redir = reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
        if not attr_redir.isNull():
            self.login_ui.webview_status_label.setText("Redirecting...")
        if reply.error() != 0:
            self.controller.log("NETWORK ERROR - Errors occurred while loading page:", reply.errorString())
            self.controller.log(">> Error code", str(reply.error()))
        #if reply.error() == 99:
            #reply.ignoreSslErrors()

    def browser_control_clicked(self):
        if self.controller.connected:
            self.switch_context()
        else:
            self.controller.end_auth()
            
    def open_item_link(self):
        url = self.manager_ui.public_link_line_edit.text()
        self.webview_load_url(url)
        self.login_ui.label_info.hide()
        self.login_ui.button_done.setText("Back")
        self.login_ui.button_done.setIcon(QIcon("ui/icons/back.png"))
        self.switch_context("browser")

    def item_download(self):
        data = self.get_selected_data()
        if data == None:
            return

        # This dialog shows strange stuff on maemo5
        # It's a PyQt4 bug and its the best we got, you can cope with this
        local_folder_path = QFileDialog.getExistingDirectory(None, "Select Download Folder", "/home/user", QFileDialog.ShowDirsOnly|QFileDialog.HideNameFilterDetails|QFileDialog.ReadOnly)
        if local_folder_path.isEmpty():
            return
        
        store_path = local_folder_path + "/" + data.name
        self.controller.connection.get_file(data.path, data.root, str(store_path))
        
    def item_upload(self):
        data = self.get_selected_data()
        if data == None or not data.is_folder():
            return

        # This dialog shows strange stuff on maemo5
        # It's a PyQt4 bug and its the best we got, you can cope with this
        local_file_path = QFileDialog.getOpenFileName(self.manager_widget, "Select File for Upload", "/home/user")
        if local_file_path.isEmpty():
            return

        self.controller.connection.upload_file(data.path, data.root, str(local_file_path))
        
    def item_rename(self):
        data = self.get_selected_data()
        if data == None:
            return
        old_name = data.get_name()
        keyword = "file" if not data.is_folder() else "folder"
        new_name, ok = QInputDialog.getText(None, "Renaming " + keyword, "Give new name for " + keyword + " " + old_name, QtGui.QLineEdit.Normal, old_name)
        if not ok:
            return
        if new_name.isEmpty() or new_name.isNull():
            return
        if new_name.contains("/") or new_name == " ":
            return

        q_old_name = QtCore.QString(old_name)
        if q_old_name.contains("."):
            if not new_name.contains("."):
                format = old_name[q_old_name.lastIndexOf("."):]
                confirmation = QMessageBox.question(None, "Extension missing", "Do you want to append the original '" + format + "' extensions to the filename '" + new_name + "'?", QMessageBox.Yes, QMessageBox.No)
                if confirmation == QMessageBox.Yes:
                    new_name.append(format)

        if data.parent == "/":
            new_name = data.parent + new_name
        else:
            new_name = data.parent + "/" + new_name
        self.controller.connection.rename(data.root, data.path, str(new_name), data.parent)
        
    def item_remove(self):
        data = self.get_selected_data()
        if data == None:
            return
        if data.is_folder():
            confirmation = QMessageBox.question(None, "Remove folder verification", "Are you sure you want to remove the entire folder " + data.get_name() +"?", QMessageBox.Yes, QMessageBox.Cancel)
        else:
            confirmation = QMessageBox.question(None, "Remove file verification", "Are you sure you want to remove " + data.get_name() +"?", QMessageBox.Yes, QMessageBox.Cancel)            
        if confirmation == QMessageBox.Yes:
            self.controller.connection.remove_file(data.root, data.path, data.parent, data.is_folder())
        
    def item_new_folder(self):
        data = self.get_selected_data()
        if data == None:
            return
        if not data.is_folder():
            return
        
        full_create_path = data.path + "/"
        new_folder_name, ok = QInputDialog.getText(None, "Give new folder name", "")
        if not ok:
            return
        if new_folder_name.isEmpty() or new_folder_name.isNull():
            return
        if new_folder_name.contains("/"):
            return # show error here

        full_create_path = data.path + "/" + str(new_folder_name)
        self.controller.connection.create_folder(data.root, full_create_path, str(new_folder_name), data.path)


""" TreeController handler all the interaction to/from the main QTreeWidget """

class TreeController:

    def __init__(self, tree_widget, controls_ui, logger):
        self.tree = tree_widget
        self.controls_ui = controls_ui
        self.log = logger

        self.root_folder = None
        self.last_clicked = None
        self.connection = None
        self.selected_data = None

        # Treeview header init
        headers = self.tree.headerItem()
        headers.setTextAlignment(0, Qt.AlignLeft|Qt.AlignVCenter)
        headers.setTextAlignment(1, Qt.AlignRight|Qt.AlignVCenter)

        font = headers.font(0)
        font.setPointSize(12)
        headers.setFont(0, font)
        headers.setFont(1, font)

        # Thumbs init
        self.thumbs = {}
        
        # Connects
        self.tree.itemSelectionChanged.connect(self.item_selection_changed)
        self.tree.itemClicked.connect(self.item_clicked)
        self.tree.itemDoubleClicked.connect(self.item_double_clicked)
        self.tree.itemExpanded.connect(self.item_expanded)
        self.tree.itemCollapsed.connect(self.item_collapsed)

    def set_connection(self, connection):
        self.connection = connection

    def item_expanded(self, tree_item):
        self.set_icon("folder_opened", tree_item)

    def item_collapsed(self, tree_item):
        self.set_icon("folder", tree_item)
        
    def set_root_folder(self, root_folder):
        self.tree.clear()
        if self.root_folder != None:
            del self.root_folder
        self.root_folder = root_folder

        # Add root
        columns = QStringList()
        columns.append(root_folder.get_name())
        columns.append(root_folder.get_size())
        root_item = QTreeWidgetItem(columns)

        self.set_icon(root_folder.mime_type, root_item)
        self.update_link_area()
        
        self.tree.addTopLevelItem(root_item)
        root_item.setExpanded(True)
        root_folder.tree_item = root_item

        self.generate_children(root_folder)

        self.tree.setCurrentItem(root_item)
            
    def update_folder(self, path, folder):
        self.generate_children(folder)
        folder.tree_item.setExpanded(True)

    def update_item(self, path, item):
        print "No handled yet really, why fetch metadata of a file?"
        print "Updated when parent folder refresed"

    def get_folder_for_path(self, search_folder, path):
        for item in search_folder.get_items():
            if not item.is_folder():
                continue
            if item.path == path:
                return item
            found = self.get_folder_for_path(item, path)
            if found != None:
                return found
        return None
        
    def get_data_for_item(self, tree_item):
        item_name = tree_item.text(0)
        if self.root_folder.get_name() == item_name:
            data = self.root_folder
        else:
            data = self.get_data_for_name(self.root_folder, item_name)
        return data

    def get_data_for_name(self, folder, item_name):
        for item in folder.get_items():
            if item.get_name() == item_name:
                return item
            if item.is_folder():
                data = self.get_data_for_name(item, item_name)
                if data != None:
                    return data
        return None

    def generate_children(self, parent):
        # Clean parent of previous items
        self.clear_tree_item(parent.tree_item)
        for item in parent.get_items():
            # Read item params
            columns = QStringList()
            columns.append(item.get_name())
            columns.append(item.get_size())
 
            # Create tree item
            child = QTreeWidgetItem(columns)
            child.setTextAlignment(1, Qt.AlignRight|Qt.AlignVCenter)

            # Set icon with mime type, and folder indicator
            self.set_icon(item.mime_type, child)
            if item.is_folder():
                child.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

            # Set tree item to item data
            item.tree_item = child

        # sort alphapetically and add items to tree
        self.sort_and_show_children(parent)

    def sort_and_show_children(self, parent):
        folders = {}
        files = {}
        for item in parent.get_items():
            if item.is_folder():
                folders[item.get_name().lower()] = item
            else:
                files[item.get_name().lower()] = item

        sorted_folders = sorted(folders)
        sorted_files = sorted(files)

        # Sort folders by name and add to tree
        sorted_folder_tree_items = []
        for folder_name in sorted_folders:
            sorted_folder_tree_items.append(folders[folder_name].tree_item)
        parent.tree_item.addChildren(sorted_folder_tree_items)

        # Sort files by name and add to tree
        sorted_file_tree_items = []
        for file_name in sorted_files:
            sorted_file_tree_items.append(files[file_name].tree_item)
        parent.tree_item.addChildren(sorted_file_tree_items)
            
    def clear_tree_item(self, item):
        for child in item.takeChildren():
            item.removeChild(child)
            del child

    def set_icon(self, item_type, tree_item, index = 0, label = None):
        base_path = "ui/icons/"
        base_type = item_type.split("/")[0]
        # item type
        if item_type == "folder":
            icon = QIcon(base_path + "folder.png")
        elif item_type == "folder_opened":
            icon = QIcon(base_path + "folder_open.png")
        elif item_type == "n900":
            icon = QIcon(base_path + "n900_small.png")
        elif item_type == "size":
            icon = QIcon(base_path + "calculator.png")
        elif item_type == "time":
            icon = QIcon(base_path + "clock.png")
        elif item_type == "deleted_item":
            icon = QIcon(base_path + "cancel.png")
        elif item_type == "deleted_folder":
            icon = QIcon(base_path + "folder_delete.png")
        # base type (from mimetype pre /)
        elif base_type == "text":
            icon = QIcon(base_path + "document_edit.png")
        elif base_type == "image":
            icon = QIcon(base_path + "picture.png")
        elif base_type == "application":
            icon = QIcon(base_path + "applications.png")
        else:
            icon = QIcon(base_path + "document.png")
        if tree_item != None:
            tree_item.setIcon(index, icon)
        elif label != None:
            label.setPixmap(icon.pixmap(24,24))        

    def update_action_buttons(self, is_folder, is_root = False):
        self.controls_ui.button_download.setEnabled(not is_folder)
        self.controls_ui.button_upload.setEnabled(is_folder)
        self.controls_ui.button_new_folder.setEnabled(is_folder)
        self.controls_ui.button_remove.setEnabled(not is_root)
        self.controls_ui.button_rename.setEnabled(not is_root)

    def update_thumbnail(self, show, qpixmap = None):
        if qpixmap:
            self.controls_ui.thumb_container.setPixmap(qpixmap)
        self.controls_ui.thumb_container.setVisible(show)
            
    # Signal handlers

    def item_selection_changed(self):
        # We catch this as the N900 sometimes selected a item
        # but did not go to item_clicked handler
        # Although this does select items when you scroll slowly, might be confusing?
        selected = self.tree.selectedItems()
        if len(selected) == 1:
            self.item_clicked(selected[0], 0)
    
    def item_clicked(self, item, column):
        # Dont proceed if item is already the selected one
        # this would happen when double clicking
        if self.last_clicked == item:
            return
        self.last_clicked = item

        # Get data of clicked tree item
        data = self.get_data_for_item(item)
        if data == None:
            self.log("ERROR] Could not find data for tree item")
            return

        # Update ui with selected data
        self.controls_ui.selected_name_label.setText(data.get_name())
        self.controls_ui.modified_label.setText(data.modified)
        self.set_icon(data.mime_type, None, None, self.controls_ui.selected_icon_label)
        self.update_action_buttons(data.is_folder(), True if data.path == "" else False)

        # Update thumbnail if its available
        if data.has_thumb:
            self.set_thumb(data.path, data.root)
        else:
            self.update_thumbnail(False)

        self.selected_data = data

        # Enable public links once API gets
        #if not data.is_folder():
        #    self.update_link_area(data.public_link)
        #else:
        #    self.update_link_area()

    def set_thumb(self, image_path, root, size = "large"):
        # Check if we already have the thumb
        if self.thumbs.has_key(image_path):
            pixmap = self.thumbs[image_path]
            # Check if this path has been marked as not fetchable
            if pixmap == None:
                self.update_thumbnail(False)
                return
            self.update_thumbnail(True, pixmap)
        # Fetch thumb from web
        else:
            if not self.is_format_supported(image_path):
                self.log("Format not supported, not fetching thumbnail for", image_path)
                self.thumbs[image_path] = None # So we dont come here again
                return
            self.connection.get_thumbnail(image_path, root, size)
            
    def is_format_supported(self, image_path):
        # Check from qt if the format is accepptable
        format = image_path.split(".")[-1]
        try:
            supported = QImageReader.supportedImageFormats()
            supported.index(QtCore.QByteArray(format))
            return True
        except ValueError:
            return False

    def update_link_area(self, url = None):
        show = False
        if url != None:
            show = True
            self.controls_ui.public_link_line_edit.setText(url)
        self.controls_ui.public_link_line_edit.setVisible(show)
        self.controls_ui.button_open_public_link.setVisible(show)
        
    def item_double_clicked(self, item, column):
        if item.isExpanded():
            return
        data = self.get_data_for_item(item)
        if not data.is_folder():
            return
        self.connection.get_metadata(data.path, data.root, data.hash)
        
