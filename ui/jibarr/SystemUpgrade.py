import os, shutil, json, time, subprocess, urllib, zipfile, sys
from jibarr.models import SiteSettings, Logs
from urllib.request import urlopen
from datetime import datetime
from os.path import dirname, abspath
from distutils.dir_util import copy_tree
from django.db import connection
import sqlite3
from sqlite3 import OperationalError
from django.core.cache import cache

def SystemUpgrade(toVer):
    try:
        Logs.objects.create(log_type='Upgrade',log_category='System',log_message='System Upgrade (' + toVer + ') initiated',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except:
        pass

    isSuccessful = True
    
    time.sleep(1)
    # 1) Backup the DB
    isSuccessful = backupDatabase()
    time.sleep(1)
    
    # 2) Download new files
    if isSuccessful:
        try:
            isSuccessful = downloadZipFile()
        except:
            isSuccessful = False
            pass

    # 3) Unzip files
    if isSuccessful:
        try:
            isSuccessful = unzipZipFile()
        except:
            isSuccessful = False
            pass

    # 4) Run Schema updates
    if isSuccessful:
        try:
            curDbVer = SiteSettings.jibarr_version
            isSuccessful = upgradeDatabase(curDbVer,toVer)
        except:
            isSuccessful = False
            pass

    # 5) Run file copies
    if isSuccessful:
        try:
            isSuccessful = upgradeCode()
        except:
            isSuccessful = False
            pass

    # 6) Update DB Version
    #    This is happening in step 4 today, change it!!

    # 7) Cleanup files
    if isSuccessful:
        try:
            isSuccessful = cleanupFiles
        except:
            isSuccessful = False
            pass

    # 8) Clear the cached Upgrade Needed indicator
    if isSuccessful:
        try:
            CACHE_KEY_NEWVERSION = 'NEWVERSION'
            cache.delete(CACHE_KEY_NEWVERSION)
            SiteSettings.checkVersion()
        except:
            isSuccessful = False
            pass

    if isSuccessful:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='System Upgrade completed successfully.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except KeyError:
            pass
    else:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='System Upgrade failed!!!!',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except KeyError:
            pass
    
    return isSuccessful

def backupDatabase():
    isSuccessful = True
    try:
        Logs.objects.create(log_type='Backup',log_category='System',log_message='Database backup initiated.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except KeyError:
        pass

    try:
        d = dirname(dirname(abspath(__file__)))
        ts = str(datetime.now().strftime("%Y%m%d%H%M%S"))
        shutil.copy2(os.path.join(d, "db.sqlite3"), os.path.join(d, "./backup/db.sqlite3." + ts + ".bak"))
    except KeyError:
        isSuccessful = False
        pass

    time.sleep(1)
    if isSuccessful:
        try:
            Logs.objects.create(log_type='Backup',log_category='System',log_message='Database backup completed successfully.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except KeyError:
            pass
    else:
        try:
            Logs.objects.create(log_type='Backup',log_category='System',log_message='Database backup failed!!!!',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except KeyError:
            pass

    return isSuccessful

def upgradeDatabase(curVer,newVer):
    isSuccessful = True
    try:
        Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Database upgrade initiated.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except:
        pass

    try:
        fd = open("./unzip/jibarr-master/jibarr/ui/dbupgrades/v" + curVer + "_to_v" + newVer + ".txt","r")
        sqlFile = fd.read()
        fd.close()
        conn = sqlite3.connect('./ui/db.sqlite3')
        c = conn.cursor()
        sqlCommands = sqlFile.split(';')
        for command in sqlCommands:
            c.execute(command)
    except OperationalError as msg:
        isSuccessful = False
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Database upgrade error: ' + msg,log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass
        pass
    except:
        isSuccessful = False
        pass

    time.sleep(1)
    if isSuccessful:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Database upgrade completed successfully.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass
    else:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Database upgrade failed!!!!',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass

    return isSuccessful

def upgradeCode():
    # RAW - https://github.com/ExtensiveJS/Jibarr/archive/master.zip
    # D:\Temp\gitTest\Jibarr
    d = dirname(dirname(abspath(__file__)))
        
    isSuccessful = True
    try:
        Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Code upgrade initiated.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except:
        pass

    if isSuccessful:
        try:
            # copy the files from the unzip to the app folder
            if os.path.exists(os.path.join(d, "./unzip/jibarr-master/jibarr/")):
                rootpath = os.path.abspath(os.path.join(d,".."))
                copy_tree(os.path.join(d, "./unzip/jibarr-master/jibarr/"),rootpath) 
                time.sleep(1) 
        except:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Code Upgrade Error: Error replacing updated files.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            isSuccessful = False
            pass

    time.sleep(1)
    if isSuccessful:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Code upgrade completed successfully.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass
    else:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Code upgrade failed!!!!',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass

    return isSuccessful

def downloadZipFile():
    isSuccessful = True
    d = dirname(dirname(abspath(__file__)))
    try:
        Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Downloading updated code base initiated.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except:
        pass
    try:
        url = 'https://github.com/ExtensiveJS/Jibarr/archive/master.zip'
        file_name = os.path.join(d, "./unzip/jibarr-master.zip")
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
    except:
        isSuccessful = False
        pass
    time.sleep(1)
    if isSuccessful:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Downloading updated code base completed.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass
    else:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='ERROR: Downloading updated code base failed.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass

    return isSuccessful

def unzipZipFile():
    isSuccessful = True
    d = dirname(dirname(abspath(__file__)))
    try:
        Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Unzip of updated code base initiated.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except:
        pass
    try:
        with zipfile.ZipFile(os.path.join(d, "./unzip/jibarr-master.zip"),"r") as zip_ref:
            zip_ref.extractall(os.path.join(d, "./unzip/jibarr-master/"))
            time.sleep(1)
        # rename the unzipped subfolder to make it easier to use
        if os.path.exists(os.path.join(d, "./unzip/jibarr-master/")):
            os.rename(os.path.join(d,"./unzip/jibarr-master/jibarr-master"),os.path.join(d,"./unzip/jibarr-master/jibarr"))
        # remove the db file from the uzip
        if os.path.exists(os.path.join(d, "./unzip/jibarr-master/jibarr/ui/db.sqlite3")):
            os.remove(os.path.join(d, "./unzip/jibarr-master/jibarr/ui/db.sqlite3"))
            time.sleep(1)     
        # remove the .vscode files
        if os.path.exists(os.path.join(d, "./unzip/jibarr-master/jibarr/.vscode/")):
            shutil.rmtree(os.path.join(d, "./unzip/jibarr-master/jibarr/.vscode/"))
            time.sleep(2)
    except:
        isSuccessful = False
        pass
    time.sleep(1)
    if isSuccessful:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Unzip of code base completed.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass
    else:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='ERROR: Unzip of code base failed.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass

    return isSuccessful

def cleanupFiles():
    isSuccessful = True
    d = dirname(dirname(abspath(__file__)))
    try:
        Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Cleanup of downloaded code base initiated.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except:
        pass
    try:
        if os.path.exists(os.path.join(d, "./unzip/jibarr-master/")):
            shutil.rmtree(os.path.join(d, "./unzip/jibarr-master/"))
            time.sleep(1)
    except:
        isSuccessful = False
        pass
    time.sleep(1)
    if isSuccessful:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Cleanup of downloaded code base completed.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass
    else:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='ERROR: Cleanup of downloaded code base failed.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass

    return isSuccessful

