
import os

from PyQt4 import QtCore, QtGui, QtMaemo5
from PyQt4.QtMaemo5 import QMaemo5InformationBox
from PyQt4.QtCore import Qt, QString, QStringList, QTimer, QDir, QSize
from PyQt4.QtGui import QMainWindow, QWidget, QDialog, QLabel, QTreeWidgetItem, QDesktopServices, QHeaderView
from PyQt4.QtGui import QImage, QPixmap, QIcon, QImageReader, QMovie, QGridLayout, QSizePolicy, QPalette
from PyQt4.QtGui import QInputDialog, QFileDialog, QMessageBox, QPushButton

from ui.ui_mainwindow import Ui_DropN900Widget
from ui.ui_trustedloginwidget import Ui_TrustedLoginWidget
from ui.ui_managerwidget import Ui_ManagerWidget
from ui.ui_consolewidget import Ui_ConsoleWidget
from ui.ui_loadingwidget import Ui_LoadingWidget


""" UiController controls ui view switching and ui interactions """

class UiController:

    def __init__(self, controller, debug_mode, logger):
        self.controller = controller
        self.datahandler = controller.datahandler
        self.debug_mode = debug_mode
        self.logger = logger

        ### Main Window
        self.main_widget = QMainWindow()
        self.main_widget.setAttribute(Qt.WA_Maemo5StackedWindow)
        self.main_ui = Ui_DropN900Widget()
        self.main_ui.setupUi(self.main_widget)

        # Stacked layout for context switching
        self.stacked_layout = QtGui.QStackedLayout()
        self.main_ui.centralwidget.setLayout(self.stacked_layout)

        # Menu items
        self.action_transfers = QtGui.QAction("Transfers", self.main_widget)
        self.action_settings = QtGui.QAction("Settings", self.main_widget)
        self.action_sync = QtGui.QAction("Synchronize", self.main_widget)
        self.action_sync_photos = QtGui.QAction("Sync Media", self.main_widget)
        self.action_console = QtGui.QAction("Show Log", self.main_widget)
        self.action_about = QtGui.QAction("About", self.main_widget)
        self.action_exit = QtGui.QAction("Exit", self.main_widget)

        self.main_ui.menubar.addAction(self.action_transfers)
        self.main_ui.menubar.addAction(self.action_settings)
        self.main_ui.menubar.addAction(self.action_sync)
        self.main_ui.menubar.addAction(self.action_sync_photos)
        self.main_ui.menubar.addAction(self.action_console)
        self.main_ui.menubar.addAction(self.action_about)
        self.main_ui.menubar.addAction(self.action_exit)

        # Connects
        self.action_transfers.triggered.connect(self.show_transfer_widget)
        self.action_sync.triggered.connect(self.synchronize_now)
        self.action_sync_photos.triggered.connect(self.synchronize_now_photos)
        self.action_settings.triggered.connect(self.show_settings_widget)
        self.action_console.triggered.connect(self.show_console)
        self.action_about.triggered.connect(self.show_about)
        self.action_exit.triggered.connect(self.shut_down)
        
        ### Trusted Login Widget
        self.trusted_login_widget = QWidget()
        self.trusted_login_ui = Ui_TrustedLoginWidget()
        self.trusted_login_ui.setupUi(self.trusted_login_widget)
        self.trusted_login_ui.label_icon.setPixmap(QPixmap(self.datahandler.datapath("ui/images/dropn900_logo.png")).scaled(65,65))

        # Connects
        self.trusted_login_ui.button_auth.clicked.connect(self.try_trusted_login)
        
        ### Manager Widget
        self.manager_widget = QWidget()
        self.manager_ui = Ui_ManagerWidget()
        self.manager_ui.setupUi(self.manager_widget)
        
        # Tree Controller
        tree = self.manager_ui.tree_widget
        self.tree_controller = TreeController(tree, self.manager_ui, self.controller, self.logger)

        # Hide public link elements on start
        self.manager_ui.button_copy_public_link.hide()
        self.manager_ui.button_open_public_link.hide()
        
        # Connects
        self.manager_ui.button_copy_public_link.clicked.connect(self.copy_item_link)
        self.manager_ui.button_open_public_link.clicked.connect(self.open_item_link)
        self.manager_ui.button_download.clicked.connect(self.item_download)
        self.manager_ui.button_upload.clicked.connect(self.item_upload)
        self.manager_ui.button_rename.clicked.connect(self.item_rename)
        self.manager_ui.button_remove.clicked.connect(self.item_remove)
        self.manager_ui.button_new_folder.clicked.connect(self.item_new_folder)
        self.manager_ui.sync_button.clicked.connect(self.synchronize_now)
        self.last_dl_location = None
        self.last_ul_location = None

        ### Console widget
        self.console_widget = QWidget(self.main_widget, Qt.Window)
        self.console_widget.setAttribute(Qt.WA_Maemo5StackedWindow)
        self.console_ui = Ui_ConsoleWidget()
        self.console_ui.setupUi(self.console_widget)
        self.console_ui.button_save.clicked.connect(self.save_log_to_file)
        self.console_ui.button_back.clicked.connect(self.hide_console)
        
        ### Settings widget
        self.settings_widget = None

        ### Fill stacked layout
        self.stacked_layout.addWidget(self.trusted_login_widget)
        self.stacked_layout.addWidget(self.manager_widget)
        self.stacked_layout.setCurrentWidget(self.trusted_login_widget)

        ### Loading Widget
        self.loading_widget = QWidget(self.manager_widget)
        self.loading_ui = Ui_LoadingWidget()
        self.loading_ui.setupUi(self.loading_widget)
        self.manager_ui.action_layout.insertWidget(3, self.loading_widget)
        self.loading_widget.hide()
        
        self.tree_controller.set_loading_ui(self.loading_ui)

        # Init loading animation
        self.loading_animation = QMovie(self.datahandler.datapath("ui/images/loading.gif"), "GIF", self.loading_ui.load_animation_label)
        self.loading_animation.setCacheMode(QMovie.CacheAll)
        self.loading_animation.setSpeed(150)
        self.loading_animation.setScaledSize(QtCore.QSize(48,48))
        self.loading_ui.load_animation_label.setMovie(self.loading_animation)

        # Init hide timer and icons for information messages
        self.information_message_timer = QTimer()
        self.information_message_timer.setSingleShot(True)
        self.information_message_timer.timeout.connect(self.hide_information_message)
        self.information_icon_ok = QPixmap(self.datahandler.datapath("ui/icons/check.png")).scaled(24,24)
        self.information_icon_error = QPixmap(self.datahandler.datapath("ui/icons/cancel.png")).scaled(24,24)
        self.information_icon_queue = QPixmap(self.datahandler.datapath("ui/icons/queue.png")).scaled(24,24)
        
        ### About dialog
        self.about_dialog = AboutDialog(self)
        
        self.set_synching(False)
        
    def set_synching(self, syncing):
        self.manager_ui.sync_button.setVisible(not syncing)
        self.manager_ui.sync_label.setVisible(syncing)

    def set_settings_widget(self, settings_widget):
        self.settings_widget = settings_widget
        
    def set_transfer_widget(self, transfer_widget):
        self.transfer_widget = transfer_widget
        
    def synchronize_now(self):
        self.settings_widget.sync_now_clicked()
        
    def synchronize_now_photos(self):
        self.controller.sync_manager.sync_media()
        
    def show(self):
        # Nokia N900 screen resolution, full screen
        self.main_widget.resize(800, 480) 
        self.main_widget.show()
        self.main_widget.showMaximized()

    def show_settings_widget(self):
        if self.settings_widget != None:
            if not self.settings_widget.isVisible():
                self.settings_widget.show()
                self.settings_widget.check_settings()

    def show_transfer_widget(self):
        if self.settings_widget.isVisible():
            self.settings_widget.hide()
        self.transfer_widget.show()
        
    def show_about(self):
        if not self.about_dialog.isVisible():
            self.about_dialog.show()
        
    def show_note(self, message):
        QMaemo5InformationBox.information(None, QString(message), 0)
        
    def show_banner(self, message, timeout = 5000):
        QMaemo5InformationBox.information(None, QString(message), timeout)
        
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

    def show_information_ui(self, message, succesfull, timeout = 4000):
        self.loading_ui.load_animation_label.hide()
        self.thumb_was_visible = self.manager_ui.thumb_container.isVisible()
        if self.thumb_was_visible:
            self.manager_ui.thumb_container.hide()
        self.loading_ui.info_label.setText(message)
        if succesfull == None:
            icon = self.information_icon_queue
        elif succesfull:
            icon = self.information_icon_ok
        else:
            icon = self.information_icon_error
        self.loading_ui.info_label_icon.setPixmap(icon)
        self.loading_ui.info_label_icon.show()
        self.loading_widget.show()
        self.information_message_timer.start(timeout)

    def hide_loading_ui(self):
        if not self.information_message_timer.isActive():
            self.loading_widget.hide()
        if self.loading_animation.state() == QMovie.Running:
            self.loading_animation.stop()

    def hide_information_message(self):
        self.loading_ui.info_label_icon.hide()
        self.hide_loading_ui()
        self.manager_ui.thumb_container.setVisible(self.thumb_was_visible)
            
    def try_trusted_login(self):
        self.trusted_login_ui.label_error.setText("")
        email = self.trusted_login_ui.line_edit_email.text()
        password = self.trusted_login_ui.line_edit_password.text()

        error = None
        if email.isEmpty():
            error = "Email can't be empty!"
        elif email.count("@") != 1:
            error = "Invalid email, check your @ signs!"
        elif email.contains(" "):
            error = "Invalid email, can't have spaces!"
        elif password.isEmpty():
            error = "Password can't be empty!"
            
        if error == None:
            self.show_banner("Authenticating...", 3000)
            self.set_trusted_login_info("Authenticating, please wait...")
            self.truested_email = self.datahandler.to_unicode(str(email.toUtf8()))
            self.trusted_password = self.datahandler.to_unicode(str(password.toUtf8()))
            QTimer.singleShot(100, self.do_trusted_login_networking)
        else:
            self.set_trusted_login_error(error)
            
    def set_trusted_login_error(self, error):
        self.trusted_login_ui.label_error.setStyleSheet("color: #9d1414;")
        self.trusted_login_ui.label_error.setText(error)
        self.truested_email = None
        self.trusted_password = None
        
    def set_trusted_login_info(self, info):
        self.trusted_login_ui.label_error.setStyleSheet("color: #149d2b;")
        self.trusted_login_ui.label_error.setText(info)
        
    def do_trusted_login_networking(self):
        self.controller.end_trusted_auth(self.truested_email.encode("utf-8"), self.trusted_password.encode("utf-8"))
        self.truested_email = None
        self.trusted_password = None
        
    def reset_trusted_login(self):
        self.trusted_login_ui.line_edit_email.clear()
        self.trusted_login_ui.line_edit_password.clear()
        self.trusted_login_ui.label_error.clear()

    def switch_context(self, view = None):
        widget = None
        if view == "trustedlogin":
            widget = self.trusted_login_widget
        if view == "manager":
            widget = self.manager_widget
        if view == "console":
            self.console_widget.show()
        if view == None and self.last_view != None:
            widget = self.last_view
        if widget != None:
            self.last_view = self.stacked_layout.currentWidget()
            self.stacked_layout.setCurrentWidget(widget)

    def get_selected_data(self):
        return self.tree_controller.selected_data
    
    # Signal handlers
            
    def shut_down(self):
        self.main_widget.close()

    def show_console(self):
        if self.console_widget.isVisible() == False:
            self.switch_context("console")
        else:
            self.hide_console()

    def hide_console(self):
        self.console_widget.hide()
                    
    def save_log_to_file(self):
        filename = self.datahandler.get_data_dir_path() + "dropn900.log"
        log_string = str(self.console_ui.text_area.toPlainText())
        try:
            log_file = open(filename, "w")
            log_file.write(log_string)
            log_file.close()
            self.show_banner("Log saved to " + filename)
        except IOError:
            self.logger.error("Could not open " + filename + " to save log")


    def browser_control_clicked(self):
        if self.controller.connected:
            self.switch_context()
        else:
            self.controller.end_auth()
            
    def copy_item_link(self):
        url = self.tree_controller.current_public_link
        if url == None:
            return
        self.datahandler.copy_url_to_clipboard(url)
    
    def open_item_link(self):
        url = self.tree_controller.current_public_link
        if url == None:
            return
        QDesktopServices.openUrl(QtCore.QUrl(url))

    def item_download(self):
        data = self.get_selected_data()
        if data == None:
            return
            
        if self.datahandler.dont_show_dl_dialog == False:
            # This dialog shows sometimes strange stuff on maemo5
            # It's a PyQt4 bug and its the best we got, you can cope with this
            if self.last_dl_location == None:
                self.last_dl_location = self.datahandler.get_data_dir_path()
            local_folder_path = QFileDialog.getExistingDirectory(self.manager_widget, QString("Select Download Folder"), QString(self.last_dl_location), QFileDialog.ShowDirsOnly|QFileDialog.HideNameFilterDetails|QFileDialog.ReadOnly)
            if local_folder_path.isEmpty():
                return
            py_unicode_path = self.datahandler.to_unicode(str(local_folder_path.toUtf8()))
            self.last_dl_location = py_unicode_path
            store_path = py_unicode_path + "/" + data.name
        else:
            dir_check = QDir(self.datahandler.get_data_dir_path())
            if not dir_check.exists():
                self.show_note("Cannot download, destination " + self.datahandler.get_data_dir_path() + " does not exist. Please set a new folder in settings.")
                return
            store_path = self.datahandler.get_data_dir_path() + data.name
        self.controller.connection.get_file(data.path, data.root, store_path, data.get_size(), data.mime_type)
        
    def item_upload(self):
        data = self.get_selected_data()
        if data == None or not data.is_folder():
            return

        # This dialog shows sometimes strange stuff on maemo5
        # It's a PyQt4 bug and its the best we got, you can cope with this
        if self.last_ul_location == None:
            self.last_ul_location = self.datahandler.get_data_dir_path()
        local_file_path = QFileDialog.getOpenFileName(self.manager_widget, QString("Select File for Upload"), QString(self.last_ul_location))
        if local_file_path.isEmpty():
            return
        py_unicode_path = self.datahandler.to_unicode(str(local_file_path.toUtf8()))
        self.last_ul_location = py_unicode_path[0:py_unicode_path.rfind("/")]
        self.controller.connection.upload_file(data.path, data.root, py_unicode_path)
        
    def item_rename(self):
        data = self.get_selected_data()
        if data == None:
            return

        # Get new name from user
        old_name = data.get_name()
        keyword = "file" if not data.is_folder() else "folder"
        new_name, ok = QInputDialog.getText(None, "Renaming " + keyword, "Give new name for " + keyword + " " + old_name, QtGui.QLineEdit.Normal, old_name)
        if not ok:
            return
        # Validate with QString
        if not self.is_name_valid(new_name, keyword):
            return
        # Make QString to python 'unicode'
        new_name = self.datahandler.to_unicode(str(new_name.toUtf8()))
        if old_name == new_name:
            return

        # Extension will be lost, ask user if he wants to leave it
        q_old_name = QtCore.QString(old_name)
        if q_old_name.contains("."):
            if not new_name.contains("."):
                format = old_name[q_old_name.lastIndexOf("."):]
                confirmation = QMessageBox.question(None, "Extension missing", "Do you want to append the original '" + format + "' extensions to the filename '" + new_name + "'?", QMessageBox.Yes, QMessageBox.No)
                if confirmation == QMessageBox.Yes:
                    new_name.append(format)

        # Get final new path and rename
        if data.parent == "/":
            new_name = data.parent + new_name
        else:
            new_name = data.parent + "/" + new_name
        self.controller.connection.rename(data.root, data.path, new_name, data)

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
        # Validate QString
        if not self.is_name_valid(new_folder_name, "folder"):
            return
        # Make QString to python unicode
        new_folder_name = self.datahandler.to_unicode(str(new_folder_name.toUtf8()))
        full_create_path = data.path + "/" + new_folder_name
        self.controller.connection.create_folder(data.root, full_create_path, new_folder_name, data.path)

    def is_name_valid(self, name, item_type):
        if name.isEmpty() or name.isNull():
            return False
        if name.contains("/"):
            self.show_information_ui("Cant use / in new " + item_type + " name", False)
            return False
        if name.contains("\\"):
            self.show_information_ui("Cant use \ in new " + item_type + " name", False)
            return False
        if name.startsWith(" "):
            self.show_information_ui("New " + item_type + " name cant start with a space", False)
            return False
        if name.endsWith(" "):
            self.show_information_ui("New " + item_type + " name cant end with a space", False)
            return False
        return True


