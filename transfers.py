
import os
import time

from collections import deque

from PyQt4.QtGui import QWidget, QPixmap, QMovie
from PyQt4.QtCore import Qt, QTimer, QDateTime, QSize, QDir

from data import Collection, Resource
from connectionmanager import NetworkWorker
from ui.ui_transferwidget import Ui_TransferWidget
from ui.ui_transferitem import Ui_TransferItem

""" Sync manager handles manual and automatic syncs """

class SyncManager:

    def __init__(self, controller):
        self.datahandler = controller.datahandler
        self.config_helper = controller.config_helper
        self.ui = controller.ui
        self.logger = controller.logger
        self.connection = controller.connection
    
        # Init poll timer
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.thread_poller)
        
        # Active metadata fetch
        self.active_metadata_thread = None
        self.sync_metadata = None
        
    def setup_automatic_sync(self):
        pass
        
    def thread_poller(self):
        if self.active_metadata_thread == None:
            self.poll_timer.stop()
            return
        self.active_metadata_thread.join(0.01)
        if not self.active_metadata_thread.isAlive():
            if self.active_metadata_thread.error != None:
                self.ui.show_banner("Sync error, check log")
                self.logger.sync_error("Could not complete sync, network errors")
            self.sync_parse_response(self.active_metadata_thread.response)
            del self.active_metadata_thread
            self.active_metadata_thread = None
                    
    def sync_now(self, sync_path):
        if sync_path == "" or sync_path == "/":
            self.ui.show_banner("Cannot synchronize, path / invalid")
            self.logger.sync("Cannot synchronize, path / invalid")
            return
        if sync_path == "None":
            self.ui.show_banner("Synchronizing disabled from settings", 2000)
            return 
        if sync_path[0] != "/":
            self.ui.show_banner("Cannot synchronize, path '" + sync_path + "' invalid")
            self.logger.sync("Cannot synchronize, path '" + sync_path + "' invalid")
            return
        if self.connection.connection_available() == False:
            self.ui.show_banner("Cannot synchronize, no network connection")
            self.logger.sync("Cannot synchronize, no network connection")
            return
        if self.active_metadata_thread != None:
            self.ui.show_banner("Synchronizing already in progress")
            self.logger.sync("Synchronizing already in progress")
            return
        dir_check = QDir(self.datahandler.get_data_dir_path())
        if not dir_check.exists():
            self.ui.show_note("Cannot synchronize, destination " + self.datahandler.get_data_dir_path() + " does not exist. Please set a new folder in settings.")
            return
        
        self.ui.show_banner("Synchronizing, please wait...", 2000)
        self.logger.sync("Start: Fetching metadata for " + sync_path)
  
        # Make metadata fetch thread
        metadata_worker = NetworkWorker()
        metadata_worker.set_callable(self.connection.client.metadata, "dropbox", sync_path, 10000, None)
        metadata_worker.start()
    
        # Start monitoring completion
        self.active_metadata_thread = metadata_worker
        self.poll_timer.start(100)
        
    def sync_parse_response(self, response):
        if response != None:
            if response.status == 304: # content hasn't changed
                self.logger.sync("Completed: Nothing to sync, content hash same")
                return
            if response.status == 200: # ok
                sync_file_list = self.parse_metadata(response.data)
                if sync_file_list == None:
                    self.ui.show_banner("Fatal sync error")
                    return
                if len(sync_file_list) == 0:
                    self.ui.show_banner("Nothing to sync, all files up to date")
                    self.logger.sync("Completed: Nothing to sync, all files up to date")
                else:
                    file_count = str(len(sync_file_list))
                    post_count = " file" if file_count == "1" else " files"
                    self.ui.show_banner("Synchronizing " + file_count + post_count)
                    self.logger.sync("Starting " + file_count + " sync downloads")
                    store_dir = self.datahandler.get_data_dir_path()
                    for sync_file in sync_file_list:
                        self.connection.get_file(sync_file.path, sync_file.root, store_dir + sync_file.get_name(), sync_file.size, True)
                    self.ui.show_transfer_widget()
            else: # path invalid
                self.logger.sync_error("Could not fetch metadata for sync path, stopping sync")
        
    def parse_metadata(self, data):
        try:
            if data["is_dir"]:        
                parent_root = data["root"]
                folder = Collection(data["path"], data["modified"], data["icon"], data["thumb_exists"], parent_root, data["hash"])
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
            else:
                self.ui.show_banner("Sync error, check log")
                self.logger.sync_error("Sync path is not a folder, stopping sync")
                return
        except Exception, e:
            self.ui.show_banner("Sync error, check log")
            self.logger.sync_error("Parsing sync path metadata failed: " + str(e))
            return
                
        self.sync_metadata = folder
        download_list = []    
        for child_file in self.sync_metadata.get_files():
            try:
                local_path = self.datahandler.datadirpath(child_file.get_name())
                if os.path.exists(local_path):
                    device_modified = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(os.path.getmtime(local_path)))
                    if self.is_remote_newer(device_modified, child_file.modified):
                        download_list.append(child_file)
                else:
                    download_list.append(child_file)
            except OSError, e:
                print e
        return download_list

    def is_remote_newer(self, local_modified, remote_modified):
        ldata = self.parse_timestamp(local_modified)
        rdata = self.parse_timestamp(remote_modified)
        
        k = "year"
        if rdata[k] > ldata[k]:
            return True
        elif rdata[k] == ldata[k]:
            k = "month"
        else:
            return False
        if rdata[k] > ldata[k]:
            return True
        elif rdata[k] == ldata[k]:
            k = "day"
        else:
            return False
        if rdata[k] > ldata[k]:
            return True
        elif rdata[k] == ldata[k]:
            k = "hour"
        else:
            return False
        if rdata[k] > ldata[k]:
            return True
        elif rdata[k] == ldata[k]:
            k = "min"
        else:
            return False
        if rdata[k] > ldata[k]:
            return True
        elif rdata[k] == ldata[k]:
            k = "sec"
        else:
            return False
        if rdata[k] > ldata[k]:
            return True
        elif rdata[k] == ldata[k]:
            return False
        else:
            return False
        return False
            
    def parse_timestamp(self, timestamp):
        main_parts = timestamp.split(" ")
        date_parts = main_parts[0].split(".")
        time_parts = main_parts[1].split(":")
        
        data = {}
        data["day"]   = int(date_parts[0])
        data["month"] = int(date_parts[1])
        data["year"]  = int(date_parts[2])
        data["hour"]  = int(time_parts[0])
        data["min"]   = int(time_parts[1])
        data["sec"]   = int(time_parts[2])
        return data
    
