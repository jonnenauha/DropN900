
import os
import time
import datetime
import simplejson
import mimetypes

from httplib import socket
from collections import deque

from PyQt4.QtGui import QMainWindow, QWidget, QMessageBox, QIcon, QPixmap, QMovie, QLabel, QScrollArea
from PyQt4.QtGui import QSpacerItem, QSizePolicy, QHBoxLayout, QVBoxLayout, QGridLayout, QFont
from PyQt4.QtCore import Qt, QObject, QTimer, QDateTime, QSize, QDir

from data import Collection, Resource
from connectionmanager import NetworkWorker
from ui.ui_transferwidget import Ui_TransferWidget
from ui.ui_transferitem import Ui_TransferItem

""" Sync manager handles manual and automatic syncs """

class SyncManager(QObject):

    def __init__(self, controller):
        QObject.__init__(self)
        self.controller = controller
        self.datahandler = controller.datahandler
        self.config_helper = controller.config_helper
        self.ui = controller.ui
        self.logger = controller.logger
        self.connection = controller.connection
           
        # Init poll timer
        self.poll_timer = QTimer(self)
        self.poll_timer.timeout.connect(self.thread_poller)
        
        # Metadata threading variables
        self.active_metadata_thread = None
        self.queued_metadata_threads = deque()
        
        # Active sync variables
        self.sync_metadata = None
        self.sync_sub_folders_left = False
        self.sync_ongoing = False
        self.sync_fetching_sync_root = True
        self.sync_root = None
        self.sync_total_results = []
        
    def check_metadata_queue(self):
        if self.active_metadata_thread == None:
            try:
                self.active_metadata_thread = self.queued_metadata_threads.popleft()
                self.active_metadata_thread.start()
                self.poll_timer.start(50)
            except IndexError:
                self.finish_sync()
                self.sync_ongoing = False
                self.active_metadata_thread = None
                self.poll_timer.stop()
                
    def thread_poller(self):
        if self.active_metadata_thread == None:
            self.poll_timer.stop()
            return
        self.active_metadata_thread.join(0.01)
        if not self.active_metadata_thread.isAlive():
            if self.active_metadata_thread.error != None:
                self.ui.show_banner("Could not complete sync, connection failed")
                self.logger.sync_error("Could not complete sync, connection failed")
            self.sync_parse_response(self.active_metadata_thread.response)
            del self.active_metadata_thread
            self.active_metadata_thread = None
            self.check_metadata_queue()
                    
    def sync_now(self, sync_path):
        if self.connection.client == None:
            self.ui.show_banner("Cannot synchronize, not connected to Dropbox")
            self.logger.sync("Cannot synchronize, no network connection")
            return
        if self.connection.connection_available() == False:
            self.ui.show_banner("Cannot synchronize, no network connection")
            self.logger.sync("Cannot synchronize, no network connection")
            return
        if self.datahandler.only_sync_on_wlan:
            if not self.connection.connection_is_wlan():
                self.ui.show_banner("Synchronizing without WLAN disabled in settings", 4000)
                return
        if len(self.controller.transfer_manager.queued_transfer_threads) > 0 or self.controller.transfer_manager.active_transfer != None:
            self.ui.show_banner("There are ongoing active transfers\nPlease wait for them to complete")
            return    
        if len(self.connection.data_workers) > 0:
            self.ui.show_banner("Data is still being written from previous downloads\nPlease wait a moment and try synchronizing again", 5000)
            return
        if self.sync_ongoing:
            self.ui.show_banner("Synchronization already in progress")
            self.logger.sync("Synchronizing already in progress")
            return
        if sync_path == "" or sync_path == "/":
            self.ui.show_banner("Cannot synchronize, path / invalid")
            self.logger.sync("Cannot synchronize, path / invalid")
            return
        if sync_path == "None":
            self.ui.show_banner("Synchronizing disabled in settings", 2000)
            return 
        if sync_path[0] != "/":
            self.ui.show_banner("Cannot synchronize, path '" + sync_path + "' invalid")
            self.logger.sync("Cannot synchronize, path '" + sync_path + "' invalid")
            return
        dir_check = QDir(self.datahandler.get_data_dir_path())
        if not dir_check.exists():
            self.ui.show_note("Cannot synchronize, download dir " + self.datahandler.get_data_dir_path() + " does not exist. Please set a new folder in settings.")
            return

        self.sync_ongoing = True
        self.sync_fetching_sync_root = True
        self.sync_root = None
        self.sync_total_results = []
        
        self.ui.show_banner("Preparing synchronization, please wait...", 2000)
        
        # Make metadata fetch thread
        metadata_worker = NetworkWorker()
        metadata_worker.set_callable(self.connection.client.metadata, "dropbox", sync_path, 10000, None)
        self.queued_metadata_threads.append(metadata_worker)
        self.check_metadata_queue()
                           
    def sync_parse_response(self, response):
        if response != None:
            if response.status == 200:
                sync_result = self.parse_metadata(response.data)
                if sync_result == None:
                    self.ui.show_banner("Fatal synchronization error, cannot continue")
                    self.logger.sync_error("Fatal synchronization error, cannot continue")
                    return
                self.sync_total_results.append(sync_result)                
                if sync_result.total_folders > 0:
                    for child_folder in sync_result.fetch_meatadata_folders:
                        metadata_worker = NetworkWorker()
                        metadata_worker.set_callable(self.connection.client.metadata, "dropbox", child_folder.path, 10000, None)
                        self.queued_metadata_threads.append(metadata_worker)
            else:
                try:
                    e = simplejson.loads(response.body)["error"]
                except:
                    e = "Invalid path"
                self.ui.show_banner("Synchronizing failed - " + e)
                self.logger.sync_error("Could not fetch metadata from sync path: " + e)
                
        self.check_metadata_queue()
        
    def parse_metadata(self, data):
        try:
            if data["is_dir"]:        
                parent_root = data["root"]
                sync_folder = Collection(data["path"], data["modified"], data["icon"], data["thumb_exists"], parent_root, data["hash"])
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
                        child = Resource(path, size, item["bytes"], modified, item["mime_type"], icon, has_thumb, parent_root)
                    sync_folder.add_item(child)
                # Store root data
                if self.sync_fetching_sync_root:
                    self.sync_root = SyncRoot(sync_folder)    
                    self.sync_fetching_sync_root = False
                # Store sync results for this path
                result = SyncResult(self.datahandler, sync_folder)
                result.check_local_path(self.sync_root)
                result.check_files_for_changes()
                return result
            else:
                self.ui.show_banner("Sync error, check log")
                self.logger.sync_error("Sync path is not a folder, stopping sync")
                return None
        except Exception, e:
            self.ui.show_banner("Sync error, check log")
            self.logger.sync_error("Parsing sync path metadata failed: " + str(e))
            return None
            
    def finish_sync(self):
        sync_confirmation = QMessageBox(self.ui.main_widget)
        continue_button = sync_confirmation.addButton("Continue", QMessageBox.YesRole)
        cancel_button = sync_confirmation.addButton("Cancel", QMessageBox.NoRole)
        sync_confirmation.setWindowTitle("Synchronization Confirmation")
        
        main_layout = QGridLayout()
        main_layout.setHorizontalSpacing(15)
        main_layout.setContentsMargins(0,0,0,0)
        
        row = 0
        hide_dl_items = []
        hide_ul_items = []
        
        # Titles
        style = "QLabel { font-size: 16pt; color: #0099FF; font-weight: bold;}"
        l = QLabel("Downloading")
        hide_dl_items.append(l)
        l.setStyleSheet(style)
        main_layout.addWidget(l, row, 0)
        l = QLabel("Files")
        hide_dl_items.append(l)
        l.setStyleSheet(style)
        main_layout.addWidget(l, row, 1)
        l = QLabel("Size")
        hide_dl_items.append(l)
        l.setStyleSheet(style)
        main_layout.addWidget(l, row, 2, Qt.AlignRight)
        
        # Information
        total_files = 0
        total_folders = 0
        total_bytes = 0
        total_ul_files = 0
        total_ul_bytes = 0

        # Iterate all results for downloads
        for result in self.sync_total_results:
            folder_files = result.total_dl_files
            total_files += folder_files
            folder_bytes = result.total_dl_bytes
            total_bytes += folder_bytes
            if folder_files > 0:
                row += 1 
                total_folders += 1
                main_layout.addWidget(QLabel(result.remote_path), row, 0)
                main_layout.addWidget(QLabel(str(folder_files)), row, 1)
                main_layout.addWidget(QLabel(self.datahandler.humanize_bytes(folder_bytes)), row, 2, Qt.AlignRight)           
        
        # Add total download numbers
        row += 1
        style = "QLabel { font-size: 14pt; color: rgb(94,189,0); }"
        l = QLabel("Total")
        hide_dl_items.append(l)
        l.setStyleSheet(style)
        main_layout.addWidget(l, row, 0)
        l = QLabel(str(total_files))
        hide_dl_items.append(l)
        l.setStyleSheet(style)
        main_layout.addWidget(l, row, 1)
        try:
            total_size_string = self.datahandler.humanize_bytes(total_bytes)
        except:
            total_size_string = "unknown"
        l = QLabel(total_size_string)
        hide_dl_items.append(l)
        l.setStyleSheet(style)
        main_layout.addWidget(l, row, 2, Qt.AlignRight)
        
        # Search for uploads
        row += 1
        ul_title_row = row
        total_ul_files = 0
        total_ul_bytes = 0
        create_new_folders = []
        all_skipped_uploads = []
        for result in self.sync_total_results:
            total_ul_bytes += result.total_ul_bytes
            total_ul_files += result.total_ul_files
            all_skipped_uploads += result.skipped_uploads
            # New files to upload
            for filename in result.new_files_to_upload:
                row += 1
                label = QLabel("NEW FILE")
                fileonly = filename.split("/")[-1]
                main_layout.addWidget(QLabel(result.remote_path + "/" + fileonly), row, 0)
                main_layout.addWidget(label, row, 1)
                main_layout.addWidget(QLabel(self.datahandler.humanize_bytes(os.path.getsize(filename))), row, 2, Qt.AlignRight)
            # Files to update
            for filename in result.out_of_date_files_upload:
                row += 1       
                label = QLabel("CHANGED FILE")
                fileonly = filename.split("/")[-1]
                main_layout.addWidget(QLabel(result.remote_path + "/" + fileonly), row, 0)
                main_layout.addWidget(label, row, 1)
                main_layout.addWidget(QLabel(self.datahandler.humanize_bytes(os.path.getsize(filename))), row, 2, Qt.AlignRight)
            # New folders and files under them to upload
            for (remote_folder, local_files) in result.new_folders_to_files.iteritems():
                create_new_folders.append(result.remote_path + "/" + remote_folder)
                folder_size = 0
                folder_files = 0
                for filename in local_files:
                    folder_size += os.path.getsize(filename)
                    folder_files += 1
                total_ul_bytes += folder_size
                total_ul_files += folder_files
                row += 1       
                if folder_files == 0:
                    continue
                label = QLabel(str(folder_files))
                main_layout.addWidget(QLabel(result.remote_path + "/" + remote_folder), row, 0)
                main_layout.addWidget(label, row, 1)
                main_layout.addWidget(QLabel(self.datahandler.humanize_bytes(folder_size)), row, 2, Qt.AlignRight)
                
        # Add total upload numbers
        row += 1
        style = "QLabel { font-size: 14pt; color: rgb(94,189,0); }"
        l = QLabel("Total")
        hide_ul_items.append(l)
        l.setStyleSheet(style)
        main_layout.addWidget(l, row, 0)
        l = QLabel(str(total_ul_files))
        hide_ul_items.append(l)
        l.setStyleSheet(style)
        main_layout.addWidget(l, row, 1)
        try:
            total_ul_size_string = self.datahandler.humanize_bytes(total_ul_bytes)
        except:
            total_ul_size_string = "unknown"
        l = QLabel(total_ul_size_string)
        hide_ul_items.append(l)
        l.setStyleSheet(style)
        main_layout.addWidget(l, row, 2, Qt.AlignRight)
                        
        # Upload titles
        style = "QLabel { font-size: 16pt; color: #0099FF; font-weight: bold;}"
        l = QLabel("Uploading")
        hide_ul_items.append(l)
        l.setStyleSheet(style)
        main_layout.addWidget(l, ul_title_row, 0, Qt.AlignBottom)
        l = QLabel("Files")
        hide_ul_items.append(l)
        l.setStyleSheet(style)
        main_layout.addWidget(l, ul_title_row, 1, Qt.AlignBottom)
        l = QLabel("Size")
        hide_ul_items.append(l)
        l.setStyleSheet(style)
        main_layout.addWidget(l, ul_title_row, 2, Qt.AlignBottom|Qt.AlignRight)
        main_layout.setRowMinimumHeight(ul_title_row, 40)
        
        # Creating New Folders
        if len(create_new_folders) > 0:
            create_new_folders.sort()
            row += 1
            style = "QLabel { font-size: 16pt; color: #0099FF; font-weight: bold;}"
            l = QLabel("Creating New Folders to DropBox")
            l.setStyleSheet(style)
            main_layout.addWidget(l, row, 0, Qt.AlignBottom)
            for remote_path in create_new_folders:
                row += 1
                l = QLabel(remote_path)
                main_layout.addWidget(l, row, 0, Qt.AlignBottom)

        # Make a scrollview
        view_widget = QWidget()
        view_widget.setFont(QFont("Arial", 14))
        view_widget_l = QVBoxLayout()
        view_widget_l.addLayout(main_layout)
        view_widget_l.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding))
        view_widget.setLayout(view_widget_l)
        view = QScrollArea()
        view.setWidget(view_widget)
        view.setWidgetResizable(True)
        view.setMinimumHeight(360)
                    
        # Add nothing to dl/ul report
        if total_files == 0 and total_ul_files == 0:
            # Modify controls and title
            cancel_button.setText("Close")
            sync_confirmation.setWindowTitle("Synchronization Report")
            sync_confirmation.removeButton(continue_button)
            # Add title
            row += 1
            style = "QLabel { font-size: 20pt; color: #0099FF; font-weight: bold;}"
            l = QLabel("Nothing to sync, all files up to date!")
            l.setStyleSheet(style)
            main_layout.addWidget(l, row, 0, Qt.AlignBottom)
            row += 1
            main_layout.addWidget(QLabel(""), row, 0, Qt.AlignBottom)
            if len(all_skipped_uploads) == 0:
                view.setMinimumHeight(150)
                    
        # Report skipped paths
        if len(all_skipped_uploads) > 0:
            all_skipped_uploads.sort()
            row += 1
            style = "QLabel { font-size: 14pt; color: red; font-weight: bold;}"
            l = QLabel("Skipping uploads: non ASCII chars in path and ~ temp files")
            l.setStyleSheet(style)
            main_layout.addWidget(l, row, 0, Qt.AlignBottom)
            for skipped_path in all_skipped_uploads:
                row += 1
                l = QLabel(skipped_path)
                main_layout.addWidget(l, row, 0, Qt.AlignBottom)
        
        # Add view and show dialog
        sync_confirmation.layout().setHorizontalSpacing(0)
        sync_confirmation.layout().setVerticalSpacing(0)
        sync_confirmation.layout().setContentsMargins(0,0,10,10)
        sync_confirmation.layout().addWidget(view, 0, 0)

        # Hide titles if no items
        if total_files == 0:
            for label in hide_dl_items:
                label.hide()
        if total_ul_files == 0:
            for label in hide_ul_items:
                label.hide()
                                
        # Show confirmation dialog
        if total_files > 0 or total_ul_files > 0:
            confirmation = sync_confirmation.exec_()
    
            # Check confirmation
            if confirmation == 1:
                del sync_confirmation
                return
            if confirmation == 0:
                # Update ui and log
                post_files = " file from " if total_files == 1 else " files from "
                post_folders = " folder" if total_folders == 1 else " folders"
                banner_total_size_string = ", total of " + total_size_string if total_size_string != "unknown" else ""
                message = "Downloading " + str(total_files) + post_files + str(total_folders) + post_folders + banner_total_size_string
                self.logger.sync(message)
                
                post_ul_files = " file" if total_ul_files == 1 else " files"
                banner_total_ul_size_string = ", total of " + total_ul_size_string if total_ul_size_string != "unknown" else ""
                message_ul = "Uploading " + str(total_ul_files) + post_ul_files + banner_total_ul_size_string
                self.logger.sync(message_ul)
                
                # Create new remote dirs
                if len(create_new_folders) > 0:
                    create_new_folders.sort() # sort so we create forlder from bottom up
                    for remote_path in create_new_folders:
                        if self.connection.create_folder_blocking(remote_path):
                            self.logger.info("Created remote folder " + remote_path + " succesfully")
                        else:
                            self.logger.info("Failed to create remote folder " + remote_path)

                # Check for additional child results, these are present 
                # if we have totally new folders with new files for upload
                additional_results = []
                for sync_result in self.sync_total_results:
                    if len(sync_result.child_upload_results) > 0:
                        additional_results += sync_result.child_upload_results
                self.sync_total_results += additional_results

                # DL/UL files from/to dropbox
                store_dir = self.datahandler.get_data_dir_path()
                for sync_result in self.sync_total_results:
                    # Create directory
                    if sync_result.local_folder_exists == False:
                        sync_result.create_local_path()
                    # Queue downloads
                    for sync_file in sync_result.out_of_date_files:
                        self.connection.get_file(sync_file.path, sync_file.root, sync_result.local_path + "/" + sync_file.get_name(), sync_file.size, sync_file.mime_type, True)
                    # Queue uploads
                    for ul_sync_file in sync_result.out_of_date_files_upload:
                        self.connection.upload_file(sync_result.remote_path, "dropbox", ul_sync_file, True)
                    for ul_sync_file in sync_result.new_files_to_upload:
                        self.connection.upload_file(sync_result.remote_path, "dropbox", ul_sync_file, True)
                self.controller.transfer_widget.add_sync_widget(self.sync_root.path, store_dir + self.sync_root.name, total_folders, total_files, total_size_string, total_ul_files, total_ul_size_string)
                self.ui.show_transfer_widget()
        else:
            sync_confirmation.exec_()
        del sync_confirmation


