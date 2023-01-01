
#Modules to download with pip :
import subprocess
import os
from ctypes import windll           #Need to check admin rights
from sys import exit
from time import sleep
import devcon_win                   #For Drivers Managment
from pyautogui import keyDown, press, keyUp     #For Keyboard Keys input (Needed for get custom terminal)

from Download_and_Extract import Download_and_Extract





#Global Variables
DelayTime = 500
OSDriveLetter = str(subprocess.check_output(f'echo %USERPROFILE%', stderr=subprocess.STDOUT, shell = True))[2:4] + '\\'




#Functions
def SetupTerminalGUIAndCheckPCRequirements():

    def CheckAdminRights():
        """Return True if user has admin privileges.

        Raises:
            AdminStateUnknownError if user privileges cannot be determined.
        """
        try:
            return os.getuid() == 0
        except AttributeError:
            pass
        try:
            return windll.shell32.IsUserAnAdmin() == 1
        except AttributeError:
            print('Cannot determinate if program has been executed as Administrator Rights!')
            print('Quitting...')
            exit()

    os.system('@echo off')
    subprocess.call('color A', shell=True)
    subprocess.call('cls', shell=True)

    #Edit Terminal Opacity...
    # Holds down keys
    keyDown("ctrl")
    keyDown("shift")
    # Presses "-" key once
    press("-")
    # Release keys
    keyUp("ctrl")
    keyUp("shift")

    #Check if program is running with Admin Privileges :
    os.system('cls')
    if CheckAdminRights() == False:
        print('Program hasn\'t been executed as Administrator Rights!')
        print('Quitting...')
        exit()

    #Check Computer Requirements : Windows 10 and x64 Base      --> For DevCon.exe
    os.system('cls')
    ComputerRequirements = True if "10" in str(subprocess.check_output('systeminfo | find "OS Version"', stderr=subprocess.STDOUT, shell=True)).split(':')[1] and "x64" in str(subprocess.check_output('systeminfo | find "System Type"', stderr=subprocess.STDOUT, shell=True)).split(':')[1] else print('\n\nYour computer platform is not supported!\nRequired Windows 10 x64 based PC!\n\nQuitting...') and sleep(6) and exit()


def GetPhoneInformations():
    PhoneInformations = {
        'Model': 'ro.product.model',
        'Build Number': 'ro.build.display.id',
        'Android Version': 'ro.build.version.release',
        'PDA': 'ro.build.PDA'
    }
    subprocess.call('cls', shell=True)

    for Info in PhoneInformations:
        try:
                                                                                                                                                #Need to format this : b'[ro.build.display.id]: [KTU84P.J100HXCS0AQC2]\r\r\n'   to  "KTU84P.J100HXCS0AQC2"
            PhoneInformations[Info] = str(subprocess.check_output(f'adb shell getprop | find "{PhoneInformations[Info]}"', stderr=subprocess.STDOUT, shell = True)).split(': ')[1].split(']')[0][1:]
            print(f'Got device {Info} : {PhoneInformations[Info]}')
        except:
            print(f'Could not get device {Info} information!')
            PhoneInformations[Info] = False
    return PhoneInformations
    

def SetupDeviceForUSBCommunication():
    """User has to MANUALLY setup his device to start USB communication"""
    print('Open your device settings and navigate into "About my phone" option')
    sleep(DelayTime)
    print('Tap 7 times on "Build number" option to enable Developer Options')
    sleep(DelayTime)
    print('Go back to settings and search for Developer Options')
    sleep(DelayTime)
    print('Search for "USB debugging" option and enable it')
    sleep(DelayTime)
    print('Connect now your device to your computer and check your device screen')
    sleep(DelayTime)
    print('Allow the pop-up asking for computer permissions')
    sleep(DelayTime)
    print('Now search inside Developer Options for "Select USB configuration"')
    sleep(DelayTime)
    print('Click it to select "MTP File transfer" protocol')
    sleep(DelayTime)
    Continue = input('\n\t$ Press Enter key to continue : ')
    print('\Now search for "OEM Unlocking" option in Developer options and ENABLE it!')
    sleep(DelayTime)
    print('\n\tIF YOU CANNOT FIND THAT OPTION THEN LOOK AT THIS DOCUMENTATION : \n\t\thttps://krispitech.com/fix-the-missing-oem-unlock-in-developer-options/ \n\t\t\tOR\n\t\thttps://www.quora.com/Why-do-some-mobile-companies-refuse-to-unlock-bootloaders-like-Huawei-and-Realme')
    sleep(DelayTime)
    Continue = input('\n\t$ Press Enter key to continue : ')


