import os, shutil, json, time, subprocess, urllib, zipfile
from jibarr.models import SiteSettings, Logs
from urllib.request import urlopen
from datetime import datetime
from os.path import dirname, abspath
from distutils.dir_util import copy_tree

def SystemUpgrade():
    try:
        Logs.objects.create(log_type='Upgrade',log_category='System',log_message='System Upgrade initiated',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except KeyError:
        pass

    #currentDir = os.path.dirname(os.path.realpath(__file__)) #D:\\Sandbox\\Jibarr\\ui\\jibarr
    isSuccessful = True
    
    time.sleep(1)
    # 1) Backup the DB
    isSuccessful = backupDatabase()
    time.sleep(1)
    
    # 2) Upgrade DB - only if it needs to be
    if isSuccessful:
        if SiteSettings.checkDBVersion():
            isSuccessful = upgradeDatabase()
            time.sleep(1)
        else:
            try:
                Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Database upgrade not needed.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass

    time.sleep(1)
    # 3) Upgrade Code - only if it needs to be
    if isSuccessful:
        if SiteSettings.checkCodeVersion():
            isSuccessful = upgradeCode()
            time.sleep(1)
        else:
            try:
                Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Code upgrade not needed.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass

    # 4) Restart?
    #time.sleep(1)

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

def upgradeDatabase():
    isSuccessful = True
    try:
        Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Database upgrade initiated.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except KeyError:
        pass

    

    time.sleep(1)
    if isSuccessful:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Database upgrade completed successfully.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except KeyError:
            pass
    else:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Database upgrade failed!!!!',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except KeyError:
            pass

    return isSuccessful

def upgradeCode():
    # RAW - https://github.com/ExtensiveJS/Jibarr/archive/master.zip
    # D:\Temp\gitTest\Jibarr
    d = dirname(dirname(abspath(__file__)))
        
    isSuccessful = True
    try:
        Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Code upgrade initiated.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except KeyError:
        pass

    try:
        url = 'https://github.com/ExtensiveJS/Jibarr/archive/master.zip'
        file_name = os.path.join(d, "./unzip/jibarr-master.zip")
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
    except:
        Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Code Upgrade Error: Error downloading update ZIP file.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        isSuccessful = False
        pass

    if isSuccessful:
        try:
            with zipfile.ZipFile(os.path.join(d, "./unzip/jibarr-master.zip"),"r") as zip_ref:
                zip_ref.extractall(os.path.join(d, "./unzip/jibarr-master/"))
                time.sleep(1)
        except:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Code Upgrade Error: Error unzipping update file.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            isSuccessful = False
            pass

    if isSuccessful:
        try:
            # remove the db file from the uzip
            if os.path.exists(os.path.join(d, "./unzip/jibarr-master/ui/db.sqlite3")):
                os.remove(os.path.join(d, "./unzip/jibarr-master/ui/db.sqlite3"))
                time.sleep(1)
            # copy the files from the unzip to the app folder
            if os.path.exists(os.path.join(d, "./unzip/jibarr-master/")):
                copy_tree(os.path.join(d, "./unzip/jibarr-master/"),"D:\\Temp\\gitTest\\Jibarr")
                time.sleep(1)
            # remove the unzip files
            if os.path.exists(os.path.join(d, "./unzip/jibarr-master/")):
                shutil.rmtree(os.path.join(d, "./unzip/jibarr-master/"))
                time.sleep(1)
            # remove the zip file
            if os.path.exists(os.path.join(d, "./unzip/jibarr-master.zip")):
                os.remove(os.path.join(d, "./unzip/jibarr-master.zip"))
        except:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Code Upgrade Error: Error replacing updated files.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            isSuccessful = False
            pass

    time.sleep(1)
    if isSuccessful:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Code upgrade completed successfully.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except KeyError:
            pass
    else:
        try:
            Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Code upgrade failed!!!!',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except KeyError:
            pass

    return isSuccessful