""" SyncRoot has data about the main synchronization path """

class SyncRoot:

    def __init__(self, data):
        self.path = data.path
        self.name = data.name

        
""" SyncResult has data about a path in the synchronization """

class SyncResult:

    def __init__(self, datahandler, sync_folder):
        self.datahandler = datahandler
        self.logger = datahandler.logger
        self.data = sync_folder
        if sync_folder != None:
            self.remote_path = self.to_unicode(sync_folder.path)
        self.local_path = None
        if sync_folder != None:
            self.local_folder_exists = False
        else:
            self.local_folder_exists = True

        self.child_upload_results = []        
        self.out_of_date_files = []
        self.out_of_date_files_upload = []
        self.new_files_to_upload = []
        self.fetch_meatadata_folders = []
        self.skipped_uploads = []
        self.new_folders_to_files = {}
        
        self.total_folders = 0
        self.total_dl_files = 0
        self.total_dl_bytes = 0
        self.total_ul_files = 0
        self.total_ul_bytes = 0

    def __str__(self):
        print "SYNC RESULT"
        print "> Remote path          :", self.remote_path
        print "> Local path           :", self.local_path
        print "> Sub folders          :", str(len(self.fetch_meatadata_folders))
        print ""
        print "> Creating new         :", self.new_folders_to_files
        print "> Downloading          :", str(len(self.out_of_date_files))
        print "> Uploading"
        print "  >> Update            :", str(len(self.out_of_date_files_upload))
        print "  >> New               :", str(len(self.new_files_to_upload))
        return ""
                
    def check_local_path(self, sync_root):
        if self.remote_path ==  sync_root.path:
            self.local_path = self.datahandler.datadirpath(sync_root.name)
        elif self.remote_path.startswith(sync_root.path):
            self.local_path = self.remote_path[len(sync_root.path):]
            self.local_path = sync_root.name + self.local_path
            self.local_path = self.datahandler.datadirpath(self.local_path)
        else:
            self.logger.sync_error("Error parsing path in SyncResult.check_local_path()")
            return
       
        if os.path.exists(self.local_path):
            self.local_folder_exists = True
            
    def create_local_path(self):
        if self.total_dl_files == 0:
            return
        if not os.path.exists(self.local_path): 
            try:
                os.makedirs(self.local_path)
                self.local_folder_exists = True
            except OSError:
                self.logger.sync_error("Failed to create folder in SyncResult.create_local_path(): " + str(self.local_path))

    def check_files_for_changes(self):
        # Mark subfolders                
        for child_folder in self.data.get_folders():
            self.fetch_meatadata_folders.append(child_folder)

        # Mark out of date files, comparing device and remote files
        for child_file in self.data.get_files():
            try:
                if self.local_folder_exists == False:
                    self.out_of_date_files.append(child_file)
                else:
                    local_file_path = self.local_path + "/" + child_file.get_name()
                    if os.path.exists(local_file_path):
                        device_modified = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(os.path.getmtime(local_file_path)))
                        
                        # Parse timestamps
                        device_datetime = self.parse_timestamp(device_modified)
                        remote_datetime = self.parse_timestamp(child_file.modified)
                        device_size_bytes = os.path.getsize(local_file_path)
                        remote_size_bytes = child_file.size_bytes
                        
                        if device_datetime == None or remote_datetime == None:
                            self.logger.warning("Parsing timestamp for " + local_file_path + " failed, skipping sync.")
                            continue
                            
                        # Check for changes
                        if remote_datetime > device_datetime and device_size_bytes != remote_size_bytes:
                            self.out_of_date_files.append(child_file)
                        elif device_datetime > remote_datetime and device_size_bytes != remote_size_bytes:
                            if self.upload_path_check(local_file_path):
                                self.out_of_date_files_upload.append(local_file_path)
                    else:
                        self.out_of_date_files.append(child_file)
            except OSError, e:
                self.logger.sync_error("OSError was raised while syncing: " + str(e))
                
        # Mark new files on the device for upload
        local_folders = []
        remote_filenames = []
        for remote_file in self.data.get_files():
            remote_filenames.append(remote_file.get_name())
       
        try:
            for filename in os.listdir(self.local_path):
                full_path = self.local_path + "/" + filename
                if os.path.isdir(full_path):
                    local_folders.append(filename)
                    continue
                try:
                    index = remote_filenames.index(filename)
                except:
                    if self.upload_path_check(full_path):
                        self.new_files_to_upload.append(full_path)
        except OSError, e:
            pass # Trying to open non existing non-ascii folder, its marked for DL at this point...
            
        # Mark new local folders for upload
        remote_folders = []
        for metadata in self.fetch_meatadata_folders:
            remote_folders.append(metadata.get_name())
        
        for local_folder_name in local_folders:
            try:
                index = remote_folders.index(local_folder_name)
            except:
                full_new_path = self.local_path + "/" + local_folder_name
                self.get_all_files(full_new_path)

        # Create child results from self.new_folders_to_files
        for (subfolder, fileslist) in self.new_folders_to_files.iteritems():
            child_result = SyncResult(self.datahandler, None)
            child_result.remote_path = self.to_unicode(self.remote_path + "/" + subfolder)
            for filepath in fileslist:
                child_result.new_files_to_upload.append(filepath)
            self.child_upload_results.append(child_result)
                    
        # Calculate totals
        self.total_folders = len(self.fetch_meatadata_folders)
        self.total_dl_files = len(self.out_of_date_files)
        for f in self.out_of_date_files:
            self.total_dl_bytes += f.size_bytes
        self.total_ul_files = len(self.new_files_to_upload) + len(self.out_of_date_files_upload)
        for f in self.new_files_to_upload:
            self.total_ul_bytes += os.path.getsize(f)
        for f in self.out_of_date_files_upload:
            self.total_ul_bytes += os.path.getsize(f)
            
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
        
        try:
            datetime_data = datetime.datetime(data["year"], data["month"], data["day"], data["hour"], data["min"], data["sec"])
        except Exception, e:
            self.logger.sync_error("Exception occurred when parsing timestamp: " + str(e))
            return None
        return datetime_data
        
    def upload_path_check(self, path):
        # Test if filename/path is ok for upload, unfortunately non-ascii 
        # paths are skipped due to dropbox not accepting them
        try:
            str(path)
            if path.endswith("~"):
                self.logger.warning("Skipping sync upload for temp file: " + path.encode("utf-8"))
                self.skipped_uploads.append(path)
                return False
        except:
            self.logger.warning("Skipping sync upload for non-ascii path: " + path.encode("utf-8"))
            self.skipped_uploads.append(path)
            return False
        return True
        
    def get_all_files(self, search_path):
        basefolder = search_path.split("/")[-1]
        for (path, dirs, files) in os.walk(search_path):
            if path != search_path:
                subfolder = basefolder + path[len(search_path):]
            else:
                subfolder = basefolder
            self.new_folders_to_files[subfolder] = []
            for filename in files:
                if self.upload_path_check(path + "/" + filename):
                    self.new_folders_to_files[subfolder].append(path + "/" + filename)

    def to_unicode(self, obj, encoding = "utf-8"):
        if isinstance(obj, basestring):
            if not isinstance(obj, unicode):
                obj = unicode(obj, encoding)
        return obj
        
