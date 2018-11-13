# MediaFileSync
Utility to allow you to track files that need to be synced to secondary drives. 

The intent of this project is to have a utility that will allow files to be copied to secondary drives.

Key features (intended) to be included:
* a list of all available files/folders from the source
* a "last updated" date tracked, per user/device, to allow for syncing "new" items
* ability to have multiple sources
* a friendly UI to allow user/device listings and the ability to include/exclude per entry
* cross platform, OS independent
* planning for a python backend.
* planning on a django GUI (yet to be determined)

Features that would be ideal to include:
* ability to pull data from SONARR for a listing of entries to include
* ability to pull data from RADARR for a listing of entries to include

To Run/Install
* Using pip install -r requirements.txt OR
* Install Python 3.7
* Install DJango
* Install djangorestframework
* Run django (point it to the ui\manage.py )
    * PYTHON.EXE \path\to\ui\manage.py runserver 8125
* Open a web browser to http://localhost:8125/MediaFileSync


