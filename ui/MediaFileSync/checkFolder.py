# this file uses only File/Folder to sync.
# all NEWER folders get synced
# all NEWER files get synced

import os
from MediaFileSync.copyTheFile import copyTheFile
from datetime import datetime

def checkFolder(homeDir, destDir, startDateTime, strPage, runSimulate):
    strPage += "Running Folder Checks.<br />"
    for x in os.listdir(homeDir):
        strPage += "Checking - " + homeDir + x + "<br />"
        if os.path.isdir(homeDir + x):
            if startDateTime < datetime.fromtimestamp(os.path.getmtime(os.path.join(homeDir + x))):
                if os.path.exists(destDir + x) == False:
                    os.makedirs(destDir + x)
                else:
                    strPage += "Creating Folder - " + destDir + x + "<br />"
            checkFolder(homeDir + x + "/",destDir + x + "/", startDateTime, strPage, runSimulate)
        elif os.path.isfile(homeDir + x):
            if os.path.exists(destDir + x):
                if datetime.fromtimestamp(os.path.getmtime(os.path.join(homeDir + x))) > datetime.fromtimestamp(os.path.getmtime(os.path.join(destDir + x))):
                    print("source is newer, copy it")
                    if os.path.exists(destDir) == False:
                        os.makedirs(destDir)
                    else:
                        strPage += "Creating Folder - " + destDir + x + "<br />"
                    copyTheFile(homeDir + x,destDir + x, strPage, runSimulate)
            elif startDateTime < datetime.fromtimestamp(os.path.getmtime(os.path.join(homeDir + x))):
                if os.path.exists(destDir) == False:
                    os.makedirs(destDir)
                else:
                    strPage += "Creating Folder - " + destDir + x + "<br />"
                copyTheFile(homeDir + x,destDir + x, strPage, runSimulate)
        else:
            strPage += "OTHER FOUND - " + x + "<br />"
    return strPage