""" TransferManager monitors upload/downloads and relays info to TransferWidget """

class TransferManager(QObject):

    def __init__(self, controller):
        QObject.__init__(self)
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
        self.poll_timer = QTimer(self)
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
        
    def start_poller(self, timeout_msec = 50):
        self.poll_timer.start(timeout_msec)
        
    def stop_poller(self):
         self.poll_timer.stop()
         
    def get_transfer_widget(self, transfer):
        try:
            transfer_widget = self.tranfer_to_widget[self.active_transfer]
        except KeyError:
            self.logger.transfer_error("Could not find transfer widget!")
            transfer_widget = None
        return transfer_widget

    def thread_poller(self):
        if self.active_transfer == None:
            self.stop_poller()
            return
        self.active_transfer.join(0.01)
        if not self.active_transfer.isAlive():
            transfer = self.active_transfer
            transfer_widget = self.get_transfer_widget(transfer)
            self.active_transfer = None
            if transfer.error != None:
                transfer_widget.set_failed()
                self.logger.transfer_error(transfer.transfer_type + " of " + transfer.file_name + " failed, no connection?")
                self.logger.transfer_error(">>" + str(transfer.error))
            if transfer.response != None:
                if transfer.response.status == 200:
                    transfer_widget.set_completed()
                    if transfer.transfer_type == "Download":
                        transfer.callback(transfer.response, transfer.data, transfer.callback_parameters)
                    else:
                        transfer.callback(transfer.response, transfer.callback_parameters)
                else:
                    try:
                        transfer_widget.set_failed("Failed with reason: " + transfer.response.data["error"])
                    except:
                        transfer_widget.set_failed("Failed with unknown reason")
            del transfer
            self.check_transfer_queue()

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
                
    def handle_download(self, path, root, file_name, dropbox_path, device_store_path, size, mime_type, sync_download):
        download = TransferWorker("Download")
        download.set_callable(self.client.get_file, root, path)
        download.set_callback(self.connection.get_file_callback, device_store_path, file_name)
        download.set_download_info(file_name, device_store_path)
        
        device_path = device_store_path[0:device_store_path.rfind("/")]
        download_item = self.transfer_widget.add_download(file_name, dropbox_path, device_path, size, mime_type, sync_download)
        self.tranfer_to_widget[download] = download_item
        
        self.queued_transfer_threads.append(download)
        self.check_transfer_queue()
        
    def handle_upload(self, path, root, file_obj, file_name, from_local_path, dropbox_store_path, local_file_path, sync_upload):
        upload = TransferWorker("Upload")
        upload.set_callable(self.client.put_file, root, path, file_obj)
        upload.set_callback(self.connection.upload_file_callback, root, path, file_name)
        upload.set_upload_info(file_name, dropbox_store_path)
        try:
            size = self.datahandler.humanize_bytes(os.path.getsize(local_file_path))
        except:
            size = ""
        upload_item = self.transfer_widget.add_upload(file_name, from_local_path, dropbox_store_path, size, sync_upload)
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
        self.data = None

    def set_download_info(self, file_name, device_store_path):
        self.file_name = file_name
        self.store_path = device_store_path
        
    def set_upload_info(self, file_name, dropbox_store_path):
        self.file_name = file_name
        self.store_path = dropbox_store_path

    def run(self):
        encoded_params = []
        for param in self.parameters:
            param = self.encode_unicode(param)
            encoded_params.append(param)

        try:
            self.response = self.method(*tuple(encoded_params))
            if self.response != None:
                if self.transfer_type == "Download":
                    self.data = self.response.read()
                else:
                    self.data = self.response.data
            else:
                self.error = "Response None, with status code " + self.response.status
                self.data = None
        except (socket.error, socket.gaierror), err:
            self.response = None
            self.error = err
            self.data = None
        