""" TransferManager monitors upload/downloads and relays info to TransferWidget """

class TransferManager:

    def __init__(self, controller):
        self.datahandler = controller.datahandler
        self.config_helper = controller.config_helper
        self.ui = controller.ui
        self.logger = controller.logger
        self.connection = controller.connection
        
        self.connection.set_transfer_manager(self)
        self.client = None
        
        # UI interactions
        self.show_loading_ui = self.connection.show_loading_ui
        self.show_information = self.connection.show_information
        
        # Init poll timer
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.thread_poller)
        
        # Init thread monitoring
        self.active_transfer = None
        self.queued_transfer_threads = deque()
        
        # Tranfer to ui item dict
        self.tranfer_to_widget = {}

    def set_client(self, client):
        self.client = client
        
    def set_transfer_widget(self, transfer_widget):
        self.transfer_widget = transfer_widget
        
    def start_poller(self, timeout_msec = 100):
        self.poll_timer.start(timeout_msec)
        
    def stop_poller(self):
         self.poll_timer.stop()

    def thread_poller(self):
        if self.active_transfer == None:
            self.stop_poller()
            return
        self.active_transfer.join(0.01)
        if not self.active_transfer.isAlive():
            if self.active_transfer.error != None:
                try:
                    self.tranfer_to_widget[self.active_transfer].set_failed()
                except KeyError:
                    self.logger.warning("Could not find widget for failed transfer")
                self.logger.transfer_error(self.active_transfer.transfer_type + " of " + self.active_transfer.file_name + " failed, no connection?")
                self.logger.transfer_error(">>" + str(self.active_transfer.error))
            transfer = self.active_transfer
            self.active_transfer = None
            self.check_transfer_queue()
            if transfer.response != None:
                try:
                    self.tranfer_to_widget[transfer].set_completed()
                except KeyError:
                    self.logger.warning("Could not find widget for completed transfer")
                if transfer.callback_parameters != None:
                    transfer.callback(transfer.response, transfer.callback_parameters)
                else:
                    transfer.callback(transfer.response)
            del transfer

    def check_transfer_queue(self):
        if self.active_transfer == None:
            try:
                self.active_transfer = self.queued_transfer_threads.popleft()
                self.active_transfer.start()
                self.start_poller()
                self.tranfer_to_widget[self.active_transfer].set_started()
            except IndexError:
                self.active_transfer = None
                self.stop_poller()
            except KeyError:
                self.logger.warning("Could not find widget for started transfer")
                
    def handle_download(self, path, root, file_name, dropbox_path, device_store_path, size, sync_download):
        download = TransferWorker("Download")
        download.set_callable(self.client.get_file, root, path)
        download.set_callback(self.connection.get_file_callback, device_store_path, file_name)
        download.set_download_info(file_name, device_store_path)
        
        device_path = device_store_path[0:device_store_path.rfind("/")]
        download_item = self.transfer_widget.add_download(file_name, dropbox_path, device_path, size, sync_download)
        self.tranfer_to_widget[download] = download_item
        
        self.queued_transfer_threads.append(download)
        self.check_transfer_queue()
        
    def handle_upload(self, path, root, file_obj, file_name, from_local_path, dropbox_store_path, local_file_path):
        upload = TransferWorker("Upload")
        upload.set_callable(self.client.put_file, root, path, file_obj)
        upload.set_callback(self.connection.upload_file_callback, root, path, file_name)
        upload.set_upload_info(file_name, dropbox_store_path)
        try:
            size = self.datahandler.humanize_bytes(os.path.getsize(local_file_path))
        except:
            size = ""
        upload_item = self.transfer_widget.add_upload(file_name, from_local_path, dropbox_store_path, size)
        self.tranfer_to_widget[upload] = upload_item
        
        self.queued_transfer_threads.append(upload)
        self.check_transfer_queue()


