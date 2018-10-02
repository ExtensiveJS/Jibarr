# this file uses only File/Folder to sync.
# all NEWER folders get synced
# all NEWER files get synced

import os
import copyTheFile
from datetime import datetime
def checkFolder(homeDir,destDir,startDateTime):
    #print("checkFolder subprocess")
    #print(homeDir)
    #print(destDir)
    #print(startDateTime)
    for x in os.listdir(homeDir):
        #print("Checking - " + homeDir + x)
        if os.path.isdir(homeDir + x):
            #print("FOLDER - " + x)
            if startDateTime < datetime.fromtimestamp(os.path.getmtime(os.path.join(homeDir + x))):
                if os.path.exists(destDir + x) == False:
                    #print("Dir does not exist - Creating")
                    os.makedirs(destDir + x)
                    #os.mkdir(destDir + x) 
                #else:
                    #print("Dir Exists")
            #homeDir = homeDir + x + "/"
            checkFolder(homeDir + x + "/",destDir + x + "/",startDateTime)
        elif os.path.isfile(homeDir + x):
            #print("FILE - " + x)
            if os.path.exists(destDir + x):
                #print("file exists")
                if datetime.fromtimestamp(os.path.getmtime(os.path.join(homeDir + x))) > datetime.fromtimestamp(os.path.getmtime(os.path.join(destDir + x))):
                    print("source is newer, copy it")
                    if os.path.exists(destDir) == False:
                        os.makedirs(destDir)
                    copyTheFile.copyTheFile(homeDir + x,destDir + x)
            elif startDateTime < datetime.fromtimestamp(os.path.getmtime(os.path.join(homeDir + x))):
                print("file not exist, lastRun < source mod date, copy it")
                if os.path.exists(destDir) == False:
                    os.makedirs(destDir)
                copyTheFile.copyTheFile(homeDir + x,destDir + x)
            #else:
                #copyTheFile.copyTheFile(homeDir + x,destDir + x)
        else:
            print("OTHER - " + x)
    #print("Folder Check Done - " + homeDir)