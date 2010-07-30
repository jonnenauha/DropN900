
from __future__ import division
import os

from PyQt4.QtGui import QIcon, QPixmap, QImage, QApplication
from PyQt4.QtCore import QDir, QString

from ConfigParser import ConfigParser, SafeConfigParser, NoSectionError

""" DataParser gets data from network layer, converts
    to app format and sends onwards to ui layer """

class DataParser:

    def __init__(self, ui_handler, logger):
        self.ui_handler = ui_handler
        self.tree_controller = ui_handler.tree_controller
        self.controller = ui_handler.controller
        self.logger = logger
        self.uid = None

    def parse_metadata(self, data, opened_folders):
        tree_item = None
        if data == None:
            return tree_item
     
        if data["is_dir"]:
            parent_root = data["root"]
            # Find existing folder, or create root
            if data["path"] != "":
                folder = self.tree_controller.get_folder_for_path(data["path"])
                if folder == None:
                    self.logger.error("Something went very wrong, did not find folder in parse_metada()!")
                    return tree_item
                folder.clear_items()
                folder.hash = data["hash"]
                self.check_deleted(data, folder, folder.tree_item)
            else:
                folder = Collection(data["path"], "", data["icon"], data["thumb_exists"], parent_root, data["hash"])

            # Add children to folder
            for item in data["contents"]:
                path = item["path"]
                size = item["size"]
                modified = item["modified"]
                icon = item["icon"]
                has_thumb = item["thumb_exists"]
                if item["is_dir"]:
                    child = Collection(path, modified, icon, has_thumb, parent_root)
                else:
                    child = Resource(path, size, modified, item["mime_type"], icon, has_thumb, parent_root)
                    if path.startswith("/Public/"):
                        child.generate_public_link(self.uid)
                folder.add_item(child)
                self.check_deleted(item, child)

            # Update tree view
            if folder.path == "":
                self.tree_controller.set_root_folder(folder)
            else:
                self.tree_controller.update_folder(folder.path, folder)

            tree_item = folder

##            # Expand previously opened folders
##            if opened_folders != None:
##                for child_folder in folder.get_folders():
##                    if opened_folders.has_key(child_folder.get_name()):
##                        if child_folder.path == opened_folders[child_folder.get_name()]:
##                            self.controller.connection.get_metadata(child_folder.path, child_folder.root)

        return tree_item

    def check_deleted(self, data, item, tree_item = None):
        # This is a bit retarded looking... meh, will remove at some point
        try:
            if data["is_deleted"]:
                if data["is_dir"]:
                    if item.tree_item != None:
                        item.tree_item.setExpanded(False)
                        item.tree_item.setIcon(0, QIcon(self.controller.datahandler.datapath("ui/icons/folder_delete.png")))
                        item.tree_item.setText(1, "deleted")
                    else:
                        item.mime_type = "deleted_folder"
                else:
                    if item.tree_item != None:
                        item.tree_item.setIcon(0, QIcon(self.controller.datahandler.datapath("ui/icons/cancel.png")))
                        item.tree_item.setText(1, "deleted")
                    else:
                        item.mime_type = "deleted_item"
                item.modified = "deleted"
        except KeyError:
            return

    def parse_thumbnail(self, resp, image_path):
        image = QImage.fromData(resp.read())
        if image.isNull():
            self.logger.warning("Failed to generate image from raw data for", image_path)
            self.tree_controller.thumbs[image_path] = None # So we dont come here again
            return
        pixmap = QPixmap.fromImage(image)
        self.tree_controller.thumbs[image_path] = pixmap
        self.tree_controller.update_thumbnail(True, pixmap)

    def parse_account_info(self, resp):
        if resp.status == 200:
            account_data = resp.data
            self.uid = str(account_data["uid"])
            name = account_data["display_name"]
            self.ui_handler.manager_ui.label_username.setText(name)
            user_icon = QPixmap(self.controller.datahandler.datapath("ui/icons/user.png"))
            self.ui_handler.manager_ui.label_username_icon.setPixmap(user_icon.scaled(24,24))
            self.logger.auth("Account data received for " + name)
        else:
            self.ui_handler.manager_ui.label_username.setText("unknown user")
            user_icon = QPixmap(self.controller.datahandler.datapath("ui/icons/user_white.png"))
            self.ui_handler.manager_ui.label_username_icon.setPixmap(user_icon.scaled(24,24))
            self.logger.auth("Failed to fetch account data, treating as unknown user")


""" Maemo data handler """