""" TransferWorker is a subclass of NetworkWorker, 
    as addition it has more information about the download/upload task """
    
class TransferWorker(NetworkWorker):

    def __init__(self, transfer_type):
        NetworkWorker.__init__(self)
        self.transfer_type = transfer_type
        self.file_name = None
        self.store_path = None

    def set_download_info(self, file_name, device_store_path):
        self.file_name = file_name
        self.store_path = device_store_path
        
    def set_upload_info(self, file_name, dropbox_store_path):
        self.file_name = file_name
        self.store_path = dropbox_store_path

        
""" TransferWidget is a tranfer monitoring widget """

class TransferWidget(QWidget):

    def __init__(self, transfer_manager):
        QWidget.__init__(self, transfer_manager.ui.main_widget, Qt.Window)
        self.setAttribute(Qt.WA_Maemo5StackedWindow)
        self.ui = Ui_TransferWidget()
        self.ui.setupUi(self)
        
        self.transfer_manager = transfer_manager
        self.datahandler = transfer_manager.datahandler
        self.logger = transfer_manager.logger
        
        self.icon_download = QPixmap(self.datahandler.datapath("ui/icons/item_download.png"))
        self.icon_upload = QPixmap(self.datahandler.datapath("ui/icons/item_upload.png"))
        self.icon_sync = QPixmap(self.datahandler.datapath("ui/icons/item_sync.png"))
        self.icon_ok = QPixmap(self.datahandler.datapath("ui/icons/item_ok.png"))
        self.icon_error = QPixmap(self.datahandler.datapath("ui/icons/item_error.png")) 
               
    def showEvent(self, show_event):
        if self.ui.item_layout.count() > 2:
            if self.ui.label_first_time_note.isVisible():
                self.ui.label_first_time_note.hide()
        QWidget.showEvent(self, show_event)
        
    def add_download(self, filename, from_path, to_path, size, sync_download):
        download_item = TransferItem(self, "Download", sync_download)
        download_item.set_icon(self.icon_download, True)
        download_item.set_information(filename, from_path, to_path, size)
        
        self.ui.item_layout.insertWidget(0, download_item)
        return download_item
        
    def add_upload(self, filename, from_path, to_path, size):
        upload_item = TransferItem(self, "Upload", False)
        upload_item.set_icon(self.icon_upload, True)
        upload_item.set_information(filename, from_path, to_path, size)

        self.ui.item_layout.insertWidget(0, upload_item)
        return upload_item
        
        
""" TransferItem is a custom list widget that shows tranfer data """

