import shutil

def copyTheFile(source, dest, strPage, runSimulate):
    strPage += "COPY THE FILE - " + source + "----" + dest + "<br />"
    if runSimulate == False:
        shutil.copy2(source, dest)
    return strPage
    