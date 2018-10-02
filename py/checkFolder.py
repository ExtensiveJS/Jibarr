import os
import copyTheFile
from datetime import datetime
def checkFolder(homeDir,destDir,startDateTime):
    #print("checkFolder subprocess")
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
            if startDateTime < datetime.fromtimestamp(os.path.getmtime(os.path.join(homeDir + x))):
                if os.path.exists(destDir) == False:
                    os.makedirs(destDir)
                #copyTheFile.copyTheFile(homeDir + x,destDir + x)
            # if file exists, if source > dest
            elif os.path.exists(destDir + x):
                if datetime.fromtimestamp(os.path.getmtime(os.path.join(homeDir + x))) > datetime.fromtimestamp(os.path.getmtime(os.path.join(destDir + x))):
                    if os.path.exists(destDir) == False:
                        os.makedirs(destDir)
            else:
                copyTheFile.copyTheFile(homeDir + x,destDir + x)
        else:
            print("OTHER - " + x)
    #print("Folder Check Done - " + homeDir)