""" TransferWidget is a tranfer monitoring widget """

class TransferWidget(QMainWindow):

    def __init__(self, transfer_manager):
        QMainWindow.__init__(self, transfer_manager.ui.main_widget, Qt.Window)
        self.setAttribute(Qt.WA_Maemo5StackedWindow)
        self.setWindowTitle("DropN900 - Transfers")
        self.setCentralWidget(QWidget())
        self.ui = Ui_TransferWidget()
        self.ui.setupUi(self.centralWidget())
        
        self.transfer_manager = transfer_manager
        self.datahandler = transfer_manager.datahandler
        self.logger = transfer_manager.logger
        
        self.icon_download = QPixmap(self.datahandler.datapath("ui/icons/item_download.png"))
        self.icon_download_sync = QPixmap(self.datahandler.datapath("ui/icons/item_download_sync.png"))
        self.icon_upload = QPixmap(self.datahandler.datapath("ui/icons/item_upload.png"))
        self.icon_upload_sync = QPixmap(self.datahandler.datapath("ui/icons/item_upload_sync.png"))
        self.icon_sync = QPixmap(self.datahandler.datapath("ui/icons/item_sync.png"))

        self.icon_ok = QPixmap(self.datahandler.datapath("ui/icons/item_ok.png"))
        self.icon_error = QPixmap(self.datahandler.datapath("ui/icons/item_error.png")) 
        self.ui.label_first_time_icon.setPixmap(QPixmap(self.datahandler.datapath("ui/icons/transfer_manager.png")))
        
        action_clear = self.menuBar().addAction("Clear History")
        action_clear.triggered.connect(self.clear_history)
        
    def clear_history(self):
        if self.ui.label_first_time_note.isVisible():
            return
        if len(self.transfer_manager.queued_transfer_threads) > 0 or self.transfer_manager.active_transfer != None:
            confirmation = QMessageBox.question(None, " ", "There are still active transfers, clear history anyway?", QMessageBox.Yes, QMessageBox.Cancel)
            if confirmation == QMessageBox.Cancel:
                return
            
        rescue_widgets = [self.ui.label_first_time_note, self.ui.label_first_time_icon]
        for w in rescue_widgets:
            index = self.ui.item_layout.indexOf(w)
            if index == -1:
                return
            l_item = self.ui.item_layout.itemAt(index)
            self.ui.item_layout.removeItem(l_item)
            
        for nothing in range(self.ui.item_layout.count()):
            child = self.ui.item_layout.takeAt(0)
            widget_item = child.widget()
            if widget_item != None:
                widget_item.hide()
                del widget_item
            del child
            
        self.ui.label_first_time_note.setText("Tranfer history cleared")
        self.ui.item_layout.insertSpacerItem(0, QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding))
        for w in rescue_widgets:
            self.ui.item_layout.insertWidget(0, w)
            w.show()
        
    def showEvent(self, show_event):
        self.layout_check()
        QWidget.showEvent(self, show_event)
        
    def add_download(self, filename, from_path, to_path, size, mime_type, sync_download):
        download_item = TransferItem(self, "Download", sync_download)
        icon = self.icon_download if not sync_download else self.icon_download_sync
        download_item.set_icon(icon, True)
        download_item.set_information(filename, from_path, to_path, size)
        download_item.handle_mime_type(mime_type)
        
        self.ui.item_layout.insertWidget(0, download_item)
        download_item.show()
        self.layout_check()
        return download_item
        
    def add_upload(self, filename, from_path, to_path, size, sync_upload):
        upload_item = TransferItem(self, "Upload", sync_upload)
        icon = self.icon_upload if not sync_upload else self.icon_upload_sync
        upload_item.set_icon(icon, True)
        upload_item.set_information(filename, from_path, to_path, size)
        mime_type, encoding = mimetypes.guess_type(filename)
        upload_item.handle_mime_type(mime_type)

        self.ui.item_layout.insertWidget(0, upload_item)
        upload_item.show()
        self.layout_check()
        return upload_item
        
    def add_sync_widget(self, sync_path, local_store_path, total_dl_folders, total_dl_files, total_dl_size, total_ul_files, total_ul_size):
        sync_information = TransferItem(self, "Synchronization", True)
        sync_information.set_icon(self.icon_sync, True)
        sync_information.set_sync_information(sync_path, local_store_path, total_dl_folders, total_dl_files, total_dl_size, total_ul_files, total_ul_size)
        
        self.ui.item_layout.insertWidget(0, sync_information)
        sync_information.show()
        self.layout_check()
                
    def layout_check(self):
        if self.ui.item_layout.count() > 3:
            if self.ui.label_first_time_note.isVisible():
                self.ui.label_first_time_note.hide()
                self.ui.label_first_time_icon.hide()
                
                
