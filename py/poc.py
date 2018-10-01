print("processing started")
import os, time
import checkFolder
from time import mktime
from datetime import datetime
from shutil import copytree
homeDir = "/videos/"
lastRun = "Sep 21 2018 11:18PM"
destDir = "/temp/"
autoRun = True
startDateTime = datetime.fromtimestamp(mktime(time.strptime(lastRun, "%b %d %Y %I:%M%p")))
checkFolder.checkFolder(homeDir,destDir)
# Check each folder in the parent directory for a Last Mod date greater than the lastRun
#for x in os.listdir(homeDir):
#    #print("Checking - " + x)
#    if startDateTime < datetime.fromtimestamp(os.path.getmtime(os.path.join(homeDir, x))):
#        print("Update found - " + x, time.ctime(os.path.getmtime(os.path.join(homeDir, x))))
#        
#        # checks if the dir exists
#        if os.path.exists("/temp/" + x) == False:
#            print("Dir does not exist - Creating")
#            os.mkdir("/temp/" + x) # - dest is a single folder/path
#        else:
#            print("Dir exists - checking for updated contents")
#            for y in os.listdir(homeDir + x):
#                print("Checking - " + y)
#                if startDateTime < datetime.fromtimestamp(os.path.getmtime(os.path.join(homeDir + x + "/" + y))):
#                    print("Update Found - " + x + "/" + y)
#        # os.mkdirs(dest) - dest can be a tree of dirs
# TODO - Update lastRun
print("processing ended")