class MaemoDataHandler:

    def __init__(self, controller, maemo, logger):
        self.controller = controller
        self.maemo = maemo
        self.logger = logger
        self.store_auth_to_file = True
        self.dont_show_dl_dialog = False
        self.only_sync_on_wlan = True
        if self.maemo:
            self.user_home = str(QDir.home().absolutePath())
            self.app_root = "/opt/dropn900/"
            self.config_root = self.user_home + "/.dropn900/"
            self.data_root = self.user_home + "/MyDocs/DropN900/"
            self.default_data_root = self.user_home + "/MyDocs/DropN900"
        else:
            self.app_root = ""
            self.config_root = ""
            self.data_root = ""
            self.default_data_root = ""
        self.startup_checks()

    def datapath(self, datafile):
        return self.app_root + datafile
        
    def configpath(self, configfile):
        return self.config_root + configfile
        
    def datadirpath(self, datafile):
        return self.data_root + datafile
    
    def get_data_dir_path(self):
        return self.data_root
        
    def startup_checks(self):
        self.check_for_data_folder()
        self.check_for_config_folder()

    def check_for_data_folder(self):
        if not self.maemo:
            return
        if self.data_root == (self.user_home + "/MyDocs/DropN900/"):
            data_dir = QDir.home()
            if data_dir.cd("MyDocs"):
                if not data_dir.cd("DropN900"):
                    if data_dir.mkdir("DropN900"):
                        print ">> [INFO] Created default data dir " + str(data_dir.absolutePath()) + "/DropN900"
                    else:
                        print ">> [ERROR] Could not create default data dir 'DropN900' to " + str(data_dir.absolutePath())
            else:
                print ">> [ERROR] Could not find 'MyDocs' folder from " + str(data_dir.absolutePath())
        else:
            non_default_data_dir = QDir(self.data_root)
            if non_default_data_dir.exists():
                print ">> [INFO] Default data dir: " + self.data_root
            else:
                print ">> [WARNING] User set default data dir " + self.data_root + " does not exist, resetting to default"
                self.data_root = self.user_home + "/MyDocs/DropN900/"
                self.check_for_data_folder()

    def check_for_config_folder(self):
        if not self.maemo:
            return
        config_dir = QDir.home()
        if not config_dir.cd(".dropn900"):
            if config_dir.mkdir(".dropn900"):
                print ">> [INFO] Created config dir '.dropn900' to " + str(config_dir.absolutePath())
            else:
                print ">> [ERROR] Could not create config dir '.dropn900' to " + str(config_dir.absolutePath())

    def store_auth(self, access_token):
        if self.store_auth_to_file:
            token_config = ConfigParser()
            token_config.add_section("token")
            token_config.set("token", "secret", access_token.secret)
            token_config.set("token", "key", access_token.key)
            try:
                config_file = open(self.configpath("token.ini"), "w")
                token_config.write(config_file)
                config_file.close()
                self.logger.auth("Stored received access token")
            except IOError:
                self.logger.config("I/O error while storing received access token, file " + self.configpath("token.ini"))
        else:
            self.logger.auth("Skipping access token storing due to user settings")
        
    def reset_auth(self):
        try:
            os.remove(self.configpath("token.ini"))
            self.logger.auth("Authentication reseted")
            self.controller.ui.show_banner("Authentication reseted")
        except OSError:
            self.controller.ui.show_banner("No stored access token, could not reset authentication")
        
    def copy_url_to_clipboard(self, url):
        clipboard = QApplication.clipboard()
        clipboard.setText(url)
        self.controller.ui.show_banner("Copied " + url + " to clipboard", 3000)
        
    """ Code snipped taken from http://code.activestate.com/recipes/577081-humanized-representation-of-a-number-of-bytes/ """
    def humanize_bytes(self, bytes, precision = 1):
        abbrevs = (
            (1<<50L, 'PB'),
            (1<<40L, 'TB'),
            (1<<30L, 'GB'),
            (1<<20L, 'MB'),
            (1<<10L, 'KB'),
            (1, 'bytes')
        )
        if bytes == 1:
            return '1 byte'
        for factor, suffix in abbrevs:
            if bytes >= factor:
                break
        return '%.*f %s' % (precision, bytes / factor, suffix)


""" Parent class for all data items """

