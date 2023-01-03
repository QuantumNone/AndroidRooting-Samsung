#This file will contain several shared utilities for use in the main classes, such as Main.py and Setup.py

import os
import platform


def getPlatform(): #getPlatform returns variables for supported platforms. Windows systems will return 1, while Linux systems return 2. All other systems will return 0.
    if platform.system() == "Windows":
        return 1
    elif platform.system() == "Linux":
        return 2
    else:
        return 0

def isSetup():
    wd = os.getcwd()
    wd = wd+"\\Tools"
    if os.file.exists(wd):
        return True
    else: 
        return False

