
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
from ui.ui_synctransferitem import Ui_SyncTransferItem

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
            
    def can_sync(self, path):
        if self.connection.client == None:
            self.ui.show_banner("Cannot synchronize, not connected to Dropbox")
            self.logger.sync("Cannot synchronize, no network connection")
            return False
        if self.connection.connection_available() == False:
            self.ui.show_banner("Cannot synchronize, no network connection")
            self.logger.sync("Cannot synchronize, no network connection")
            return False
        if self.datahandler.only_sync_on_wlan:
            if not self.connection.connection_is_wlan():
                self.ui.show_banner("Synchronizing without WLAN disabled in settings", 4000)
                return False
        if len(self.controller.transfer_manager.queued_transfer_threads) > 0 or self.controller.transfer_manager.active_transfer != None:
            self.ui.show_banner("There are ongoing active transfers\nPlease wait for them to complete")
            return False    
        if len(self.connection.data_workers) > 0:
            self.ui.show_banner("Data is still being written from previous downloads\nPlease wait a moment and try synchronizing again", 5000)
            return False
        if self.sync_ongoing:
            self.ui.show_banner("Synchronization already in progress")
            self.logger.sync("Synchronizing already in progress")
            return False
        if sync_path == "" or sync_path == "/":
            self.ui.show_banner("Cannot synchronize, path / invalid")
            self.logger.sync("Cannot synchronize, path / invalid")
            return False
        if sync_path == "None":
            self.ui.show_banner("Synchronizing disabled in settings", 2000)
            return False 
        if sync_path[0] != "/":
            self.ui.show_banner("Cannot synchronize, path '" + sync_path + "' invalid")
            self.logger.sync("Cannot synchronize, path '" + sync_path + "' invalid")
            return False
        dir_check = QDir(self.datahandler.get_data_dir_path())
        if not dir_check.exists():
            self.ui.show_note("Cannot synchronize, download dir " + self.datahandler.get_data_dir_path() + " does not exist. Please set a new folder in settings.")
            return False
        # If got this far, we should be ok to sync
        return True
            
    def sync_images(self):
        path_local = self.datahandler.user_home + "/MyDocs/DCIM"
        path_remote = "/Photos"
        if not self.can_sync(path_remote):
            return
        
        self.ui.show_banner("Preparing photo synchronization, please wait...", 2000)
        self.ui.set_synching(True)
        
        print "Fetching metadata for Photos folder..."
        response = self.connection.client.metadata("dropbox", path_remote, 10000, None)
        print "Response:", response.status        
        if response.status != 200:
            print "Error fetching destination metadata"
            self.ui.set_synching(False)
            return
            
        data_photos = self.connection.data_parser.parse_metadata(response.data, None)
        remote_files_obj = data.get_files()
        remote_files = []
        for file_obj in remote_files_obj:
            remote_files.append(file_obj.get_name())
        print "Remote files:", remote_files
        
        sending_local_files = {}
        for filename in os.listdir(path_local):
            full_path = path_local + "/" + filename
            if os.path.isdir(full_path):
                continue
            try:
                found = remote_files[filename]
            except IndexError:
                print "File", filename, "not found from remote"
                sending_local_files[filename] = full_path
                
        if len(sending_local_files) == 0:
            print "All photos/videos up to date"
            return
            
        videos = {}
        videos_size = 0
        images = {}
        images_size = 0
        for (name, path) in sending_local_files.iteritems():
            ext = name.split(".")[-1]
            if ext == "mp4":
                videos[name] = path
                videos_size += os.path.getsize(path)
            else:
                images[name] = path
                images_size += os.path.getsize(path)
        
        confirmation_ul = SyncDialog(self.ui.main_widget)    
        confirmation_ul.setWindowTitle("Camera Photos Upload Confirmation")
        button_ul_all = confirmation_ul.addButton("Upload All", QMessageBox.YesRole)
        button_ul_photos = confirmation_ul.addButton("Upload Photos", QMessageBox.ActionRole)
        button_ul_videos = confirmation_ul.addButton("Upload Videos", QMessageBox.DestructiveRole)
        button_ul_cancel = confirmation_ul.addButton("Cancel", QMessageBox.NoRole)
        
        confirmation_ul.add_titles(" ", "Files", "Size")
        confirmation_ul.add_row("Photos", len(images), self.datahandler.humanize_bytes(images_size))
        confirmation_ul.add_row("Videos", len(videos), self.datahandler.humanize_bytes(videos_size))
        confirmation_ul.add_totals(" ", str(len(images)+len(videos)), self.datahandler.humanize_bytes(images_size+videos_size))
        confirmation_ul.finalize()
                
        # Photo UL dialog: Upload All = 0, Upload Photos = 1, Cancel = 2, Upload Videos = 3
        upload_map = {}
        upload_bytes = 0
        result = confirmation_ul.exec_()
            if result == 2:
                print "Canceled"
                return
            elif result == 0:
                print "Upload All"
                upload_map = images + videos
                upload_bytes = images_size + videos_size
            elif results == 1:
                print "Upload Photos"
                upload_map = images
                upload_bytes = images_size
            elif result == 3:
                print "Upload Videos"
                upload_map = videos
                upload_bytes = videos_size
                
        sync_widget = SyncTransferItem(self)
        sync_widget.set_totals(0, len(upload_map))
        sync_widget.set_sizes("0", self.datahandler.humanize_bytes(upload_bytes))
        sync_widget.ui.dl_size.hide()
        self.controller.transfer_manager.set_current_sync(sync_widget)
        self.controller.transfer_widget.add_sync_reporting(sync_widget)
        
        for (name, path) in upload_map.iteritems():
            self.connection.upload_file(path_remote, "dropbox", path, True)

        self.ui.set_synching(False)
        self.ui.show_transfer_widget()
                
    def sync_now(self, sync_path):
        if not self.can_sync(sync_path):
            return
            
        self.sync_ongoing = True
        self.sync_fetching_sync_root = True
        self.sync_root = None
        self.sync_total_results = []
        
        self.ui.show_banner("Preparing synchronization, please wait...", 2000)
        self.ui.set_synching(True)
        
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
        confirm_dl = True
        confirm_ul = True
        new_ul_files = False
        
        confirmation_dl = SyncDialog(self.ui.main_widget)
        confirmation_dl.setWindowTitle("Synchronization Download Confirmation")
        button_dl_continue = confirmation_dl.addButton("Download All", QMessageBox.YesRole)
        button_dl_ignore = confirmation_dl.addButton("Ignore Files", QMessageBox.ActionRole)
        button_dl_cancel = confirmation_dl.addButton("Cancel", QMessageBox.NoRole)

        confirmation_ul = SyncDialog(self.ui.main_widget)    
        confirmation_ul.setWindowTitle("Synchronization Upload Confirmation")
        button_ul_continue = confirmation_ul.addButton("Upload All", QMessageBox.YesRole)
        button_ul_ignore = confirmation_ul.addButton("Ignore Files", QMessageBox.ActionRole)
        button_ul_cancel = confirmation_ul.addButton("Cancel", QMessageBox.NoRole)
        button_ul_remove = confirmation_ul.addButton("Remove New \nLocal Files", QMessageBox.DestructiveRole)
                
        # DOWNLOADS
        total_dl_files = 0
        total_dl_folders = 0
        total_dl_bytes = 0
        
        confirmation_dl.add_titles("Downloading", "Files", "Size")

        # Download files
        for result in self.sync_total_results:
            if result.total_dl_files == 0:
                continue
            total_dl_folders += 1
            total_dl_files += result.total_dl_files
            total_dl_bytes += result.total_dl_bytes
            confirmation_dl.add_row(result.remote_path, str(result.total_dl_files), self.datahandler.humanize_bytes(result.total_dl_bytes))
        
        # Totals
        confirmation_dl.add_totals("Total", str(total_dl_files), self.datahandler.humanize_bytes(total_dl_bytes))
        if total_dl_files == 0:
            confirm_dl = False

        confirmation_dl.finalize()
        
        # UPLOAD
        total_ul_files = 0
        total_ul_folders = 0
        total_ul_bytes = 0
        
        confirmation_ul.add_titles("Uploading", "Files", "Size")
        
        # Upload files
        create_new_folders = []
        all_skipped_uploads = []
        for result in self.sync_total_results:
            total_ul_bytes += result.total_ul_bytes
            total_ul_files += result.total_ul_files
            all_skipped_uploads += result.skipped_uploads
            # New files to upload
            for filename in result.new_files_to_upload:
                new_ul_files = True
                fileonly = filename.split("/")[-1]
                confirmation_ul.add_row(result.remote_path + "/" + fileonly, "NEW FILE", self.datahandler.humanize_bytes(os.path.getsize(filename)))
            # Files to update
            for filename in result.out_of_date_files_upload:
                fileonly = filename.split("/")[-1]
                confirmation_ul.add_row(result.remote_path + "/" + fileonly, "CHANGED FILE", self.datahandler.humanize_bytes(os.path.getsize(filename)))               
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
                total_ul_folders += 1 
                if folder_files == 0:
                    continue
                confirmation_ul.add_row(result.remote_path + "/" + remote_folder, str(folder_files), self.datahandler.humanize_bytes(folder_size))
        
        # Totals
        confirmation_ul.add_totals("Total", str(total_ul_files), self.datahandler.humanize_bytes(total_ul_bytes))
        if total_ul_files == 0:
            confirm_ul = False

        # New folders
        if len(create_new_folders) > 0:
            create_new_folders.sort()
            confirmation_ul.add_spacer()
            confirmation_ul.add_titles("Creating New Folders to DropBox")
            for remote_path in create_new_folders:
                confirmation_ul.add_row(remote_path)
                
        confirmation_ul.finalize()
                                
        # Show confirmation dialog
        if confirm_dl == True or confirm_ul == True:
            # DL dialog: OK = 0, IGNORE = 1, CANCEL = 2
            # UL dialog: OK = 0, IGNORE = 1, CANCEL = 2, REMOVE LOCAL = 3
            answer_dl = -1
            answer_ul = -1
            if confirm_dl:
                answer_dl = confirmation_dl.exec_()
                if answer_dl == 2:
                    del confirmation_dl
                    del confirmation_ul
                    self.ui.show_banner("Synchronization canceled")
                    self.ui.set_synching(False)
                    return
            if confirm_ul:
                if new_ul_files == False:
                    button_ul_remove.hide()
                answer_ul = confirmation_ul.exec_()
                if answer_ul == 2:
                    del confirmation_dl
                    del confirmation_ul
                    self.ui.show_banner("Synchronization canceled")
                    self.ui.set_synching(False)
                    return
                elif answer_ul == 3:
                    self.ui.show_banner("Removing new local files\nPlease wait...", 2000)
                    # Remove new local files and ask again
                    uploads_remaining = False
                    self.logger.sync("Removing local files that were not in DropBox")
                    for sync_result in self.sync_total_results:
                        for filepath in sync_result.new_files_to_upload:
                            self.logger.sync("- " + filepath)
                            total_ul_files -= 1
                            total_ul_bytes -= os.path.getsize(filepath)
                            os.remove(filepath)                
                        if len(sync_result.new_folders_to_files) > 0 or len(sync_result.out_of_date_files_upload) > 0:
                            uploads_remaining = True
                        sync_result.new_files_to_upload = []
                    # Reconfirm if needed
                    if uploads_remaining:
                        confirmation_ul.hide_new_uploads()
                        button_ul_remove.hide()
                        confirmation_ul.set_totals(str(total_ul_files), self.datahandler.humanize_bytes(total_ul_bytes))
                        answer_ul = confirmation_ul.exec_()
                    else:
                        answer_ul = -1
              
            # Check for additional child results, these are present 
            # if we have totally new folders with new files for upload
            additional_results = []
            for sync_result in self.sync_total_results:
                if len(sync_result.child_upload_results) > 0:
                    additional_results += sync_result.child_upload_results
            self.sync_total_results += additional_results
            store_dir = self.datahandler.get_data_dir_path()

            sync_widget = None
            if answer_dl == 0 or answer_ul == 0:
                sync_widget = SyncTransferItem(self)
                sync_widget.set_totals(total_dl_files, total_ul_files)
                sync_widget.set_sizes(self.datahandler.humanize_bytes(total_dl_bytes), self.datahandler.humanize_bytes(total_ul_bytes))
                self.controller.transfer_manager.set_current_sync(sync_widget)
                self.controller.transfer_widget.add_sync_reporting(sync_widget)
                
            # Do downloads
            if answer_dl == 0:
                # Update ui and log
                post_files = " file from " if total_dl_files == 1 else " files from "
                post_folders = " folder" if total_dl_folders == 1 else " folders"
                banner_total_size_string = ", total of " + self.datahandler.humanize_bytes(total_dl_bytes)
                message = "Downloading " + str(total_dl_files) + post_files + str(total_dl_folders) + post_folders + banner_total_size_string
                self.logger.sync(message)

                for sync_result in self.sync_total_results:
                    # Create directory
                    if sync_result.local_folder_exists == False:
                        sync_result.create_local_path()
                    # Queue downloads
                    for sync_file in sync_result.out_of_date_files:
                        self.connection.get_file(sync_file.path, sync_file.root, sync_result.local_path + "/" + sync_file.get_name(), sync_file.size, sync_file.mime_type, True)
            elif answer_dl == 1:
                self.logger.sync("Ignoring downloads")
            elif answer_dl == -1:
                self.logger.sync("No synchronization downloads, all file up to date")    
              
            # Do uploads
            if answer_ul == 0:
                post_ul_files = " file and creating " if total_ul_files == 1 else " files and "
                post_ul_folders = " folder" if total_ul_folders == 1 else " folders"
                banner_total_ul_size_string = ", total of " + self.datahandler.humanize_bytes(total_ul_bytes)
                message_ul = "Uploading " + str(total_ul_files) + post_ul_files + str(total_ul_folders) + post_ul_folders + banner_total_ul_size_string
                self.logger.sync(message_ul)
                
                # Create new remote dirs
                if len(create_new_folders) > 0:
                    create_new_folders.sort() # sort so we create forlder from bottom up
                    for remote_path in create_new_folders:
                        if self.connection.create_folder_blocking(remote_path):
                            self.logger.info("Created remote folder " + remote_path + " succesfully")
                        else:
                            self.logger.info("Failed to create remote folder " + remote_path)

                for sync_result in self.sync_total_results:
                    # Queue uploads
                    for ul_sync_file in sync_result.out_of_date_files_upload:
                        self.connection.upload_file(sync_result.remote_path, "dropbox", ul_sync_file, True)
                    for ul_sync_file in sync_result.new_files_to_upload:
                        self.connection.upload_file(sync_result.remote_path, "dropbox", ul_sync_file, True)
            elif answer_ul == 1:
                self.logger.sync("Ignoring uploads")
            elif answer_dl == -1:
                self.logger.sync("No synchronization uploads, all file up to date")    
                       
            if sync_widget != None:
                self.ui.show_transfer_widget()
            else:
                self.ui.set_synching(False)
        else:
            self.ui.show_banner("Nothing to sync - all files up to date")
            self.ui.set_synching(False)

        # Cleanup
        del confirmation_dl
        del confirmation_ul


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