class Item:

    def __init__(self, path, root, modified, icon, has_thumb):
        self.path = path
        self.root = root
        self.format_modified(modified)
        self.icon = icon
        self.has_thumb = has_thumb
        
        self.tree_item = None
        self.load_widget = None
        self.load_animation = None
        self.public_link = None
        self.hash = None
        self.size = None

        self.format_parent()

    def get_name(self):
        return self.name

    def get_size(self):
        if self.size == None:
            return ""
        else:
            return self.size

    """ This may seem a bit difficult of an approach, let me explain:
        We get english names for months from dropbox, this will get us into localization problems
        if the device has != english as language. We form same kind of timestamps that we get from maemo os module.
        This way we can compare timestamps directly when syncing """
    def format_modified(self, modified):
        if modified == "":
            self.modified = modified
            return

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        # Strinp timezone (always +0000) and name of day
        modified = modified.split(" +")[0]
        modified = modified[5:]
        
        # Split timestamp to elements
        modified_split = modified.split(" ")
        if len(modified_split) == 4:
            # Get elements
            day = modified_split[0]
            month_string = modified_split[1]
            year =  modified_split[2]
            time = modified_split[3]
        else:
            print "#1 FATAL ERROR ON TIMESTAMP PARSING!"
            self.modified = "<timestamp parse error, report to app author>"
            return
            
        # Convert name of english month name to number
        try:
            month = months.index(month_string) + 1
            if month < 10:
                month = "0" + str(month)
            else:
                month = str(month)
        except IndexError:
            print "#2 FATAL ERROR ON TIMESTAMP PARSING!"
            self.modified = "<timestamp parse error, report to app author>"
            return
            
        # Form final timestamp
        self.modified = day + "." + month + "." + year + " " + time
        
    def get_modified(self):
        return self.modified
    
    def set_load_widget(self, widget, animation):
        self.load_widget = widget
        self.load_animation = animation

    def set_loading(self, loading):
        if self.load_widget == None or self.load_animation == None:
            return
        try:
            self.load_widget.setVisible(loading)
            if loading:
                self.load_widget.setMovie(self.load_animation)
                self.load_animation.start()
            else:
                self.load_animation.stop()
                self.load_widget.setMovie(None)        
        except RuntimeError:
            print "Could not stop C++ object for " + self.path + " deleted!"

    def format_parent(self):
        self.parent = ""
        for string in self.path.split("/")[0:-1]:
            self.parent += string + "/"
        self.parent = self.parent[0:-1]

    def refresh_name_data(self, path):
        self.path = path
        self.set_name()
        
""" Collection aka folder data class """

class Collection(Item):

    def __init__(self, path, modified, icon, has_thumb, root, hashcode = None):
        # Init parent class
        Item.__init__(self, path, root, modified, icon, has_thumb)

        # Init Collection params
        self.hash = hashcode
        self.items = []
        self.mime_type = "folder"
        
        self.set_name()

    def set_name(self):
        if self.path != "":
            self.name = self.path.split("/")[-1]
        else:
            if self.root == "sandbox":
                self.name = "DropN900"
            else:
                self.name = "DropBox"

    def add_item(self, item):
        self.items.append(item)

    def item_count(self):
        return len(self.items)

    def clear_items(self):
        self.items = []
    
    def get_items(self):
        return self.items

    def get_folders(self):
        folders = []
        for child in self.items:
            if child.is_folder():
                folders.append(child)
        return folders

    def get_files(self):
        files = []
        for child in self.items:
            if not child.is_folder():
                files.append(child)
        return files

    def is_folder(self):
        return True

    # For debug prints
    def __str__(self):
        print self.name
        print "  Path       : ", self.path
        print "  Name       : ", self.name
        print "  Root       : ", self.root
        print "  Item count : ", self.item_count()
        print "  Hashcode   : ", self.hash
        print "  TREE item  : ", self.tree_item
        return ""


""" Resource aka file data class """

class Resource(Item):

    def __init__(self, path, size, modified, mime_type, icon, has_thumb, root):
        # Init parent class
        Item.__init__(self, path, root, modified, icon, has_thumb)

        # Init Resource params
        self.size = size
        self.mime_type = mime_type
        
        self.set_name()
        self.format_size()

    def set_name(self):
        self.name = self.path.split("/")[-1]
        
    def format_size(self):
        i = self.size.find("MB")
        if i != -1:
            self.size = self.size[0:i] + " MB"
        i = self.size.find("KB")
        if i != -1:
            self.size = self.size[0:i] + " KB"

    def is_folder(self):
        return False
        
    def generate_public_link(self, uid):
        if uid != None:
            public_path = self.path[len("/Public"):]
            self.public_link = "http://dl.dropbox.com/u/" + uid + public_path
        else:
            self.public_link = None
    
    # For debug prints
    def __str__(self):
        print self.name
        print "  Root : ", self.root
        print "  Path : ", self.name
        print "  Size : ", self.size
        print "  Mod  : ", self.modified
        print "  Mime : ", self.mime_type
        print "  TREE item : ", self.tree_item
        return ""

