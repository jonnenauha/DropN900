
from PyQt4.QtGui import QIcon, QPixmap, QImage

""" DataParser gets data from network layer, converts
    to app format and sends onwards to ui layer """

class DataParser:

    def __init__(self, ui_handler):
        self.ui_handler = ui_handler
        self.tree_controller = ui_handler.tree_controller
        self.controller = ui_handler.controller
        self.log = self.ui_handler.controller.log

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
                    self.log("ERROR - Something went very wrong, did not find folder in parse_metada()!")
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
                        item.tree_item.setIcon(0, QIcon("ui/icons/folder_delete.png"))
                        item.tree_item.setText(1, "deleted")
                    else:
                        item.mime_type = "deleted_folder"
                else:
                    if item.tree_item != None:
                        item.tree_item.setIcon(0, QIcon("ui/icons/cancel.png"))
                        item.tree_item.setText(1, "deleted")
                    else:
                        item.mime_type = "deleted_item"
                item.modified = "deleted"
        except KeyError:
            return

    def parse_thumbnail(self, resp, image_path):
        image = QImage.fromData(resp.read())
        if image.isNull():
            self.log("ERROR - Failed to generate image from raw data for", image_path)
            self.tree_controller.thumbs[image_path] = None # So we dont come here again
            return
        pixmap = QPixmap.fromImage(image)
        self.tree_controller.thumbs[image_path] = pixmap
        self.tree_controller.update_thumbnail(True, pixmap)

    def parse_account_info(self, resp):
        if resp.status == 200:
            account_data = resp.data
            name = account_data["display_name"]
            self.ui_handler.manager_ui.label_username.setText(name)
            user_icon = QPixmap("ui/icons/user.png")
            self.ui_handler.manager_ui.label_username_icon.setPixmap(user_icon.scaled(24,24))
            self.log("Account data recieved")
        else:
            self.ui_handler.manager_ui.label_username.setText("unknown user")
            user_icon = QPixmap("ui/icons/user_white.png")
            self.ui_handler.manager_ui.label_username_icon.setPixmap(user_icon.scaled(24,24))
            self.log("Failed to fetch account data, treating as unknown user")

""" Parent class for all data items """

class Item:

    def __init__(self, path, root, modified, icon, has_thumb):
        self.path = path
        self.root = root
        self.modified = modified.split(" +")[0]
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

    def get_modified(self):
        return self.modified
    
    def set_load_widget(self, widget, animation):
        self.load_widget = widget
        self.load_animation = animation

    def set_loading(self, loading):
        try:
            if loading:
                self.load_widget.setMovie(self.load_animation)
                self.load_animation.start()
            else:
                self.load_animation.stop()
                self.load_widget.setMovie(None)
            self.load_widget.setVisible(loading)
        except RuntimeError:
            print "Could not stop C++ object for " + self.path + " deleted!"

    def format_parent(self):
        self.parent = "/"
        for string in self.path.split("/")[0:-1]:
            self.parent += string

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
