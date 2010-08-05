
import os

from httplib import socket 
from threading import Thread
from collections import deque

from PyQt4.QtCore import QObject, QTimer
from data import DataParser, Collection, Resource
from dbusmanager import DBusMonitor

""" ConnectionManager gets request from ui layer. Does there request to network
    with python threads so it wont block the main ui thread. Returs data either to
    DataParser or relays itself it to ui layer """

class ConnectionManager(QObject):

    def __init__(self, controller, ui_handler, logger):
        QObject.__init__(self)
        self.controller = controller
        self.data_parser = DataParser(ui_handler, logger)
        self.ui_handler = ui_handler
        self.tree_controller = ui_handler.tree_controller
        self.logger = logger
        self.client = None
        self.transfer_manager = None

        # Init poll timer
        self.poll_timer = QTimer(self)
        self.poll_timer.timeout.connect(self.thread_poller)

        # Init thread params
        self.running_threads = []
        self.queued_threads = []
        self.active_data_worker = None
        self.data_workers = deque()
        
        # DBus manager
        self.dbus_monitor = DBusMonitor(self, logger)
        
        # Start the thread poller
        self.poll_timer.start(100)
    
    def set_transfer_manager(self, transfer_manager):
        self.transfer_manager = transfer_manager
    
    def check_data_workers(self):
        # Start next data worker if available
        if self.active_data_worker == None:
            try:
                worker = self.data_workers.popleft()
                worker.start()
                self.active_data_worker = worker
            except IndexError:
                self.active_transfer = None
    
    def thread_poller(self):
        # Check for completed network threads
        if len(self.running_threads) > 0:
            removable_network_threads = []
            for thread in self.running_threads:
                thread.join(0.01)
                if not thread.isAlive():
                    if thread.error != None:
                        # If tree exists, lets store the request and do it again
                        # when a connection is available
                        if self.tree_controller.root_folder != None:
                            self.queued_threads.append(thread)
                        # Request a connection only once
                        if len(self.queued_threads) == 1:
                            self.request_connection()
                    if thread.response != None:
                        if thread.callback_parameters != None:
                            thread.callback(thread.response, thread.callback_parameters)
                        else:
                            thread.callback(thread.response)
                    removable_network_threads.append(thread)  
            for removable in removable_network_threads:
                self.running_threads.remove(removable)
                del removable
                
        # Check for active data worker
        if self.active_data_worker != None:
            self.active_data_worker.join(0.01)
            if not self.active_data_worker.isAlive():
                if self.active_data_worker.error != None:
                    self.logger.error("DataWorker error: " + self.active_data_worker.error)
                self.active_data_worker = None
                self.check_data_workers()
                    
    def request_connection(self):
        self.dbus_monitor.request_connection()
        
    def connection_available(self):
        return self.dbus_monitor.device_has_networking
    
    def connection_is_wlan(self):
        if not self.connection_available():
            return False
        bearer = self.dbus_monitor.bearer
        if bearer == None:
            return False
        if bearer.startswith("WLAN"):
            return True
        else:
            return False
            
    def set_connected(self, connected):
        if connected:
            self.ui_handler.hide_loading_ui()
            if self.controller.login_done == False:
                self.controller.start_trusted_auth()
                trusted_login_ui = self.ui_handler.trusted_login_ui
                if trusted_login_ui.line_edit_email.text().isEmpty() == False and trusted_login_ui.line_edit_password.text().isEmpty() == False:
                    self.logger.network("Network connection established, starting authentication")
                    self.ui_handler.try_trusted_login()
            elif self.controller.connected == True and self.client != None:
                if len(self.queued_threads) > 0:
                    self.ui_handler.show_information_ui("Connection established, fetching queued tasks", True)
                    self.logger.network("Network connection established, starting queued networking")
                    for queued_thread in self.queued_threads:
                        worker = NetworkWorker()
                        worker.clone(queued_thread)
                        worker.start()
                        self.running_threads.append(worker)
                    self.queued_threads = []
                else:
                    self.ui_handler.show_information_ui("Connection established, fetching content", True)
                    self.logger.network("Network connection established, fetching root metadata")
                    self.get_account_data()
                    self.get_metadata("/", "dropbox")
        else:
            self.ui_handler.show_loading_ui("Waiting for a connection...", True)
    
    def set_client(self, client):
        # Set client for usage, we are not connected
        self.client = client
        self.transfer_manager.set_client(client)
        # Get account information
        if self.connection_available():
            if self.get_account_data():
                # Start by fetching sandbox root contents
                self.get_metadata("/", "dropbox")
            else:
                self.ui_handler.show_loading_ui("Waiting for a connection...", True)
                self.request_connection()
        else:
            self.ui_handler.show_loading_ui("Waiting for a connection...", True)
            self.request_connection()

    def get_account_data(self):
        try:
            self.data_parser.parse_account_info(self.client.account_info())
            return True
        except (socket.error, socket.gaierror), err:
            return False
    
    def check_client(self):
        if not self.client:
            self.logger.network_error("Tried networking without a ready connection")
            return False
        else:
            return True

    def show_loading_ui(self, message, loading = True):
        self.ui_handler.show_loading_ui(message, loading)

    def hide_loading_ui(self):
        self.ui_handler.hide_loading_ui()

    def show_information(self, message, succesfull, timeout = 4000):
        self.ui_handler.show_information_ui(message, succesfull, timeout)

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
                    self.logger.network_error(str(resp.status) + " - Could not fetch metadata")
                    self.logger.network_error(">> ", resp.body)
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
            self.logger.error("Could not find tree item for path", path)

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
                self.logger.network_error(str(resp.status) + " - Could not fetch thumbnail for", image_path)
                self.logger.network_error(">> Reason:", resp.read())
                self.show_information("Thumbnail fetch failed, network error", False)
        else:
            self.hide_loading_ui()
            self.show_information("Thumbnail fetch failed, internal error", False)

    ### GET FILE HANDLERS
    def get_file(self, path, root, store_path, size, mime_type, sync_download = False):
        if not self.check_client:
            return
        file_name = path.split("/")[-1]
        dropbox_path = path[0:path.rfind("/")]
        if sync_download == False:
            self.show_information("Download queued\n" + file_name, None, 4000)
        self.transfer_manager.handle_download(path, root, file_name, dropbox_path, store_path, size, mime_type, sync_download)
        
    def get_file_callback(self, resp, data, params):
        if resp != None and params[0] != None and params[1] != None:
            store_path = params[0]
            file_name = params[1]
            if resp.status == 200:
                store_worker = DataWorker("store")
                store_worker.setup_store(store_path, data)
                self.data_workers.append(store_worker)
                self.check_data_workers()
            else:
                self.logger.network_error(str(resp.status) + " - Could not download file to", store_path)
                self.logger.network_error(">> Reason:", resp.read())
        else:
            self.logger.error("Download failed, internal error")

    ### UPLOAD FILE HANDLERS
    def upload_file(self, path, root, local_file_path):
        if not self.check_client:
            return
 
        # Get info for ui
        if root == "sandbox":
            root_name = unicode("DropN900", "utf-8")
        elif root == "dropbox":
            root_name = unicode("DropBox", "utf-8")
        else:
            self.logger.error("Upload file path/root parse error! Cannot continue.")
            return
        file_name = local_file_path.split("/")[-1]
        folder_path = local_file_path[0:local_file_path.rfind("/")]

        # Open file for lib
        try:
            file_obj = open(local_file_path.encode("utf-8"), "rb")
        except IOError:
            self.logger.error("Could not open " + local_file_path + " file. Aborting upload.")
            self.show_information("Could not open " + local_file_path + " file for uploading", False)
            return
        
        self.show_information("Upload queued\n" + file_name, None, 4000)
        self.transfer_manager.handle_upload(path, root, file_obj, file_name, folder_path, root_name + path, local_file_path)

    def upload_file_callback(self, resp, params):
        if resp != None and params[0] != None and params[1] != None and params[2] != None:
            root = params[0]
            store_path = params[1]
            file_name = params[2]
            if resp.status == 200:
                self.get_automated_metadata(store_path, root)
            else:
                self.logger.network_error(str(resp.status) + " - Upload of " + params[0] + " to " + store_path + " failed.")
                self.logger.network_error(">> Reason:", resp.body)
        else:
            self.logger.error("Upload failed, internal error")

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
                self.logger.network_error(str(resp.status) + " - Renaming failed.")
                self.logger.network_error(">> Reason:", resp.body)
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
                self.logger.network_error(str(resp.status) + " - Removing " + keyword + removed_file + " from " + update_path + " failed.")
                self.logger.network_error(">> Reason:", resp.body)
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
                self.logger.network_error(str(resp.status) + " - Could not create folder " + full_create_path)
                self.logger.network_error(">> Reason:", resp.body)
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
        self.error = None
        
    def clone(self, worker):
        self.method = worker.method
        self.parameters = worker.parameters
        self.callback = worker.callback
        self.callback_parameters = worker.callback_parameters
                        
    def set_callable(self, method, *parameters):
        self.method = method
        self.parameters = parameters

    def set_callback(self, callback, *parameters):
        self.callback = callback
        if parameters[0] != None:
            self.callback_parameters = parameters
        else:
            self.callback_parameters= None

    def encode_unicode(self, obj, encoding = "utf-8"):
        if isinstance(obj, basestring):
            if isinstance(obj, unicode):
                return obj.encode(encoding)
        return obj
    
    def run(self):
        encoded_params = []
        for param in self.parameters:
            param = self.encode_unicode(param)
            encoded_params.append(param)

        try:
            self.response = self.method(*tuple(encoded_params))
        except (socket.error, socket.gaierror), err:
            self.response = None
            self.error = err

""" DataWorker is a simple thread subclass that does file writing, this way the main thread can run at peace """

class DataWorker(Thread):

    def __init__(self, action):
        Thread.__init__(self)
        self.action = action
        self.file_path = None
        self.data = None
        self.error = None
        
    def setup_store(self, file_path, data):
        self.file_path = file_path
        self.data = data
        
    def run(self):
        if self.action == "store":
            try:
                if self.data != None:
                    f = open(self.file_path.encode("utf-8"), "wb")
                    f.write(self.data)
                    f.close()
                else:
                    self.error = "Data is 'None' skipping file " + self.file_path
            except IOError, e:
                self.error = "Could not open " + self.file_path + " for file I/O: " + str(e)

