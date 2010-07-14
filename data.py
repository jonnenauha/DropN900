
from PyQt4.QtGui import QIcon, QPixmap, QImage

""" DataParser gets data from network layer, converts
    to app format and sends onwards to ui layer """

class DataParser:

    def __init__(self, ui_handler):
        self.ui_handler = ui_handler
        self.tree_controller = ui_handler.tree_controller
        self.log = self.ui_handler.controller.log

    def parse_metadata(self, data):
        if data == None:
            return

        if data["is_dir"]:
            parent_root = data["root"]
            # Find existing folder, or create root
            if data["path"] != "":
                folder = self.tree_controller.get_folder_for_path(self.tree_controller.root_folder, data["path"])
                if folder == None:
                    self.log("ERROR - Something went very wrong, did not find folder in parse_metada()!")
                    return;
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
        else:
            # Does not happen, we dont update item metadatas when double clicked, why should we?
            return

    def check_deleted(self, data, item, tree_item = None):
        # This is a bit retarded looking... meh
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

        
""" Collection aka folder data class """

class Collection:

    def __init__(self, path, modified, icon, has_thumb, root, hashcode = None):
        self.path = path
        self.hash = hashcode
        self.root = root
        self.items = []
        self.modified = modified.split(" +")[0]
        self.icon = icon
        self.has_thumb = has_thumb
        self.mime_type = "folder"

        self.set_name(path)
        self.format_parent()
        
        self.tree_item = None
        
    def set_name(self, path):
        if path != "":
            self.name = path.split("/")[-1]
        else:
            if self.root == "sandbox":
                self.name = "DropN900"
            else:
                self.name = "DropBox"

    def format_parent(self):
        self.parent = "/"
        for string in self.path.split("/")[0:-1]:
            self.parent += string
            
    def add_item(self, item):
        self.items.append(item)

    def item_count(self):
        return len(self.items)

    def clear_items(self):
        self.items = []
    
    def get_items(self):
        return self.items

    def get_name(self):
        return self.name
    
    def get_size(self):
        return ""

    def get_modified(self):
        return self.modified

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

class Resource:

    def __init__(self, path, size, modified, mime_type, icon, has_thumb, root):
        self.name = path.split("/")[-1]
        self.path = path
        self.size = size
        self.modified = modified
        self.mime_type = mime_type
        self.icon = icon
        self.has_thumb = has_thumb
        self.root = root

        self.format_size()
        self.format_modified()
        self.format_parent()

        self.tree_item = None
        self.public_link = None

    def format_size(self):
        i = self.size.find("MB")
        if i != -1:
            self.size = self.size[0:i] + " MB"
        i = self.size.find("KB")
        if i != -1:
            self.size = self.size[0:i] + " KB"

    def format_modified(self):
        self.modified = self.modified.split(" +")[0]

    def format_parent(self):
        self.parent = "/"
        for string in self.path.split("/")[0:-1]:
            self.parent += string
        
    def get_name(self):
        return self.name
    
    def get_size(self):
        return self.size

    def get_modified(self):
        return self.modified

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
