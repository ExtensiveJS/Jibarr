import os
import copyTheFile
def checkFolder(homeDir,destDir):
    print("checkFolder subprocess")
    for x in os.listdir(homeDir):
        print("Checking - " + x)
        if os.path.isdir(homeDir + x):
            print("FOLDER - " + x)
            if os.path.exists(destDir + x) == False:
                print("Dir does not exist - Creating")
                os.mkdir(destDir + x) 
            checkFolder(homeDir + x + "/",destDir + x + "/")
        elif os.path.isfile(homeDir + x):
            print("FILE - " + x)
            copyTheFile.copyTheFile(homeDir + x,destDir + x)
        else:
            print("OTHER - " + x)
    print("Folder Check Done - " + homeDir)