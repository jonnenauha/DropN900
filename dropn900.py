#!/usr/bin/python2.5

import sys
import os

from PyQt4 import QtCore, QtGui
from dropbox import client, rest, auth
from oauth import oauth
from httplib import socket 
from httplib import CannotSendRequest, BadStatusLine
from ConfigParser import ConfigParser, SafeConfigParser, NoSectionError

from uicontroller import UiController
from data import MaemoDataHandler
from connectionmanager import ConnectionManager
from logger import Logger
from settings import ConfigHelper, SettingsWidget
from transfers import SyncManager, TransferManager, TransferWidget

""" Main programs controller, instantiates all the nessesary classes, starts ui and auth """

class DropN900(QtCore.QObject):

    def __init__(self, debug_mode = False, maemo_env = True):
        self.logger = Logger(debug_mode)
        
        # Setup data handler and config helper
        self.datahandler = MaemoDataHandler(self, maemo_env, self.logger)
        self.config_helper = ConfigHelper(self.datahandler, self.logger)
        
        # Setup ui
        self.ui = UiController(self, debug_mode, self.logger)
        self.logger.set_ui(self.ui)
        self.settings_widget = SettingsWidget(self.ui, self.config_helper, self.logger)

        # Setup connection
        self.connection = ConnectionManager(self, self.ui, self.logger, maemo_env)
        
        # Create transfer managers and widget
        self.sync_manager = SyncManager(self)
        self.transfer_manager = TransferManager(self)
        self.transfer_widget = TransferWidget(self.transfer_manager)

        # Pass objects around
        self.ui.tree_controller.setup(self.connection)
        self.settings_widget.setup(self.connection, self.sync_manager)
        self.ui.set_settings_widget(self.settings_widget)
        self.ui.set_transfer_widget(self.transfer_widget)
        self.transfer_manager.set_transfer_widget(self.transfer_widget)
            
    def start(self):
        # Show ui
        self.ui.show()
        # Some validations
        self.authenticator = None
        self.request_token = None
        self.login_done = False
        self.connected = False
        # Start by checking existing auth
        self.check_for_auth(self.datahandler.configpath("token.ini"))
                
    def check_for_auth(self, filename):
        token_config = SafeConfigParser()
        token_config.read(filename)
        try:
            access_key = token_config.get("token", "key")
            access_secret = token_config.get("token", "secret")
            if access_key != "" and access_secret != "":
                self.logger.config("Found existing access token")
                self.login_done = True
                self.init_dropbox_client(oauth.OAuthToken(access_key, access_secret))
            else:
                self.logger.error("Parsing access token from file failed")
                self.datahandler.reset_auth()
        except NoSectionError:
            self.logger.config("No stored access token found")
            self.start_trusted_auth()
    
    def start_trusted_auth(self):
        self.login_done = False
        self.ui.switch_context("trustedlogin")
    
    def end_trusted_auth(self, email, password):
        self.login_done = False
        if self.connection.connection_available():
            if self.authenticator:
                del self.authenticator
            self.authenticator = auth.Authenticator(self.get_config())
            try:
                access_token = self.authenticator.obtain_trusted_access_token(email, password)
            except AssertionError:
                self.ui.set_trusted_login_error("Email and/or password invalid")
                return
            except socket.gaierror:
                self.ui.set_trusted_login_info("Requesting a network connection...")
                self.connection.request_connection()
                return
            self.login_done = True
            self.datahandler.store_auth(access_token)
            self.init_dropbox_client(access_token)
        else:
            self.ui.set_trusted_login_info("Requesting a network connection...")
            self.connection.request_connection()
    
    def init_dropbox_client(self, access_token):
        dropbox_config = self.get_config()
        server = dropbox_config["server"]
        content_server = dropbox_config["content_server"]
        if not self.authenticator:
            self.authenticator = auth.Authenticator(dropbox_config)
        dropbox_client = client.DropboxClient(server, content_server, 80, self.authenticator, access_token)
        self.connection.set_client(dropbox_client)
        self.ui.switch_context("manager")
        self.connected = True

    def get_config(self):
        return auth.Authenticator.load_config(self.datahandler.datapath(".config"))


""" This is the main function that starts the program

    * Set debug if you want to get stdout prints from python
      this is meant for scratchbox so you dont have to constantly look at console widget
    * Set maemo_env if you are running in the device
      other wise set to False when running in scratchbox"""
      
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    debug = True
    maemo_env = True
    dropn900 = DropN900(debug, maemo_env)
    dropn900.start()
    os._exit(app.exec_())

