import os, shutil, json, time, subprocess
from jibarr.models import SiteSettings, Logs
from urllib.request import urlopen
from datetime import datetime
from os.path import dirname, abspath

def SystemUpgrade():
    try:
        Logs.objects.create(log_type='Upgrade',log_category='System',log_message='System Upgrade initiated',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except KeyError:
        pass

    isSuccessful = True
    
    time.sleep(1)
    # 1) Backup the DB
    isSuccessful = backupDatabase()

    time.sleep(1)
    # 2) Upgrade DB
    if isSuccessful:
        isSuccessful = upgradeDatabase()

    time.sleep(1)
    # 3) Upgrade Code (git fetch origin master)

    if isSuccessful:
        isSuccessful = upgradeCode()

    # 4) Restart?

    time.sleep(1)
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
        shutil.copy2(os.path.join(d, "db.sqlite3"), os.path.join(d, "./db.sqlite3." + ts + ".bak"))
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
    # GIT - git fetch origin master
    # git update-index --assume-unchanged Localization/el-GR.js

    # D:\Temp\gitTest\Jibarr

    isSuccessful = True
    try:
        Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Code upgrade initiated.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except KeyError:
        pass

    try:
        ret = subprocess.check_output("git --git-dir=d:\\Temp\\gitTest\\Jibarr\\.git pull origin master", shell=True)
        print(ret)
    except subprocess.CalledProcessError:
        Logs.objects.create(log_type='Upgrade',log_category='System',log_message='Code upgrade error: ' + str(subprocess.STDOUT),log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
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