def AddToEnvironmentPath(Directory):
    os.system(f'setx PATH = "{Directory};%PATH%"')

def DriverInstaller():
    """Installs a requested driver"""


def Uninstaller():
    """Removes any Pre-Installed Tools-Files"""
    os.system('cls')
    print('Deleting Unused Files...\n')

    #ADB&Fastboot
    print('Deleting ADB&Fastboot Files...')
    os.system('del %USERPROFILE%\\Downloads\\platform-tools-latest-windows.zip')
    os.system('del %USERPROFILE%\\Downloads\\platform-tools-latest-windows')
    os.system('del %USERPROFILE%\\Downloads\\platform-tools')
    os.system(f'del {OSDriveLetter}\\platform-tools')

    #GoogleUSBDrivers
    print('Deleting GoogleUSBDrivers Files...')
    os.system('del %USERPROFILE%\\Downloads\\usb_driver_r13-windows.zip')
    os.system('del %USERPROFILE%\\Downloads\\usb_driver_r13-windows')
    os.system('del %USERPROFILE%\\Downloads\\usb_driver')


#HOW THE PROGRAM WORKS :
#Firstly it checks all requirements before starting. [Internet, HWID, Windows 10 x64, Setup Terminal GUI]
#Removes any Pre-Installed Tools-Files



#--------------PROGRAM STARTS HERE-------------------
#RUN THE PROGRAM WITH ADMINISTRATOR RIGHTS
SetupTerminalGUIAndCheckPCRequirements()

#WELCOME SCREEN
os.system('cls')
print('\nWelcome...Other stuff to drop here for introduction....')
os.system('pause > nul')

Uninstaller()

#START GETTING DEVICE INFORMATIONS
SetupDeviceForUSBCommunication()


#SETUP REQUIRED TOOLS

os.system('cls')
print('\nDownloading Tools for USB comunication...\n')
#Download ADB&Fastboot tools
Download_and_Extract("https://dl.google.com/android/repository/platform-tools-latest-windows.zip", f"{OSDriveLetter}")
#Add ADB%Fastboot directory to Windnows User Environment PATH
AddToEnvironmentPath(f"{OSDriveLetter}platform-tools")

#Install ADB&Fastboot USB drivers   [Google USB drivers]
Download_and_Extract("https://dl.google.com/android/repository/usb_driver_r13-windows.zip")


#Move DevCon.exe to C:\platform-tools
path = os.getcwd()
os.system(f'copy {path}\DevCon C:\platform-tools')


#After ADB&Fastboot tool has been installed, we proceed on getting device informations
os.system('cls')
SetupDeviceForUSBCommunication()
os.system('cls')
PhoneInformations = GetPhoneInformations()



#CREATING A CLASS TO MANAGE BETTER WITH DEVICE INFORMATIONS AND ACTIONS
class Phone:
    def __init__(self):
        self.Model = PhoneInformations['Model']
        self.BuildNumber = PhoneInformations['Build Number']
        self.AndroidVersion = PhoneInformations['Android Version']
        self.PDA = PhoneInformations['PDA']

device = Phone(PhoneInformations)

print(device.ModelName)
print(device.PhoneInformations['Model Name'])