class TransferItem(QWidget):

    def __init__(self, parent, transfer_type, sync_transfer):
        QWidget.__init__(self)
        self.ui = Ui_TransferItem()
        self.ui.setupUi(self)
        self.parent = parent
        
        self.generate_timestamp(QDateTime.currentDateTime())
        self.status_style = "font-size: 12pt; color: "
        self.transfer_type = transfer_type
        self.set_status("Waiting")
        
        self.loading_animation = QMovie(self.parent.datahandler.datapath("ui/images/loading.gif"), "GIF")
        self.loading_animation.setCacheMode(QMovie.CacheAll)
        self.loading_animation.setScaledSize(QSize(48,48))
        self.initial_pixmap = None

        self.duration_timer = QTimer()
        self.duration_timer.timeout.connect(self.set_duration)
        self.duration_sec = 0
        self.duration_min = 0
        
        self.ui.label_duration.hide()
        self.ui.label_sep.hide()
        
        self.sync_transfer = sync_transfer
        if self.sync_transfer:
            self.ui.sync_icon.setPixmap(self.parent.icon_sync)
            self.ui.content_frame.setStyleSheet("QFrame#content_frame{border: 0px;border-bottom: 1px solid grey;background-color: qlineargradient(spread:pad, x1:0, y1:0.466182, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255), stop:0.462312 rgba(11, 11, 64, 255), stop:1 rgba(22, 22, 22, 255));}")
        else:
            self.ui.sync_icon.hide()

    def set_information(self, filename, from_path, to_path, size):
        self.ui.label_filename.setText(filename)
        self.ui.label_from.setText(from_path)        
        self.ui.label_to.setText(to_path)
        self.ui.label_size.setText(size)
        self.ui.label_duration.setText("Under 1 sec")
        if size == "":
            self.ui.label_size.hide()
            self.ui.label_sep.hide()
        
    def set_duration(self):
        self.duration_sec += 1
        if self.duration_sec == 60:
            self.duration_min += 1
            self.duration_sec = 0
        if self.duration_min > 0 and self.duration_sec < 10:
            duration = "0" + str(self.duration_sec) + " sec"
        else:
            duration = str(self.duration_sec) + " sec"
        if self.duration_min > 0:
            duration = str(self.duration_min) + " min " + duration
        self.ui.label_duration.setText(duration)
    
    def generate_timestamp(self, date_time_now):
        self.ui.label_timestamp.setText(date_time_now.toString("dd.MM.yyyy HH:mm:ss"))   
        
    def set_icon(self, pixmap, initial_set = False):
        self.ui.main_icon.setPixmap(pixmap)
        if initial_set:
            self.initial_pixmap = pixmap
        
    def start_animation(self):
        self.ui.main_icon.setMovie(self.loading_animation)
        self.loading_animation.start()
        self.duration_sec = 0
        self.duration_min = 0
        self.ui.label_duration.show()
        if not self.ui.label_size.text().isEmpty():
            self.ui.label_sep.show()
        self.duration_timer.start(1000)
        
    def stop_animation(self):
        self.loading_animation.stop()
        self.ui.main_icon.setMovie(None)
        self.duration_timer.stop()
        
    def set_status(self, status, color = "rgb(218,218,218);"):
        self.ui.label_status.setText(status)
        self.ui.label_status.setStyleSheet(self.status_style + color)
        
    def set_started(self, status = None, color = "rgb(255,255,255);"):
        if status == None:
            status = self.transfer_type + "ing"
        self.set_status(status, color)
        self.start_animation()
        
    def set_completed(self, status = None, color = "rgb(94,189,0);"):
        if status == None:
            status = self.transfer_type + " completed"
        if self.sync_transfer:
            status = "Sync " + status.lower()
            color = "#6798cb;"
        self.set_status(status, color)       
        self.stop_animation()
        self.set_icon(self.initial_pixmap)
        self.ui.content_frame.setStyleSheet("QFrame#content_frame{border: 0px;border-bottom: 1px solid grey;background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 7, 0, 255), stop:0.502513 rgba(0, 50, 0, 200), stop:1 rgba(0, 0, 0, 255));}")

    def set_failed(self, status = None, color = "rgb(200,0,0);"):
        if status == None:
            status = self.transfer_type + " failed"
        if self.sync_transfer:
            status = "Sync " + status.lower()
        self.set_status(status, color)
        self.stop_animation()
        self.set_icon(self.parent.icon_error)
        self.ui.content_frame.setStyleSheet("QFrame#content_frame{border: 0px;border-bottom: 1px solid grey;background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 255), stop:0.512563 rgba(64, 0, 0, 255), stop:1 rgba(6, 6, 6, 255));}")
                
