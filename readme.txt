DropN900 - a maemo5 dropbox client
==================================

Dropbox released a public (mobile) API to their services some time ago.
As the maemo 5 platform was lacking a native client for the dropbox services,
I wanted to make one. I use the dropbox provided python API client and PyQt4.

Current capabilities
====================

- Web authentication to dropbox, you only give your password to the dropbox website, 
  the DropN900 app will never see it or store it. An OAuth access token is stored and 
  reused so the user wont have to authenticate on every session.
  
- Read/Write access to the DropN900 application folder
  * DropBox does not automatically let you roam free on users root folder. 
    This access has to be requested and I'm in the process of doing this.

- Create new folder, rename file/folder, upload file, download file, remove file/folder.

- Image file thumbnail preview, loading animations and showing results for actions.

- Threaded networking (non-bloking) so you'll have a smooth user experience while
  network I/O is happening. Otherwise ui would freeze on all calls to the dropbox
  API.

Notes
=====

1. You cant do anything with this code alone. The python dependencies are PyQt4, poster,
   oauth and python-dropbox-client. These are currently not anywhere in the maemo repos.
   I will have to make .deb packages on all of these in order for anyone to get the app
   from the app manager in maemo 5.
   
2. This repo is missing the config file that makes the python-dropbox-client work. As
   this file has the apps consumer key and secret I wont make it public yet. I will
   consult with dropbox how to solve this. As it would be very bad to just have my
   private oauth credentials in a config file or in the python code that is readable.

3. I have modified the python-dropbox-client client.py metadata function to include hash
   in the params when one is available. This hash gives better performance as it wont list
   metadata back if the content of that folder has not changed. Saves time and networking.
   I'm hoping they would include this in their code so I could use the unmodified lib.
 
Known bugs
==========

I have tested the app on my Nokia N900 (PR1.2) with latest PyQt4 and found the following:

#001 Download/upload dialogs
  
  PyQt4.QFileDialog.getExistingDirectory() and PyQt4.QFileDialog.getOpenFileName() 
  both show strange names on titles etc. These dialogs are used when downloading/uploading files.
  They are usable but not very pretty. This seems to be a bug in PyQt4.
  
  Status: Not Fixed
  Suggestion: Waiting for PyQt4 fix or will make a custom dialog
  
#002 Fail to obtain access token after web browser authentication

  http lib exceptions from python-dropbox-client code once calling Authenticator.obtain_access_token()
  with authenticated request token. Bug is quite random, sometimes happens sometimes not, cant
  figure a pattern out.
  
  Status: Not fixed
  Suggestion: Get mobile auth access to dropbox so we can skip playing around with separate web browser auth

Contact
=======
email: jonne.nauha@evocativi.com
irc: Pforce @ freenode/IRCnet/Qnet

Changelog
=========

No public releases to the maemo repos have been made yet.
