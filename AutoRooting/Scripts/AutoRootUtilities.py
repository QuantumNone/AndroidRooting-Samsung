


#This file will contain several shared utilities for use in the main classes, such as Main.py and Setup.py

import os, platform, ctypes, shutil, socket, urllib.request, zipfile

#Prompts the user (y/n)
def askUser(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False

class UnsupportedPlatformError(Exception):
    pass

# getPlatform returns variables for supported platforms. 
# Windows systems will return 1, while Linux systems return 2. All other systems will error out.
def getPlatform() -> int: 
    if platform.system() == "Windows":
        return 1
    elif platform.system() == "Linux":
        return 2
    raise UnsupportedPlatformError("This Platform is not currently supported. Only Windows or Linux are supported. If you are on a Windows or Linux machine, please report this error.")

# isSetup returns true if setup has been run, or false otherwise. It's that simple.
def isSetup() -> bool:
    wd = os.getcwd() + "\\Tools\\config.cfg"
    if os.path.isfile(wd):
        return True
    else: 
        return False

# isElevated is the first program here that can actually fail to get a result. This exception is defined for that case.
class AdminStateUnknownError(Exception): 
    pass

# Checks if the script has Elevated Priviledges. On Linux, this means uid 0, while on wnidows we check if user is an admin.
def isElevated(): 
    try:
        return os.getuid() == 0
    except AttributeError:
        pass
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError:
        raise AdminStateUnknownError("Cannot determine whether the user is an admin.")

#returns the free disk space, in bytes
def getDiskSpace(): 
    total, used, free = shutil.disk_usage(os.getcwd())
    return free

#checks if dns exists and can ping a known good server
def isConnected() -> bool: 
    REMOTE_SERVER = "one.one.one.one"
    try: 
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception: 
        pass
    return False

#checks if whatever executable provided (as string) exists in $PATH
def checkTool(name): 
    return shutil.which(name) is not None

class DownloadFailedError(Exception):
    pass

#Downloads a file
def download(URLink: str, FileName: str):
    DestinationPath = os.getcwd()
    try:
        urllib.request.urlretrieve(URLink, DestinationPath + "\\Downloads\\" + FileName)
    except urllib.error.ContentTooShortError:
        if askUser("The download was interrupted, either because connection was lost or the connection was forcibly closed. Would you like to retry the download?"):
            download(URLink, FileName)
        else:
            raise DownloadFailedError("The Download failed for some reason. This Application cannot continue.")
    except:
        raise DownloadFailedError("The Download failed for some reason. This Application cannot continue.")



#Extracts a zip
def extractZip(zip_file: str, DestinationPath: str):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(DestinationPath)

#This checks for the existance of a file witin the AutoRooting directory, using relative paths. Inputs should be formatted so AutoRooting/Downloads/Dockerfile is input as Downloads/Dockerfile
def checkfile(filename: str):
    basepath = os.getcwd()+"\\"
    if os.path.isfile(basepath+filename):
        return True
    else:
        return False