""" About Dialog to show information and links to relevant URLs """

class AboutDialog(QDialog):

    def __init__(self, controller):
        QDialog.__init__(self, controller.main_widget, Qt.Dialog)
        self.setAttribute(Qt.WA_Maemo5StackedWindow)
        self.setWindowTitle("About DropN900")
        
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(5)
        grid_layout.setHorizontalSpacing(25)
        grid_layout.setContentsMargins(0, 10, 50, 0)
        self.setLayout(grid_layout)

        icon_label = QLabel(self)
        icon_label.setMinimumSize(128, 128)
        icon_label.setMaximumSize(128, 128)
        icon_label.setPixmap(QPixmap(controller.datahandler.datapath("ui/images/dropn900_logo.png")))
        icon_label.move(600, 5)
        
        topics = []           
        links = []
        
        label = QLabel("Version")
        topics.append(label)        
        self.layout().addWidget(label, 0, 0, Qt.AlignRight)
        
        label = QLabel("0.1.8")
        self.layout().addWidget(label, 0, 1)
                
        label = QLabel("Made by")
        topics.append(label)        
        self.layout().addWidget(label, 1, 0, Qt.AlignRight)
        
        label = QLabel("Jonne Nauha")
        self.layout().addWidget(label, 1, 1)

        label = QLabel("Pforce @ IRCNet & freenode")
        self.layout().addWidget(label, 2, 1)
        
        label = QPushButton("jonne.nauha@evocativi.com")
        label.clicked.connect(self.email_clicked)
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        links.append(label)
        self.layout().addWidget(label, 3, 1)
        
        label = QLabel("Official Thread")
        topics.append(label)       
        self.layout().addWidget(label, 4, 0, Qt.AlignRight)
        
        label = QPushButton("http://talk.maemo.org/showthread.php?t=58882")
        label.clicked.connect(self.thread_clicked)
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        links.append(label)
        self.layout().addWidget(label, 4, 1)
        
        label = QLabel("Bug tracker")
        topics.append(label)       
        self.layout().addWidget(label, 5, 0, Qt.AlignRight)
        
        label = QPushButton("http://github.com/jonnenauha/DropN900/issues")
        label.clicked.connect(self.tracker_clicked)
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        links.append(label)
        self.layout().addWidget(label, 5, 1)
        
        label = QLabel("Icons")
        topics.append(label)       
        self.layout().addWidget(label, 6, 0, Qt.AlignRight)
        
        label = QPushButton("http://openiconlibrary.sourceforge.net")
        label.clicked.connect(self.icons_clicked)
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        links.append(label)
        self.layout().addWidget(label, 6, 1)
                
        label = QLabel("Donate")
        topics.append(label)       
        self.layout().addWidget(label, 7, 0, Qt.AlignRight)
        
        label = QLabel("Paypal with above email or click")
        self.layout().addWidget(label, 7, 1)
        
        button = QPushButton()
        button.clicked.connect(self.donate_clicked)
        button.setMinimumSize(160, 70)
        button.setMaximumSize(160, 70)
        button.setStyleSheet("QPushButton { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(37, 37, 37, 255), \
                              stop:0.542714 rgba(66, 66, 66, 255), stop:1 rgba(39, 39, 39, 255)); border: 2px solid grey; border-radius: 15px; background-repeat: no-repeat; \
                              background-position: center center; background-image: url(" + controller.datahandler.datapath("ui/images/paypal.gif") + ") } \
                              QPushButton:pressed { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(37, 37, 37, 255), \
                              stop:0.542714 rgba(118, 118, 118, 255), stop:1 rgba(39, 39, 39, 255)); border: 2px solid white; }")        
        self.layout().addWidget(button, 7, 1, Qt.AlignRight)
        self.layout().setRowMinimumHeight(7, 200)
        
        style = "QLabel { color: #0099FF; }"
        for topic in topics:
            topic.setStyleSheet(style)
            
        # Cant seem to change color of links no matter what
        style = "QPushButton { background-color: transparent; border: 0px; text-decoration: underline; } \
                 QPushButton:pressed { color: #0099FF; }"
        for link in links:
            link.setStyleSheet(style)
        
    def email_clicked(self):
        QDesktopServices.openUrl(QtCore.QUrl("mailto:user@foo.com?subject=DropN900 Feedback"))
        
    def tracker_clicked(self):
        QDesktopServices.openUrl(QtCore.QUrl("http://github.com/jonnenauha/DropN900/issues"))
        
    def thread_clicked(self):
        QDesktopServices.openUrl(QtCore.QUrl("http://talk.maemo.org/showthread.php?t=58882"))
    
    def icons_clicked(self):
        QDesktopServices.openUrl(QtCore.QUrl("http://openiconlibrary.sourceforge.net"))
        
    def donate_clicked(self):
        QDesktopServices.openUrl(QtCore.QUrl("https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=jonne.nauha@evocativi.com&lc=FI&item_name=Jonne%20Nauha&item_number=dropn900&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted"))
    
    
