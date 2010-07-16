
import os

from threading import Thread
from data import DataParser, Collection, Resource
from PyQt4.QtCore import QObject, QTimer

""" ConnectionManager gets request from ui layer. Does there request to network
    with python threads so it wont block the main ui thread. Returs data either to
    DataParser or relays itself it to ui layer """

class ConnectionManager:

    def __init__(self, controller, ui_handler):
        self.controller = controller
        self.data_parser = DataParser(ui_handler)
        self.ui_handler = ui_handler
        self.tree_controller = ui_handler.tree_controller
        self.log = controller.log
        self.client = None

        # Init poll timer
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.thread_poller)

        # Init running threads to empty
        self.running_threads = []

    def thread_poller(self):
        for thread in self.running_threads:
            thread.join(0.01)
            if not thread.isAlive():
                if thread.callback_parameters != None:
                    thread.callback(thread.response, thread.callback_parameters)
                else:
                    thread.callback(thread.response)
                self.running_threads.remove(thread)

    def set_client(self, client):
        # Set client for usage, we are not connected
        self.client = client
        # Get account information
        self.data_parser.parse_account_info(self.client.account_info())
        # Start network thread poller
        self.poll_timer.start(100)
        # Start by fetching sandbox root contents
        self.get_metadata("/", "sandbox")
        
    def check_client(self):
        if not self.client:
            self.log("ERROR - Tried networking without a ready connection")
            return False
        else:
            return True

    def show_loading_ui(self, message, loading = True):
        self.ui_handler.show_loading_ui(message, loading)

    def hide_loading_ui(self):
        self.ui_handler.hide_loading_ui()

    def show_information(self, message, succesfull):
        self.ui_handler.show_information_ui(message, succesfull)

    def get_automated_metadata(self, folder_path, root):
        folder = self.tree_controller.get_folder_for_path(folder_path)
        if folder == None:
            return
        self.tree_controller.tree.setCurrentItem(folder.tree_item)
        self.tree_controller.start_load_anim(folder)
        # Leave for later
        #self.store_opened_folders(path)
        self.get_metadata(folder_path, root, None, True)
            
    ### METADATA HANDLERS
    def get_metadata(self, path, root, hashcode = None, automated = False):
        if not self.check_client:
            return

        if not automated:
            self.updated_open_folders = {}
            
        # Make thread
        worker = NetworkWorker()
        worker.set_callable(self.client.metadata, root, path, 10000, hashcode)
        worker.set_callback(self.get_metadata_callback, None)
        worker.start()

        # Add thread to watch list
        self.running_threads.append(worker)
        
    def get_metadata_callback(self, resp):
        tree_item = None
        if resp != None:
            if resp.status != 304: # content hasn't changed
                if resp.status == 200: # ok
                    tree_item = self.data_parser.parse_metadata(resp.data, self.updated_open_folders)
                else:
                    self.log("NETWORK ERROR "+str(resp.status)+" - Could not fetch metadata")
                    self.log(">> ", resp.body)
                    self.show_information("Metadata fetch failed, network error", False)
        else:
            self.show_information("Metadata fetch failed, internal error", False)

        # Got new metadata ui was updated
        tree_controller = self.ui_handler.tree_controller
        if tree_item != None: 
            tree_controller.stop_load_anim(tree_item)
        # Content not changed or error fetching
        else:
           tree_controller.stop_all_load_anims()

    def store_opened_folders(self, path):
        self.updated_open_folders = {}
        folder = self.tree_controller.get_folder_for_path(path)
        if folder != None:
            for child_folder in folder.get_folders():
                if child_folder.tree_item.isExpanded():
                    self.updated_open_folders[child_folder.get_name()] = child_folder.path
        else:
            self.log("ERROR - Could not find tree item for path", path)

    ### GET THUMBNAIL HANDLERS
    def get_thumbnail(self, path, root, size):
        if not self.check_client:
            return

        image_name = path.split("/")[-1]
        self.show_loading_ui("Loading preview of " + image_name)
        
        # Make thread
        worker = NetworkWorker()
        worker.set_callable(self.client.thumbnail, root, path, size)
        worker.set_callback(self.get_thumbnail_callback, path)
        worker.start()

        # Add thread to watch list
        self.running_threads.append(worker)

    def get_thumbnail_callback(self, resp, params):
        # Check response and first param that is the image path
        if resp != None and params[0] != None:
            image_path = params[0]
            self.hide_loading_ui()
            if resp.status == 200:
                self.data_parser.parse_thumbnail(resp, image_path)
            else:
                self.log("NETWORK ERROR "+str(resp.status)+" - Could not fetch thumbnail for", image_path)
                self.log(">> Reason:", resp.read())
                self.show_information("Thumbnail fetch failed, network error", False)
        else:
            self.hide_loading_ui()
            self.show_information("Thumbnail fetch failed, internal error", False)

    ### GET FILE HANDLERS
    def get_file(self, path, root, store_path):
        file_name = path.split("/")[-1]
        self.show_loading_ui("Downloading file " + file_name)
        
        # Make thread
        worker = NetworkWorker()
        worker.set_callable(self.client.get_file, root, path)
        worker.set_callback(self.get_file_callback, store_path, file_name)
        worker.start()

        # Add thread to watch list
        self.running_threads.append(worker)
        
    def get_file_callback(self, resp, params):
        if resp != None and params[0] != None and params[1] != None:
            store_path = params[0]
            file_name = params[1]
            self.hide_loading_ui()
            if resp.status == 200:
                try:
                    f = open(store_path, "wb")
                    f.write(resp.read())
                    f.close()
                    self.show_information("Download of " + file_name + " completed", True)
                except IOError:
                    self.show_information("Could not open " + store_path + " for store operation", False)
            else:
                self.log("NETWORK ERROR "+str(resp.status)+" - Could not download file to", store_path)
                self.log(">> Reason:", resp.read())
                self.show_information("Download failed, network error", False)
        else:
            self.hide_loading_ui()
            self.show_information("Download failed, internal error", False)

    ### UPLOAD FILE HANDLERS
    def upload_file(self, path, root, local_file_path):
        # Get info for ui and show loading ui
        if root == "sandbox":
            root_name = "DropN900"
        elif root == "dropbox":
            root_name = "DropBox"
        else:
            self.log("ERROR - Upload file path/root parse error! Cannot continue.")
            return
        file_name = local_file_path.split("/")[-1]
        self.show_loading_ui("Uploading file " + file_name + "\nto " + root_name + path)

        # Open file for lib
        try:
            file_obj = open(local_file_path, "rb")
        except IOError:
            self.hide_loading_ui()
            self.log("ERROR - Could not open " + local_file_path + " file for uploading. Aborting")
            self.show_information("Could not open " + local_file_path + " file for uploading", False)
            return
        
        # Make thread
        worker = NetworkWorker()
        worker.set_callable(self.client.put_file, root, path, file_obj)
        worker.set_callback(self.upload_file_callback, root, path, file_name)
        worker.start()

        # Add thread to watch list
        self.running_threads.append(worker)

    def upload_file_callback(self, resp, params):
        if resp != None and params[0] != None and params[1] != None and params[2] != None:
            root = params[0]
            store_path = params[1]
            file_name = params[2]
            self.hide_loading_ui()
            if resp.status == 200:
                self.get_automated_metadata(store_path, root)
                self.show_information("Upload of " + file_name + " completed", True)
            else:
                self.log("NETWORK ERROR "+str(resp.status)+" - Upload of " + params[0] + " to " + store_path + "failed.")
                self.log(">> Reason:", resp.body)
                self.show_information("Upload of " + file_name + " failed, network error", False)
        else:
            self.hide_loading_ui()
            self.show_information("Upload failed, internal error", False)

    ### RENAME HANDLERS
    def rename(self, root, from_path, to_path, data):
        # Start rename loading anim
        data.set_loading(True)

        # Parse names from paths
        old_name = from_path.split("/")[-1]
        new_name = to_path.split("/")[-1]

        # Make thread
        worker = NetworkWorker()
        worker.set_callable(self.client.file_move, root, from_path, to_path)
        worker.set_callback(self.rename_callback, old_name, new_name, data)
        worker.start()

        # Add thread to watch list
        self.running_threads.append(worker)

    def rename_callback(self, resp, params):
        if resp != None and params[0] != None and params[1] != None and params[2] != None:
            old_name = params[0]
            new_name = params[1]
            data = params[2]
            # Set new name to tree item
            if resp.status == 200:
                data.refresh_name_data(resp.data["path"])
                data.tree_item.setText(0, new_name)
                self.show_information("Renamed " + old_name + " succesfully", True)
            else:
                self.log("NETWORK ERROR "+str(resp.status)+" - Renaming failed.")
                self.log(">> Reason:", resp.body)
                self.show_information("Renaming of " + old_name + " failed, network error", False)
            # Stop rename loading anim
            data.set_loading(False)
        else:
            self.show_information("Renaming failed, internal error", False)

    ### REMOVE HANDLERS
    def remove_file(self, root, path, update_path, is_folder):
        # Show loading ui
        file_name = path.split("/")[-1]
        keywork = "file" if not is_folder else "folder"
        self.show_loading_ui("Removing " + keywork + " " + file_name)
        
        # Make thread
        worker = NetworkWorker()
        worker.set_callable(self.client.file_delete, root, path)
        worker.set_callback(self.remove_file_callback, root, update_path, file_name, is_folder)
        worker.start()

        # Add thread to watch list
        self.running_threads.append(worker)

    def remove_file_callback(self, resp, params):
        if resp != None and params[0] != None and params[1] != None and params[2] != None and params[3] != None:
            root = params[0]
            update_path = params[1]
            removed_file = params[2]
            is_folder = params[3]
            keyword = "file " if not is_folder else "folder "
            self.hide_loading_ui()
            if resp.status == 200:
                self.get_automated_metadata(update_path, root)
                self.show_information("Removed " + keyword + removed_file + " succesfully", True)
            else:
                self.log("NETWORK ERROR "+str(resp.status)+" - Removing " + keyword + removed_file + " from " + update_path + " failed.")
                self.log(">> Reason:", resp.body)
                self.show_information("Removing of " + keyword + removed_file + " failed, network error", False)
        else:
            self.hide_loading_ui()
            self.show_information("Removing of file or folder failed, internal error", False)

    ### NEW FOLDER HANDLERS

    def create_folder(self, root, full_create_path, folder_name, update_path):
        # Show loading ui
        if update_path == "":
            if root == "sandbox":
                self.show_loading_ui("Creating folder " + folder_name + "\nto DropN900")
            else:
                self.show_loading_ui("Creating folder " + folder_name + "\nto DropBox")
        else:
            self.show_loading_ui("Creating folder " + folder_name + "\nto " + update_path)
        
        # Make thread
        worker = NetworkWorker()
        worker.set_callable(self.client.file_create_folder, root, full_create_path)
        worker.set_callback(self.create_folder_callback, root, full_create_path, folder_name, update_path)
        worker.start()

        # Add thread to watch list
        self.running_threads.append(worker)
        
    def create_folder_callback(self, resp, params):
        if resp != None and params[0] != None and params[1] != None and params[2] != None and params[3] != None:
            root = params[0]
            full_create_path = params[1]
            folder_name = params[2]
            update_path = params[3]
            self.hide_loading_ui()
            if resp.status == 200:
                self.get_automated_metadata(update_path, root)
                self.show_information("Created folder " + folder_name + " succesfully", True)
            else:
                self.log("NETWORK ERROR "+str(resp.status)+" - Could not create folder " + full_create_path)
                self.log(">> Reason:", resp.body)
                self.show_information("Creating folder " + folder_name + " failed, network error", False)
        else:
            self.hide_loading_ui()
            self.show_information("Creating folder failed, internal error", False)
        

""" NetworkWorker is a simple thread subclass that will do networking.
    Set method with arguments. Set callback function that will be called with self.response
    and start() """

class NetworkWorker(Thread):

    def __init__(self):
        Thread.__init__(self)
        
        self.method = None
        self.parameters = None
        self.callback = None
        self.callback_parameters = None
        self.response = None

    def set_callable(self, method, *parameters):
        self.method = method
        self.parameters = parameters

    def set_callback(self, callback, *parameters):
        self.callback = callback
        if parameters[0] != None:
            self.callback_parameters = parameters
        else:
            self.callback_parameters= None

    def run(self):
        self.response = self.method(*self.parameters)
