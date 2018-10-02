print("processing started")
import os, time, checkFolder, sys, argparse, checkDB
from time import mktime
from datetime import datetime
#autoRun = True
useDB = False #temporary override as that function hasn't been built yet, just stubbed
parser = argparse.ArgumentParser()
parser.add_argument("-s","--srcDir", help="-s/--srcDir is the source folder to check.")
parser.add_argument("-d","--destDir", help="-d/--destDir is the destination folder to copy to.")
parser.add_argument("-l","--lastRun", help="-l/--lastRun is the date/time of the last run.")
args = parser.parse_args()
errMsg = ""
if args.srcDir is None:
    errMsg = "Error: -s/--srcDir cannot be empty. \n"
if args.destDir is None:
    errMsg += "Error: -d/--destDir cannot be empty."
if len(errMsg) > 0:
    print(errMsg)
else:
    if args.lastRun is None:
        args.lastRun = "Mar 29 1971 6:07PM"
    startDateTime = datetime.fromtimestamp(mktime(time.strptime(args.lastRun, "%b %d %Y %I:%M%p")))
    if useDB == True:
        checkDB.checkDB(args.srcDir,args.destDir,startDateTime)
    else:
        checkFolder.checkFolder(args.srcDir,args.destDir,startDateTime)
print("processing ended")