""" SyncDialog is for showing information of sync results and provides button for how to proceed """
        
class SyncDialog(QMessageBox):

    def __init__(self, par):
        QMessageBox.__init__(self)
                    
        # Grid layout
        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(15)
        self.grid_layout.setContentsMargins(0,0,0,0)
        
        # Make a main widget with the grid layout
        self.widget = QWidget()
        self.widget.setFont(QFont("Arial", 14))
        self.widget.setLayout(QVBoxLayout())
        self.widget.layout().addLayout(self.grid_layout)
        
        # Make a scrollview for the box itself
        self.view = QScrollArea()
        self.view.setWidget(self.widget)
        self.view.setWidgetResizable(True)
        self.view.setMinimumHeight(360)

        # Add view and show dialog
        self.layout().setHorizontalSpacing(0)
        self.layout().setVerticalSpacing(0)
        self.layout().setContentsMargins(0,0,10,10)
        self.layout().addWidget(self.view, 0, 0)
        self.layout().addWidget(self.view, 0, 0)
        
        # Internal data
        self.row = -1
        self.style_title = "QLabel { font-size: 20pt; color: #0099FF; font-weight: bold;}"
        self.style_totals = "QLabel { font-size: 14pt; color: rgb(94,189,0); }"
        
        self.new_file_widgets = []
        
        self.label_total_files = None
        self.label_total_size = None

    def iterate_row(self):
        self.row += 1

    def add_spacer(self, height = 15):
        self.iterate_row()
        self.grid_layout.addItem(QSpacerItem(1, height, QSizePolicy.Fixed, QSizePolicy.Fixed), self.row, 0)
        
    def finalize(self):
        self.widget.layout().addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Expanding))

    def add_titles(self, text1, text2 = None, text3 = None):
        self.iterate_row()
        l1 = QLabel(text1)
        l1.setStyleSheet(self.style_title)
        if text2 != None:
            l2 = QLabel(text2)
            l2.setStyleSheet(self.style_title)
        else:
            l2 = None
        if text3 != None:
            l3 = QLabel(text3)
            l3.setStyleSheet(self.style_title)
        else:
            l3 = None
        self.add_widgets(l1, l2, l3)
                
    def add_row(self, text1, text2 = None, text3 = None):
        self.iterate_row()
        l1 = QLabel(text1)
        l2 = None
        l3 = None
        if text2 != None:
            l2 = QLabel(text2)
        if text3 != None:
            l3 = QLabel(text3)
        self.add_widgets(l1, l2, l3)
        
        if text2 == "NEW FILE":
            self.new_file_widgets.append(l1)
            self.new_file_widgets.append(l2)
            self.new_file_widgets.append(l3)
            
    def add_totals(self, text1, text2 = None, text3 = None):
        self.iterate_row()
        l1 = QLabel(text1)
        l1.setStyleSheet(self.style_totals)
        if text2 != None:
            l2 = QLabel(text2)
            l2.setStyleSheet(self.style_totals)
            self.label_total_files = l2
        else:
            l2 = None
        if text3 != None:
            l3 = QLabel(text3)
            l3.setStyleSheet(self.style_totals)
            self.label_total_size = l3
        else:
            l3 = None
        self.add_widgets(l1, l2, l3)
        
    def add_widgets(self, w1, w2, w3, align = Qt.AlignBottom):
        self.grid_layout.addWidget(w1, self.row, 0, align)
        if w2 != None:
            self.grid_layout.addWidget(w2, self.row, 1, align)
        if w3 != None:
            self.grid_layout.addWidget(w3, self.row, 2, align | Qt.AlignRight)

    def hide_new_uploads(self):
        for w in self.new_file_widgets:
            w.hide()
            
    def set_totals(self, files, size):
        if self.label_total_files != None:
            self.label_total_files.setText(files)
        if self.label_total_size != None:
            self.label_total_size.setText(size)


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
        
        self.sync_widget = None

    def set_client(self, client):
        self.client = client
        
    def set_current_sync(self, widget):
        self.sync_widget = widget
        
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
        
        if sync_download and self.sync_widget != None:
            download.setup_reporting(self.sync_widget)
            self.tranfer_to_widget[download] = self.sync_widget
        else:
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
        
        if sync_upload and self.sync_widget != None:
            upload.setup_reporting(self.sync_widget)
            self.tranfer_to_widget[upload] = self.sync_widget
        else:
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
        self.report = None

    def set_download_info(self, file_name, device_store_path):
        self.file_name = file_name
        self.store_path = device_store_path
        
    def set_upload_info(self, file_name, dropbox_store_path):
        self.file_name = file_name
        self.store_path = dropbox_store_path
        
    def setup_reporting(self, report):
        self.report = report
        
    def run(self):
        encoded_params = []
        for param in self.parameters:
            param = self.encode_unicode(param)
            encoded_params.append(param)

        try:
            # Reporting
            if self.report != None:
                self.report.started(self.transfer_type, self.file_name)
                
            self.response = self.method(*tuple(encoded_params))
            if self.response != None:
                if self.transfer_type == "Download":
                    self.data = self.response.read()
                else:
                    self.data = self.response.data
            else:
                self.error = "Response None, with status code " + self.response.status
                self.data = None
                
            # Reporting
            if self.report != None:
                self.report.completed(self.transfer_type, self.file_name)
        except (socket.error, socket.gaierror), err:
            self.response = None
            self.error = err
            self.data = None
            if self.report != None:
                self.report.failed(self.transfer_type, self.file_name)
        
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
        
    def add_sync_reporting(self, sync_widget):
        self.ui.item_layout.insertWidget(0, sync_widget)
        sync_widget.show()
        self.layout_check()
        
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
                

