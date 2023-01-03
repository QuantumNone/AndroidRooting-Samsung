#This file will contain several shared utilities for use in the main classes, such as Main.py and Setup.py

import os, platform, ctypes, shutil, socket

# getPlatform returns variables for supported platforms. 
# Windows systems will return 1, while Linux systems return 2. All other systems will return 0.
def getPlatform(): 
    if platform.system() == "Windows":
        return 1
    elif platform.system() == "Linux":
        return 2
    else:
        return 0

# isSetup returns true if setup has been run, or false otherwise. It's that simple.
def isSetup():
    wd = os.getcwd() + "\\Tools"
    if os.path.isfile(wd):
        return True
    else: 
        return False

class AdminStateUnknownError(Exception): #Is Elevated is the first program here that can actually fail to get a result. This exception is defined for that case.
    """Cannot determine whether the user is an admin."""
    pass

def isElevated(): #Checks if the script has Elevated Priviledges. On Linux, this means uid 0, while on wnidows we check if user is an admin.
    try:
        return os.getuid() == 0
    except AttributeError:
        pass
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError:
        raise AdminStateUnknownError

def getDiskSpace(): #returns the free disk space, in bytes
    total, used, free = shutil.disk_usage(os.getcwd())
    return free

def isConnected(): #checks if dns exists and can ping a known good server
    REMOTE_SERVER = "one.one.one.one"
    try: 
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception: 
        pass
    return False

def checkTool(name): #checks if whatever executable provided (as string) exists in $PATH
    return shutil.which(name) is not None