""" TreeController handler all the interaction to/from the main QTreeWidget """

class TreeController:

    def __init__(self, tree_widget, controls_ui, controller, logger):
        self.tree = tree_widget
        self.controls_ui = controls_ui
        self.controller = controller
        self.datahandler = controller.datahandler
        self.logger = logger

        self.root_folder = None
        self.last_clicked = None
        self.connection = None
        self.selected_data = None
        self.current_public_link = None
        self.loading_ui = None
        
        # Treeview header init
        headers = self.tree.headerItem()
        headers.setTextAlignment(0, Qt.AlignLeft|Qt.AlignVCenter)
        headers.setTextAlignment(1, Qt.AlignRight|Qt.AlignVCenter)

        font = headers.font(0)
        font.setPointSize(12)
        headers.setFont(0, font)
        headers.setFont(1, font)
        
        self.tree.header().resizeSections(QHeaderView.ResizeToContents)
        
        # Click tracking
        self.clicked_items = {}
        
        # Supported thumb image formats
        self.supported_reader_formats = QImageReader.supportedImageFormats()
        
        # Thumbs init
        self.thumbs = {}

        # Current loading anim list
        self.load_animations = []
        
        # Connects
        self.tree.itemSelectionChanged.connect(self.item_selection_changed)
        self.tree.itemClicked.connect(self.item_clicked)
        self.tree.itemExpanded.connect(self.item_expanded)
        self.tree.itemCollapsed.connect(self.item_collapsed)

    def setup(self, connection):
        self.connection = connection
        
    def set_loading_ui(self, loading_ui):
        self.loading_ui = loading_ui

    def item_expanded(self, tree_item):
        self.tree.setCurrentItem(tree_item)
        self.folder_opened(tree_item)
        self.set_icon("folder_opened", tree_item)
        self.tree.header().resizeSections(QHeaderView.ResizeToContents)

    def item_collapsed(self, tree_item):
        self.set_icon("folder", tree_item)
        self.tree.header().resizeSections(QHeaderView.ResizeToContents)
        
    def set_root_folder(self, root_folder):
        self.tree.clear()
        self.clear_all_load_animations()
        
        if self.root_folder != None:
            del self.root_folder
        self.root_folder = root_folder

        # Add root
        columns = QStringList()
        columns.append(root_folder.get_name())
        columns.append(root_folder.get_size())
        root_item = QTreeWidgetItem(columns)

        self.set_icon(root_folder.mime_type, root_item)
        
        self.tree.addTopLevelItem(root_item)
        root_item.setExpanded(True)
        root_folder.tree_item = root_item

        self.generate_children(root_folder)
        self.add_loading_widgets(root_folder)

        self.tree.setCurrentItem(root_item)
        self.start_load_anim(root_folder)
        
        self.tree.header().resizeSections(QHeaderView.ResizeToContents)
            
    def update_folder(self, path, folder):
        self.generate_children(folder)
        folder.tree_item.setExpanded(True)
        self.tree.header().resizeSections(QHeaderView.ResizeToContents)

    def update_item(self, path, item):
        print "No handled yet really, why fetch metadata of a file?"
        print "Updated when parent folder refresed"

    def get_folder_for_path(self, path, search_folder = None):
        # Return root
        if path == "/" or path == "":
            return self.root_folder
        # If start folder was not defined, start from root
        if search_folder == None:
            search_folder = self.root_folder
        # Iterate folders untill we find path
        for folder_item in search_folder.get_folders():
            if folder_item.path == path:
                return folder_item
            found = self.get_folder_for_path(path, folder_item)
            if found != None:
                return found
        return None

    def get_item_for_path(self, path):
        found = self.get_folder_for_path(path)
        if found != None:
            return found
        found = self.get_file_for_path(path)
        return found

    def get_file_for_path(self, path, search_folder = None):
        # If start folder was not defined, start from root
        if search_folder == None:
            search_folder = self.root_folder
        # Iterate files untill we find path
        for file_item in search_folder.get_files():
            if file_item.path == path:
                return file_item
        # Iterate sub folders as deep as needed to find path
        for folder in search_folder.get_folders():
            found = self.get_file_for_path(path, folder)
            if found != None:
                return found
        return None
        
    def get_data_for_item(self, tree_item):
        name, path = self.parse_tree_item(tree_item)
        if self.root_folder.get_name() == name and (path == "/DropBox" or path == "/DropN900"):
            data = self.root_folder
        else:
            data = self.get_data_for_name(self.root_folder, name, path)
        return data
        
    def parse_tree_item(self, tree_item):
        item_path = []
        item_name = self.datahandler.to_unicode(str(tree_item.text(0).toUtf8()))
        item_path.append(item_name)
        if tree_item.parent() != None:
            current_item = tree_item
            while current_item.parent() != None:
                current_item = current_item.parent()
                item_path.append(self.datahandler.to_unicode(str(current_item.text(0).toUtf8())))
            item_path.pop() # remove root item name from path
        path_str = ""
        for i in range(len(item_path)):
            path_str += "/" + item_path.pop()
        return item_name, self.datahandler.to_unicode(path_str)
        
    def get_data_for_name(self, folder, item_name, item_path):
        for item in folder.get_items():
            if item.get_name() == item_name and item.path == item_path:
                return item
        for folder in folder.get_folders():
            data = self.get_data_for_name(folder, item_name, item_path)
            if data != None:
                return data
        return None

    def generate_children(self, parent):
        # Clean parent of previous items
        self.clear_tree_item(parent)
        for item in parent.get_items():
            # Read item params
            columns = QStringList()
            columns.append(item.get_name())
            columns.append(item.get_size())
            # Create tree item
            child = QTreeWidgetItem(columns)
            child.setTextAlignment(1, Qt.AlignRight|Qt.AlignVCenter)
            child.setFirstColumnSpanned(True)
            # Set icon with mime type, and folder indicator
            self.set_icon(item.mime_type, child)
            if item.is_folder():
                child.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            # Set tree item to item data
            item.tree_item = child

        # sort alphapetically and add items to tree
        self.sort_and_show_children(parent)

        # add loading widgets
        self.add_loading_widgets(parent.get_items())

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

    def add_loading_widgets(self, children):
        # Generate list if only one item was given
        if not type(children) is list:
            item_list = []
            item_list.append(children)
            children = item_list
        # Add loading widgets to tree items
        for child in children:
            if child.tree_item == None:
                return
            # Create loading widget
            load_widget = QtGui.QLabel()
            load_widget.resize(50,50)
            #load_widget.setMaximumSize(50,50)
            load_widget.setStyleSheet("QLabel { background-color: transparent; }")

            # Create animation
            load_anim = QMovie(self.datahandler.datapath("ui/images/loading_tree.gif"), "GIF", load_widget)
            load_anim.setCacheMode(QMovie.CacheAll)
            load_anim.setSpeed(150)
            load_anim.setScaledSize(QtCore.QSize(50,50))

            # Add to data model and tree
            child.set_load_widget(load_widget, load_anim)
            self.tree.setItemWidget(child.tree_item, 1, load_widget)
            
    def clear_tree_item(self, data):
        item = data.tree_item
        for child in item.takeChildren():
            item.removeChild(child)
            del child

    def set_icon(self, item_type, tree_item, index = 0, label = None):
        base_path = self.controller.datahandler.app_root + "ui/icons/"
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
        if self.loading_ui.info_label.isVisible():
            show = False
        self.controls_ui.thumb_container.setVisible(show)

    # Qt signal handlers below

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
        if self.clicked_items.has_key(item):
            data = self.clicked_items[item]
        else:
            data = self.get_data_for_item(item)
            if data != None:
                self.clicked_items[item] = data
            
        # Be sure that something was returned
        if data == None:
            self.logger.error("Could not find data for clicked tree item.")
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
            
        # Set selected data
        self.selected_data = data

        # Show public link if present
        self.update_link_area(data.public_link)

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
                self.logger.warning("Format not supported, not fetching thumbnail for", image_path)
                self.thumbs[image_path] = None # So we dont come here again
                return
            self.connection.get_thumbnail(image_path, root, size)
            
    def is_format_supported(self, image_path):
        # Check from qt if the format is accepptable
        format = image_path.split(".")[-1]
        try:
            self.supported_reader_formats.index(QtCore.QByteArray(format.lower()))
            return True
        except ValueError:
            return False

    def update_link_area(self, public_link_url):
        show_link_controls = False
        if public_link_url != None:
            show_link_controls = True
        self.controls_ui.button_copy_public_link.setVisible(show_link_controls)
        self.controls_ui.button_open_public_link.setVisible(show_link_controls)
        self.controls_ui.button_upload.setVisible(not show_link_controls)
        self.controls_ui.button_new_folder.setVisible(not show_link_controls)
        self.current_public_link = public_link_url
        
    def folder_opened(self, item):
        if not item.isExpanded():
            return
        # We always want to reset found tree items when we
        # are building the tree up with metadata fetches
        self.clicked_items = {}
        data = self.selected_data
        # Validity checks
        if data == None:
            self.logger.error("Could not find data for clicked tree item.")
            return
        if not data.is_folder():
            return
        # Start loading anim and get new metadata with hash
        self.start_load_anim(data)
        self.connection.get_metadata(data.path, data.root, data.hash)
        
    def start_load_anim(self, item):
        item.set_loading(True)
        self.load_animations.append(item)

    def stop_load_anim(self, item):
        item.set_loading(False)
        try:
            self.load_animations.remove(item)
        except ValueError:
            return

    def stop_all_load_anims(self):
        for item in self.load_animations:
            item.set_loading(False)
        self.load_animations = []

    def clear_all_load_animations(self):
        self.load_animations = []      
          
