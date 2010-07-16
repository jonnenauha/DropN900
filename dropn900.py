
import sys
import os

from PyQt4 import QtCore, QtGui
from dropbox import client, rest, auth
from oauth import oauth
from httplib import CannotSendRequest, BadStatusLine
from ConfigParser import ConfigParser, SafeConfigParser, NoSectionError

from uicontroller import UiController
from connectionmanager import ConnectionManager

""" Main programs controller, instantiates all the nessesary classes, starts ui and auth """

class DropN900(QtCore.QObject):

    def __init__(self, debug_enabled = False):
        self.ui = UiController(self, debug_enabled)
        self.connection = ConnectionManager(self, self.ui)
        self.ui.tree_controller.set_connection(self.connection)
        
    def start(self):
        self.ui.show()
        self.reset_variables()
        self.check_for_data_folder()
        self.check_for_auth("token.ini")

    def reset_variables(self):
        self.authenticator = None
        self.request_token = None
        self.connected = False

    def check_for_data_folder(self):
        home_dir = QtCore.QDir.home()
        if home_dir.absolutePath() == "/home/user":
            if not home_dir.cd("DropN900"):
                home_dir.mkdir("DropN900")
                
    def check_for_auth(self, file):
        token_config = SafeConfigParser()
        token_config.read(file)
        try:
            access_key = token_config.get("token", "key")
            access_secret = token_config.get("token", "secret")
            if access_key != "" and access_secret != "":
                self.log("Found a stored auth token")
                self.init_dropbox_client(oauth.OAuthToken(access_key, access_secret))
            else:
                self.log("Access token invalid, starting auth")
                self.reset_auth()
        except NoSectionError:
            self.log("No stored auth access tokens found, starting auth")
            self.start_auth()

    def store_auth(self, access_token):
        self.log("Storing recieved access token")
        
        token_config = ConfigParser()
        token_config.add_section("token")
        token_config.set("token", "secret", access_token.secret)
        token_config.set("token", "key", access_token.key)
        
        write_file = open("token.ini", "w")
        token_config.write(write_file)
        write_file.close()

    def reset_auth(self):
        os.remove("token.ini")
        self.start_auth()
    
    def start_auth(self):
        if not self.authenticator:
            self.authenticator = auth.Authenticator(self.get_config())
        try:
            self.request_token = self.authenticator.obtain_request_token()
            authurl = self.authenticator.build_authorize_url(self.request_token)
            self.ui.load_login(authurl)
        except AssertionError:
            self.log("ERROR - Could not init DropBox connection, errors occurred!")
            self.request_token = None

    def end_auth(self):
        if not self.request_token:
            self.log("WARNING - Cannot continue authentication, request token invalid. Restart DropN900!")
            return
        dropbox_config = self.get_config()
        try:
            access_token = self.authenticator.obtain_access_token(self.request_token, dropbox_config["verifier"])
        except CannotSendRequest, BadStatusLine:
            self.log("ERROR - httplib exception catched from dropbox client code while obtaining access token!")
            return
        except:
            self.log("ERROR - Unkown exceptions occurred while obtaining access token!")
            return
        self.store_auth(access_token)
        self.init_dropbox_client(access_token)

    def init_dropbox_client(self, access_token):
        dropbox_config = self.get_config()
        server = dropbox_config["server"]
        content_server = dropbox_config["content_server"]

        if not self.authenticator:
            self.authenticator = auth.Authenticator(dropbox_config)
            
        dropbox_client = client.DropboxClient(server, content_server, 80, self.authenticator, access_token)

        self.log("DropBox connection initialised...")
        self.connection.set_client(dropbox_client)
        self.ui.switch_context("manager")
        self.connected = True

    def get_config(self):
        return auth.Authenticator.load_config("config.ini")
    
    def log(self, msg, param = None):
        if param is None:
            self.ui.log(msg)
        else:
            msg_join = msg + " %s" % param
            self.ui.log(msg_join)       

""" This is the main function that starts the program """

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dropn900 = DropN900(True) # Remove param to disable debug prints
    dropn900.start()
    os._exit(app.exec_())
