print("processing started")
import os, time
from time import mktime
from datetime import datetime
from shutil import copytree
homeDir = "d:/videos/"
lastRun = "Jan 21 2018 11:18PM"
destDir = "d:/temp/"
autoRun = True
startDateTime = datetime.fromtimestamp(mktime(time.strptime(lastRun, "%b %d %Y %I:%M%p")))
for x in os.listdir(homeDir):
    if startDateTime < datetime.fromtimestamp(os.path.getmtime(os.path.join(homeDir, x))):
        print(x, time.ctime(os.path.getmtime(os.path.join(homeDir, x))))
        
        # WORKS, not used copytree("d:/videos/Thor Ragnarok (2017)","d:/temp/Thor Ragnarok (2017)")
        # os.direxists(dest) - checks if the dir exists
        if os.path.exists("d:/videos/Thor Ragnarok (2017)") == False:
            print("dir does not exist")
            os.mkdir("d:/temp/Thor Ragnarok (2017)") # - dest is a single folder/path
        # os.mkdirs(dest) - dest can be a tree of dirs
print("processing ended")
