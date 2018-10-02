print("processing started")
import os, time, checkFolder, sys, argparse
from time import mktime
from datetime import datetime
#srcDir = "/videos/"
#lastRun = "Jan 9 2018 11:18PM"
#destDir = "/temp/"
#autoRun = True
parser = argparse.ArgumentParser()
parser.add_argument("-s","--srcDir", help="description of -s --srcDir")
parser.add_argument("-d","--destDir", help="description of -d --destDir")
parser.add_argument("-l","--lastRun", help="description of -l --lastRun")
args = parser.parse_args()
#print("-s " + args.srcDir)
#print("-d " + args.destDir)
#print("-l " + args.lastRun)
startDateTime = datetime.fromtimestamp(mktime(time.strptime(args.lastRun, "%b %d %Y %I:%M%p")))
checkFolder.checkFolder(args.srcDir,args.destDir,startDateTime)
# TODO - Update lastRun
print("processing ended")