""" SyncTransferItem is a custom list widget that shows tranfer status of a sync """

class SyncTransferItem(QWidget):
    
    def __init__(self, parent):
        QWidget.__init__(self)
        self.ui = Ui_SyncTransferItem()
        self.ui.setupUi(self)
        self.parent = parent
        
        self.total_dl = 0
        self.total_ul = 0
        self.current_dl = 0        
        self.current_ul = 0
        
        self.sync_icon = QPixmap(self.parent.datahandler.datapath("ui/icons/item_sync.png"))
        self.set_icon(self.sync_icon)
        
        self.ui.dl_status.setText("Waiting...")
        self.ui.ul_status.setText("Waiting...")
        
        self.downloads_done = False
        self.uploads_done = False
        self.internal_do_started = False
        self.internal_do_completed = False
        
        self.loading_animation = QMovie(self.parent.datahandler.datapath("ui/images/loading.gif"), "GIF")
        self.loading_animation.setCacheMode(QMovie.CacheAll)
        self.loading_animation.setScaledSize(QSize(48,48))
        self.loading_animation.setSpeed(75)

        self.timer_dl = QTimer()
        self.timer_dl.timeout.connect(self.set_dl_duration)
        self.dl_duration_sec = 0
        self.dl_duration_min = 0
        
        self.timer_ul = QTimer()
        self.timer_ul.timeout.connect(self.set_ul_duration)
        self.ul_duration_sec = 0
        self.ul_duration_min = 0
        
        self.poller = QTimer()
        self.poller.timeout.connect(self.poll_input)
        self.poller.start(50)

    def set_dl_duration(self):
        self.dl_duration_sec += 1
        if self.dl_duration_sec == 60:
            self.dl_duration_min += 1
            self.dl_duration_sec = 0
        if self.dl_duration_min > 0 and self.dl_duration_sec < 10:
            duration = "0" + str(self.dl_duration_sec) + " sec"
        else:
            duration = str(self.dl_duration_sec) + " sec"
        if self.dl_duration_min > 0:
            duration = str(self.dl_duration_min) + " min " + duration
        self.ui.dl_timer_label.setText(duration)
        
    def set_ul_duration(self):
        self.ul_duration_sec += 1
        if self.ul_duration_sec == 60:
            self.ul_duration_min += 1
            self.ul_duration_sec = 0
        if self.ul_duration_min > 0 and self.ul_duration_sec < 10:
            duration = "0" + str(self.ul_duration_sec) + " sec"
        else:
            duration = str(self.ul_duration_sec) + " sec"
        if self.ul_duration_min > 0:
            duration = str(self.ul_duration_min) + " min " + duration
        self.ui.ul_timer_label.setText(duration)
        
    def set_status(self, status):
        self.ui.status_label.setText(status)
        
    def set_totals(self, download, upload):
        self.total_dl = download
        self.total_ul = upload
        self.ui.dl_total.setText(str(download))
        self.ui.ul_total.setText(str(upload))
        
        if self.total_dl == 0:
            self.downloads_done = True
            self.ui.dl_status.setText("")
            self.ui.dl_total.setText("-")
            self.ui.dl_present.setText("-")
            self.ui.dl_separator2.hide()
            self.ui.dl_size.hide()
        if self.total_ul == 0:
            self.uploads_done = True
            self.ui.ul_status.setText("")
            self.ui.ul_total.setText("-")
            self.ui.ul_present.setText("-")
            self.ui.ul_separator2.hide()
            self.ui.ul_size.hide()
            
    def set_sizes(self, download, upload):
        self.ui.dl_size.setText(download)
        self.ui.ul_size.setText(upload)
            
    def iter_downloads(self):
        if self.current_dl == 0:
            self.timer_dl.start(1000)
        self.current_dl += 1
        self.ui.dl_present.setText(str(self.current_dl))
        if self.current_dl == self.total_dl:
            self.timer_dl.stop()
            self.downloads_done = True
            self.ui.dl_status.setText("")
            self.check_completed()
        
    def iter_uploads(self):
        if self.current_ul == 0:
            self.timer_ul.start(1000)
        self.current_ul += 1
        self.ui.ul_present.setText(str(self.current_ul))
        if self.current_ul == self.total_ul:
            self.timer_ul.stop()
            self.uploads_done = True
            self.ui.ul_status.setText("")
            self.check_completed()
        
    def set_icon(self, pixmap):
        self.ui.main_icon.setPixmap(pixmap)
            
    def set_started(self, status = None):
        pass
        
    def set_completed(self, status = None):
        pass
    
    def set_failed(self, status = None):
        pass

    def poll_input(self):
        if self.internal_do_completed:
            self.completed_internal()
        if self.internal_do_started:
            self.started_internal()
                    
    def started(self, transfer_type, filename):
        self.internal_do_started = True
        self.internal_start_type = transfer_type
        self.internal_start_filename = filename
                
    def started_internal(self):
        if self.downloads_done == False or self.uploads_done == False:
            if self.loading_animation.state() != QMovie.Running:
                self.ui.main_icon.setMovie(self.loading_animation)
                self.loading_animation.start()
    
        self.set_status(self.internal_start_type + "ing...")
        if self.internal_start_type == "Download":
            self.ui.dl_status.setText("Processing " + self.internal_start_filename)
        else:
            self.ui.ul_status.setText("Processing " + self.internal_start_filename)
        self.internal_do_started = False
                
    def completed(self, transfer_type, filename):
        self.internal_do_completed = True
        self.internal_iter_type = transfer_type
        
    def completed_internal(self):
        if self.internal_iter_type == "Download":
            self.iter_downloads()
        else:
            self.iter_uploads()
        self.internal_do_completed = False
        
    def failed(self, transfer_type, filename):
        print "Failed   : " + transfer_type + " --- " + filename
        
    def check_completed(self):
        if self.downloads_done and self.uploads_done:
            self.sync_complete()
    
    def sync_complete(self):
        self.ui.status_label.setText("Synchronization completed")
        self.ui.dl_status.setText("")
        self.ui.ul_status.setText("")
        self.loading_animation.stop()
        self.set_icon(self.sync_icon)
        self.parent.ui.set_synching(False)
        self.ui.content_frame.setStyleSheet("QFrame#content_frame{border: 0px;border-bottom: 1px solid grey;background-color: \
            qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 7, 0, 255), stop:0.502513 rgba(0, 50, 0, 200), stop:1 rgba(0, 0, 0, 255));}")
        
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