""" TransferItem is a custom list widget that shows tranfer data """

class TransferItem(QWidget):

    def __init__(self, parent, transfer_type, sync_transfer):
        QWidget.__init__(self)
        self.ui = Ui_TransferItem()
        self.ui.setupUi(self)
        self.parent = parent
        
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
        
        self.ui.label_timestamp.hide()
        self.ui.label_duration.hide()
        self.ui.label_sep.hide()
        
        self.sync_transfer = sync_transfer
        if self.sync_transfer:
            self.ui.content_frame.setStyleSheet("QFrame#content_frame{border: 0px;border-bottom: 1px solid grey;background-color: \
            qlineargradient(spread:pad, x1:0, y1:0.466182, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255), stop:0.462312 rgba(11, 11, 64, 255), stop:1 rgba(22, 22, 22, 255));}")

    def handle_mime_type(self, item_type):
        if item_type == None:
            self.ui.mime_icon.hide()
            self.ui.label_filename.setIndent(0)
            return
        base_path = self.parent.datahandler.app_root + "ui/icons/"
        base_type = item_type.split("/")[0]
        # item type
        icon = None
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
        # set icon
        if icon != None:
            self.ui.mime_icon.setPixmap(icon.pixmap(20,20))
        else:
            self.ui.mime_icon.hide()
            self.ui.label_filename.setIndent(0)

    def set_information(self, filename, from_path, to_path, size):
        self.ui.label_filename.setText(filename)
        self.ui.label_from.setText(from_path)        
        self.ui.label_to.setText(to_path)
        self.ui.label_size.setText(size)
        self.ui.label_duration.setText("< 1 sec")
        if size == "":
            self.ui.label_size.hide()
            self.ui.label_sep.hide()
            
    def set_sync_information(self, sync_path, local_store_path, total_dl_folders, total_dl_files, total_dl_size, total_ul_files, total_ul_size):
        self.handle_mime_type(None)
        self.set_status(self.transfer_type, "#0099FF;")
        self.generate_timestamp(QDateTime.currentDateTime())
        self.ui.label_filename.setText(sync_path)
        self.ui.label_size.setText("DL " + total_dl_size)
        self.ui.title_from.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.ui.title_from.setMaximumWidth(300)
        self.ui.title_from.setText("Downloading")
        self.ui.title_from.setIndent(5)
        self.ui.title_from.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.ui.title_to.setMinimumWidth(1)
        self.ui.title_to.setIndent(5)
        post_files = " file from " if total_dl_files == 1 else " files from "
        post_folders = " folder" if total_dl_folders == 1 else " folders"
        self.ui.label_from.setText(str(total_dl_files) + post_files + str(total_dl_folders) + post_folders)
        self.ui.label_to.setText(local_store_path)
        self.ui.label_duration.setText("UL " + total_ul_size)
        
        layout = QHBoxLayout()
        ul_title = QLabel("Uploading")
        ul_title.setObjectName("title_upload")
        post_ul_files = " file" if total_ul_files == 1 else " files"
        ul_value = QLabel(str(total_ul_files) + post_ul_files)
        ul_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        ul_value.setIndent(5)
        layout.addWidget(ul_title)
        layout.addWidget(ul_value)
        self.ui.labels_layout.addLayout(layout)
        
        self.ui.label_duration.show()
        self.ui.label_sep.show()
                
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
        self.ui.label_timestamp.show()
        
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
        self.generate_timestamp(QDateTime.currentDateTime())
        self.set_status(status, color)
        self.start_animation()
        
    def set_completed(self, status = None, color = "rgb(94,189,0);"):
        if status == None:
            status = self.transfer_type + " completed"
            if self.sync_transfer:
                status = "Sync " + status.lower()
        self.set_status(status, color)       
        self.stop_animation()
        self.set_icon(self.initial_pixmap)
        self.ui.content_frame.setStyleSheet("QFrame#content_frame{border: 0px;border-bottom: 1px solid grey;background-color: \
        qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 7, 0, 255), stop:0.502513 rgba(0, 50, 0, 200), stop:1 rgba(0, 0, 0, 255));}")

    def set_failed(self, status = None, color = "rgb(200,0,0);"):
        if status == None:
            status = self.transfer_type + " failed"
            if self.sync_transfer:
                status = "Sync " + status.lower()
        self.set_status(status, color)
        self.stop_animation()
        self.set_icon(self.parent.icon_error)
        self.ui.content_frame.setStyleSheet("QFrame#content_frame{border: 0px;border-bottom: 1px solid grey;background-color: \
        qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 255), stop:0.512563 rgba(64, 0, 0, 255), stop:1 rgba(6, 6, 6, 255));}")

