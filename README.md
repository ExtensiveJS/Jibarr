# MediaFileSync ![alt text](https://github.com/ExtensiveJS/MediaFileSync/blob/master/ui/MediaFileSync/static/mediafilesync/images/MFS_Logo.png?raw=true "MediaFileSync") 

Utility to allow you to track files that need to be synced to secondary drives. 

The intent of this project is to have a utility that will allow files to be copied to secondary drives.

## Key features to be included:
* a list of all available media from the source
* a "last updated" date tracked, per user/device, to allow for syncing "new" items
* ability to pull data from RADARR for a listing of entries to include
* ability to have multiple profiles
* cross platform, OS independent

## Features that would be ideal to include:
* ability to pull data from SONARR for a listing of entries to include (Future Release)
* ability to pull data from LIDARR for a listing of entries to include (Future Release)

## To Run/Install:
* Using pip install -r requirements.txt OR
* Install Python 3.7
* Install DJango
* Install djangorestframework
* Install celery
* Run django (point it to the ui\manage.py )
    * PYTHON.EXE \path\to\ui\manage.py runserver 8125
* Open a web browser to http://localhost:8125/MediaFileSync


