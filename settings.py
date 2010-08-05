
import os

from ConfigParser import ConfigParser, SafeConfigParser, NoSectionError, NoOptionError

from PyQt4 import QtMaemo5
from PyQt4.QtCore import Qt, QDir, QString
from PyQt4.QtGui import QMainWindow, QWidget, QInputDialog, QFileDialog, QMessageBox, QStandardItemModel, QStandardItem, QVBoxLayout, QPixmap, QMessageBox
from PyQt4.QtMaemo5 import QMaemo5ValueButton, QMaemo5ListPickSelector

from ui.ui_settingswidget import Ui_SettingsWidget

    
""" ConfigHelper handler SettingsWidget ui read/write to file """

class ConfigHelper:

    def __init__(self, datahandler, logger):
        self.datahandler = datahandler 
        self.logger = logger
        self.settings_config_filename = self.datahandler.configpath("settings.ini").encode("utf-8")
        self.current_settings = None
        self.read_settings(self.settings_config_filename)

    def set_current_settings(self, download_data, authentication_data, automate_sync_data):
        self.current_settings = {}
        self.current_settings["download"] = download_data
        self.current_settings["authentication"] = authentication_data
        self.current_settings["automated-sync"] = automate_sync_data
        
        ### Notify related parts of the app of the settings change
        
        # Default download folder
        if download_data["default-folder"][-1] != "/":
            self.datahandler.set_data_dir_path(download_data["default-folder"] + "/")
        else:
            self.datahandler.set_data_dir_path(download_data["default-folder"])
            
        # Show download dialog
        self.datahandler.dont_show_dl_dialog = download_data["no-dialog"]
            
        # Store authentication
        self.datahandler.store_auth_to_file = authentication_data["store-auth"]
        
        # Sync only on WLAN
        self.datahandler.only_sync_on_wlan = automate_sync_data["only-sync-on-wlan"]
        
    def get_current_settings(self):
        return self.current_settings
    
    def read_settings(self, filename):
        settings_config = SafeConfigParser()
        settings_config.read(filename)
        try:
            # Download section
            section = "download"
            download_data = {}
            download_data["default-folder"] = settings_config.get(section, "default-folder")
            download_data["no-dialog"] = settings_config.getboolean(section, "no-dialog") 
            
            # Authentication section
            section = "authentication"
            authentication_data = {}
            authentication_data["store-auth"] = settings_config.getboolean(section, "store-auth") 

            # Automated sync section
            section = "automated-sync"
            automate_sync_data = {}
            automate_sync_data["enabled"] = settings_config.getboolean(section, "enabled")
            automate_sync_data["only-sync-on-wlan"] = settings_config.getboolean(section, "only-sync-on-wlan")
            automate_sync_data["update-interval"] = settings_config.getint(section, "update-interval") 
            automate_sync_data["sync-path"] = settings_config.get(section, "sync-path")

            self.set_current_settings(download_data, authentication_data, automate_sync_data)            
        except NoSectionError:
            self.write_default_settings()
        except NoOptionError, e:
            print "DropN900 config is missing a settings:", e
        except ValueError:
            self.write_default_settings()

        
    def write_default_settings(self, force_dl_folder = False):
        download_data = {}
        if force_dl_folder == False:
            download_data["default-folder"] = self.datahandler.get_data_dir_path()
        else:
            download_data["default-folder"] = self.datahandler.default_data_root
        download_data["no-dialog"] = False
        
        authentication_data = {}
        authentication_data["store-auth"] = True
        
        automate_sync_data = {}
        automate_sync_data["enabled"] = False
        automate_sync_data["only-sync-on-wlan"] = True
        automate_sync_data["update-interval"] = 10
        automate_sync_data["sync-path"] = "None"
        
        self.write_settings(download_data, authentication_data, automate_sync_data)
    
    def write_settings(self, download_data, authentication_data, automate_sync_data):
        settings_config = ConfigParser()
        try:
            # Write config values
            section = "download"
            settings_config.add_section(section)
            settings_config.set(section, "default-folder", download_data["default-folder"])
            if download_data["no-dialog"] == True:
                settings_config.set(section, "no-dialog", "true")
            else:
                settings_config.set(section, "no-dialog", "false")

            section = "authentication"
            settings_config.add_section(section)
            if authentication_data["store-auth"] == True:
                settings_config.set(section, "store-auth", "true")
            else:
                settings_config.set(section, "store-auth", "false")

            section = "automated-sync"
            settings_config.add_section(section)
            if automate_sync_data["enabled"] == True:
                settings_config.set(section, "enabled", "true")
            else:
                settings_config.set(section, "enabled", "false")
            if automate_sync_data["only-sync-on-wlan"] == True:
                settings_config.set(section, "only-sync-on-wlan", "true")
            else:
                settings_config.set(section, "only-sync-on-wlan", "false")
            str_update_interval = str(automate_sync_data["update-interval"])
            settings_config.set(section, "update-interval", str_update_interval)
            settings_config.set(section, "sync-path", automate_sync_data["sync-path"])
            
            self.set_current_settings(download_data, authentication_data, automate_sync_data)
        except NoSectionError:
            self.current_settings = None
            return
        except ValueError:
            self.current_settings = None
            return
            
        try:
            # Write config to file
            config_file = open(self.settings_config_filename, "w")
            settings_config.write(config_file)
            config_file.close()
        except IOError:
            self.current_settings = None
        
