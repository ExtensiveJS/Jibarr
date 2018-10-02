import os, shutil
def copyTheFile(source,dest):
    print("COPY THE FILE - " + source + "----" + dest)
    shutil.copy2(source,dest)
    