""" SettingWidget is the DropN900 settings ui """

class SettingsWidget(QMainWindow):
    
    def __init__(self, main_ui_handler, config_helper, logger):
        QMainWindow.__init__(self, main_ui_handler.main_widget, Qt.Window)
        self.setAttribute(Qt.WA_Maemo5StackedWindow)
        self.setWindowTitle("DropN900 - Settings")
        self.setCentralWidget(QWidget())
        self.ui = Ui_SettingsWidget()
        self.ui.setupUi(self.centralWidget())
        
        self.main_ui_handler = main_ui_handler
        self.tree_controller = main_ui_handler.tree_controller
        self.config_helper = config_helper
        self.datahandler = config_helper.datahandler
        self.logger = logger
        self.store_settings = False
        self.backup_settings = None
        self.connection_manager = None
        self.sync_manager = None
        
        # Icons for titles
        self.ui.downloading_icon.setPixmap(QPixmap(self.datahandler.datapath("ui/icons/download.png")))
        self.ui.authentication_icon.setPixmap(QPixmap(self.datahandler.datapath("ui/icons/authentication.png")))
        self.ui.sync_icon.setPixmap(QPixmap(self.datahandler.datapath("ui/icons/folder-sync.png")))

        # Connects
        self.ui.button_save.clicked.connect(self.save_setting_clicked)
        self.ui.button_cancel.clicked.connect(self.hide)
        self.ui.button_browse_folder.clicked.connect(self.set_default_dl_folder)
        self.ui.button_reset_auth.clicked.connect(self.reset_authentication_clicked)
        self.ui.button_sync_now.clicked.connect(self.sync_now_clicked)
        
        self.ui.checkbox_enable_sync.toggled.connect(self.set_sync_widgets_enabled)
        self.ui.checkbox_only_wlan_sync.toggled.connect(self.set_wlan_sync_only_enabled)
        
        # Create maemo value button for selecting sync location
        self.sync_path_model = QStandardItemModel(0,1)

        self.sync_path_pick_selector = QMaemo5ListPickSelector()
        self.sync_path_pick_selector.setModel(self.sync_path_model)
        self.sync_path_pick_selector.selected.connect(self.sync_path_selected)
        
        self.sync_path_button = QMaemo5ValueButton("Sync Path")
        self.sync_path_button.setValueLayout(QMaemo5ValueButton.ValueUnderTextCentered)
        self.sync_path_button.setPickSelector(self.sync_path_pick_selector)
        
        self.ui.sync_buttons_layout.insertWidget(0, self.sync_path_button)

        # Get initial settings and set to ui
        init_settings = self.config_helper.get_current_settings()
        if init_settings == None:
            self.logger.config("Settings data from file invalid, writing defaults")
            self.config_helper.write_default_settings()
            init_settings = self.config_helper.get_current_settings()
        self.set_settings_to_ui(init_settings["download"], init_settings["authentication"], init_settings["automated-sync"])
        
        action_restore_defaults = self.menuBar().addAction("Restore Defaults")
        action_restore_defaults.triggered.connect(self.restore_defaults)
        
    def setup(self, connection_manager, sync_manager):
        self.connection_manager = connection_manager
        self.sync_manager = sync_manager
        
    def restore_defaults(self):
        confirmation = QMessageBox.question(None, " ", "Sure you want to restore default settings?", QMessageBox.Yes, QMessageBox.Cancel)
        if confirmation == QMessageBox.Cancel:
            return
        self.logger.config("Restoring default settings to config")
        self.config_helper.write_default_settings(True)
        default_data = self.config_helper.get_current_settings()
        self.set_settings_to_ui(default_data["download"], default_data["authentication"], default_data["automated-sync"])
        self.select_config_sync_path(default_data["automated-sync"]["sync-path"])
        
    def handle_root_folder(self, root_folder):
        items = []
        if root_folder == None:
            enabled = False            
            items.append("Connect to DropBox first")
        else:
            enabled = True
            items.append("None")
            self.populate_folder_list(items, root_folder)
        self.populate_sync_path_model(items)
        self.select_config_sync_path(self.config_helper.get_current_settings()["automated-sync"]["sync-path"])
        self.ui.button_sync_now.setEnabled(enabled)
        self.sync_path_button.setEnabled(enabled)
            
    def populate_folder_list(self, folder_list, search_folder):
        for folder in search_folder.get_folders():
            folder_list.append(folder.path)
            self.populate_folder_list(folder_list, folder)

    def populate_sync_path_model(self, folder_paths):
        self.sync_path_model.clear() 
        for folder_path in folder_paths:
            item = QStandardItem(folder_path)
            item.setEditable(False)
            if folder_path == "Connect to DropBox first":
                item.setTextAlignment(Qt.AlignCenter)
            self.sync_path_model.appendRow(item)
            
    def select_config_sync_path(self, config_sync_path):
        found_items = self.sync_path_model.findItems(config_sync_path)
        if len(found_items) > 0:
            index = found_items[0].index().row()
        else:
            config_item = QStandardItem(config_sync_path)
            config_item.setEditable(False)
            self.sync_path_model.insertRow(1, config_item)
            index = 1
        self.sync_path_pick_selector.setCurrentIndex(index)
            
    def check_settings(self):
        self.sync_path_selected(str(self.sync_path_button.valueText()))
        download_default_folder = self.ui.lineedit_default_download_folder.text()
        dir_check = QDir(download_default_folder)
        if not dir_check.exists():
            confirmation = QMessageBox.question(None, "Default Download Folder", "The folder " + str(download_default_folder) + " does not exist anymore. Define new folder now or reset to default?", QMessageBox.Yes, QMessageBox.Reset)
            if confirmation == QMessageBox.Yes:
                self.set_default_dl_folder(False, self.datahandler.default_data_root)
            if confirmation == QMessageBox.Reset:
                self.ui.lineedit_default_download_folder.setText(self.datahandler.default_data_root)
            self.parse_settings_from_ui()
    
    def sync_path_selected(self, new_path):
        if new_path == "None":
            enabled = False
        else:
            enabled = True
        if not self.sync_path_button.isEnabled():
            enabled = False
        self.set_sync_controls_enabled(enabled)
        
    def save_setting_clicked(self):
        self.store_settings = True
        self.hide()
        
    def reset_authentication_clicked(self):
        self.config_helper.datahandler.reset_auth()
        
    def set_default_dl_folder(self, magic, open_in_path = None):
        if open_in_path == None:
            open_in_path = self.ui.lineedit_default_download_folder.text()
        local_folder_path = QFileDialog.getExistingDirectory(None, QString("Select Default Download Folder"), QString(open_in_path), (QFileDialog.ShowDirsOnly|QFileDialog.HideNameFilterDetails|QFileDialog.ReadOnly))
        if local_folder_path.isEmpty():
            self.ui.lineedit_default_download_folder.setText(open_in_path)
            return
        dir_check = QDir(local_folder_path)
        if dir_check.exists():
            self.ui.lineedit_default_download_folder.setText(local_folder_path)
        else:
            self.logger.warning("Could not validate " + str(local_folder_path) + " folder, resetting to default.")
            self.ui.lineedit_default_download_folder.setText(open_in_path)
    
    def set_sync_controls_enabled(self, enabled):
        self.ui.button_sync_now.setEnabled(enabled)
        self.ui.checkbox_enable_sync.setEnabled(enabled)
        self.ui.checkbox_only_wlan_sync.setEnabled(enabled)
        #self.set_sync_widgets_enabled(enabled)
    
    def set_sync_widgets_enabled(self, enabled):
        if not self.ui.checkbox_enable_sync.isChecked():
            enabled = False
        self.ui.sync_frame.setEnabled(enabled)
        #self.ui.checkbox_only_wlan_sync.setEnabled(enabled)
        self.ui.label_update_every.setEnabled(enabled)
        self.ui.spinbox_sync_interval.setEnabled(enabled)
        self.ui.label_min.setEnabled(enabled)
        
    def set_wlan_sync_only_enabled(self, enabled):
        # NOTIFY TO SYNC MANAGER THAT USE ONLY WLAN IMMIDIATELY?
        # - no affected only after save
        pass

    def sync_now_clicked(self):
        if not self.isVisible():
            sync_path = self.config_helper.get_current_settings()["automated-sync"]["sync-path"]
        else:
            sync_path = str(self.sync_path_button.valueText())
            if sync_path != self.config_helper.get_current_settings()["automated-sync"]["sync-path"]:
                self.parse_settings_from_ui()
        self.sync_manager.sync_now(sync_path)
        
    def showEvent(self, show_event):
        self.backup_settings = self.config_helper.get_current_settings()
        self.handle_root_folder(self.tree_controller.root_folder)
        self.hide_unused()
        QWidget.showEvent(self, show_event)
        
    def hide_unused(self):
        self.ui.checkbox_enable_sync.hide()
        self.ui.sync_frame.hide()
        
    def hideEvent(self, hide_event):
        if self.store_settings:
            self.logger.config("Storing new settings to config")
            self.parse_settings_from_ui()
        else:
            if self.backup_settings != None:
                self.set_settings_to_ui(self.backup_settings["download"], self.backup_settings["authentication"], self.backup_settings["automated-sync"])
            else:
                self.logger.error("Settings data from file invalid, cannot restore state.")
        self.store_settings = False
        QWidget.hideEvent(self, hide_event)
        
    def parse_settings_from_ui(self):
        # Download settings
        download_data = {} 
        download_default_folder = self.ui.lineedit_default_download_folder.text()
        dir_check = QDir(download_default_folder)
        if dir_check.exists():
            download_data["default-folder"] = str(download_default_folder)
        else:
            download_data["default-folder"] = self.config_helper.datahandler.get_data_dir_path()
            self.ui.lineedit_default_download_folder.setText(download_data["default-folder"])
            self.main_ui_handler.show_banner("Could not validate default download folder " + str(download_default_folder) + ", reseted to default")
            self.logger.warning("Default download folder invalid, reseted to default")
        download_data["no-dialog"] = self.ui.checkbox_no_dl_dialog.isChecked()
        
        # Authentication settings
        authentication_data = {}
        authentication_data["store-auth"] = self.ui.checkbox_enable_store_auth.isChecked()

        # Automated sync
        automate_sync_data = {}
        automate_sync_data["enabled"] = self.ui.checkbox_enable_sync.isChecked()
        automate_sync_data["only-sync-on-wlan"] = self.ui.checkbox_only_wlan_sync.isChecked()
        automate_sync_data["update-interval"] = self.ui.spinbox_sync_interval.value()
        automate_sync_data["sync-path"] = str(self.sync_path_button.valueText())
        
        self.config_helper.write_settings(download_data, authentication_data, automate_sync_data)
        
    def set_settings_to_ui(self, download_data, authentication_data, automate_sync_data):
        # Download settings
        dir_check = QDir(download_data["default-folder"])
        if dir_check.exists():
            self.ui.lineedit_default_download_folder.setText(download_data["default-folder"])
        else:
            self.ui.lineedit_default_download_folder.setText(str(QDir.home().absolutePath()) + "/MyDocs/DropN900/")
        self.ui.checkbox_no_dl_dialog.setChecked(download_data["no-dialog"])

        # Authentication settings
        self.ui.checkbox_enable_store_auth.setChecked(authentication_data["store-auth"])
        
        # Automated sync
        self.ui.checkbox_enable_sync.setChecked(automate_sync_data["enabled"])
        self.set_sync_widgets_enabled(automate_sync_data["enabled"])
        self.ui.checkbox_only_wlan_sync.setChecked(automate_sync_data["only-sync-on-wlan"])
        self.ui.spinbox_sync_interval.setValue(automate_sync_data["update-interval"])
        
