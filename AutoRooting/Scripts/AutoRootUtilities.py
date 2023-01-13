# [AutoRootUtiilities.py] file will contain several functions, where mostly of them are required for the Setup.py and for Main.py files
import os, platform, ctypes, shutil, socket, urllib.request, zipfile, subprocess, requests, sys
from time import sleep
sleepDelay = 2

# Colors for String formatting :
Colors: dict[str, str] = {
    "Reset": "\033[0m",
    "Grey": "\033[1;30m",
    "Red": "\033[1;31m",
    "Green": "\033[1;32m",
    "Green_Highlight": "\033[1;42m",
    "Yellow": "\033[1;33m",
    "Blue": "\033[1;34m",
    "Magenta": "\033[1;35m",
    "Cyan": "\033[1;36m",
    "White": "\033[1;37m",
}
# Usage Example : print(Colors["Red"] + 'Color that string' + Colors["Reset"])


OSDriveLetter = str(subprocess.check_output(f'echo %USERPROFILE%', stderr=subprocess.STDOUT, shell = True))[2:4] + '\\'

try:
    os.mkdir("Tools")
except FileExistsError:
    pass
try:
    os.mkdir("Downloads")
except FileExistsError:
    pass



# Prompts the user (y/n)
def askUser(question: str) -> bool:
    while "the answer is invalid":
        reply = (
            str(input(question + Colors["Green"] + "  (Y/N) : " + Colors["Reset"]))
            .lower()
            .strip()
        )
        if reply[:1] == "y":
            return True
        if reply[:1] == "n":
            return False


class UnsupportedPlatformError(Exception):
    pass


# getPlatform returns variables for supported platforms.
def getPlatform() -> str:
    if platform.system() in ["Windows", "Darwin", "Linux"]:
        return platform.system()
    raise UnsupportedPlatformError(
        f"{Colors['Red']}Unsupported Platform! {Colors['Reset']}\nOnly Windows or Linux are supported.\nIf you are on a Windows or Linux machine, please report this error."
    )


def CheckFile(Filename: str, Directory = os.getcwd() + '\\'):
    return os.path.isfile(Directory + Filename)

# Checks if whatever executable provided (as string) exists in $PATH
def checkTool(name: str) -> bool:
    return shutil.which(name) is not None


# isSetup returns true if setup has been run, or false otherwise. It's that simple.
def isSetup() -> bool:
    wd = os.getcwd() + "\\Tools\\config.cfg"
    return os.path.isfile(wd)


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
        print("Cannot determinate if program has been executed as Administrator Rights!")
        input(f"Press {Colors['Red']}ENTER{Colors['Reset']} to exit : ")
        raise AdminStateUnknownError()


# Returns the free disk space, in bytes
def getDiskSpace() -> int:
    total, used, free = shutil.disk_usage(os.getcwd())
    return free


# Checks if dns exists and can ping a known good server
def isConnected() -> bool:
    print('Running Connection Test...')
    print('Connection Status : ', end = '')
    REMOTE_SERVER = "one.one.one.one"
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        s.close()
        print(f'\t\t[{Colors["Green"]}Online!{Colors["Reset"]}]')
        return True
    except Exception:
        pass
    
    print(f'\t\t[{Colors["Red"]}Offline!{Colors["Reset"]}]')
    return False

#This function should be needed
def AddToEnvironmentPath(Directory):
    print(
    f'{Colors["Green"]}Adding{Colors["Reset"]} {Directory} to the {Colors["Green"]}User Environment{Colors["Reset"]} Path...'
    )
    os.system(f'setx PATH = "{Directory};%PATH%"')




# Checks if whatever executable provided (as string) exists in $PATH
def checkTool(name: str) -> bool:
    return shutil.which(name) is not None


def DriverInstaller():
    """Installs a requested driver"""
    print('Disabling Windows Driver Signature Verification... ')
    # os.system('bcdedit /set testsigning on')



class DownloadFailedError(Exception):
    pass


TryAgainTimes = (
    0  # This lets the code know that the download has been re-started more than N times
)


def Download(URLink: str, FileName: str):  # Downloads a file
    DestinationPath = os.getcwd() + "\\Downloads\\" + FileName
    try:
        print(
            f"{Colors['Green']}\nDownloading{Colors['Reset']} {FileName} to {DestinationPath}",
            end = ''
        )
        urllib.request.urlretrieve(URLink, DestinationPath)
        print(f"      [{Colors['Green']}Done{Colors['Reset']}!]")

    except urllib.error.ContentTooShortError:  # If the download has been interrupted for Connection Lost or the connection was Forcibly closed
        print(f"{Colors['Red']}Failed{Colors['Reset']} to download {FileName}...")

        if not isConnected():
            print("\t[Please make sure you are connected to Internet!]")
            input(
                f"Press {Colors['Red']}ENTER{Colors['Reset']} key if you are connected to Internet : "
            )  # This input is like a delay : when the user is correctly connected to internet then the program will continue
            Download(URLink, FileName)

        elif (
            isConnected()
        ):  # If the connection is stable then the connection was Forcibly closed by AntiVirus or an other process.
            print("\t[The download process has been stopped from an unknown source!]")

            if askUser("Would you like to retry?"):
                TryAgainTimes += 1
                if TryAgainTimes == 2:
                    raise DownloadFailedError(
                        Colors["Red"]
                        + f"[The download has failed too many times. Exiting.]"
                        + Colors["Reset"]
                    )

                Download(URLink, FileName)
            else:
                print("The user stopped the download process - Execution cannot continue.")
                input(f"Press {Colors['Red']}ENTER{Colors['Reset']} to exit : ")
                raise DownloadFailedError()
    except:
        print(
            f"""{FileName} failed to be downloaded for some reason.
            The application cannot continue."""
            )
        raise DownloadFailedError()

    TryAgainTimes = 0

def Pip_Installer(Package: str, Package_Name: str):
    try:
        if not checkTool(Package_Name):
            #sys.executable returns python version
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', Package])
        else:
            print(f'{Package_Name} already exists!')
    except Exception as ex:
        print(f'An {Colors["Red"]}unknown error{Colors["Reset"]} came out while trying to download {Package_Name} : {Package}')
        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
        raise ex()



# Extracts a zip
def ExtractZip(Zip_FileName: str, DestinationPath: str):
    print(
        f"{Colors['Green']}Extracting{Colors['Reset']} {Zip_FileName} to {DestinationPath}",
        end = "",
    )

    with zipfile.ZipFile(Zip_FileName, "r") as zip_ref:
        zip_ref.extractall(DestinationPath)

    print(f"      [{Colors['Green']}Done!{Colors['Reset']}]")




# The user has to follow these steps in order to be able to use Adb
def SetupDeviceForUSBCommunication():
    """User has to MANUALLY setup his device to start USB communication"""

    def DelayedPrint(string: str, sleepDelay: float) -> None:
        for line in string.split('\n'):
            print(line)
            sleep(sleepDelay)

    instructions = f'''

    1. Open your device {Colors["Green"]}settings{Colors["Reset"]} and navigate into "About my phone" option.
    2. Search for "{Colors["Red"]}Build number{Colors["Reset"]}" option inside these settings (if you cannot find it try in "{Colors["Green"]}Software Information{Colors["Reset"]}" option).
    3. Tap 7 times on "Build number" option to enable {Colors["Red"]}Developer Options{Colors["Reset"]}.
    4. Go back to settings and {Colors["Red"]}search{Colors["Reset"]} for Developer Options.
    5. Search for "{Colors["Red"]}USB debugging{Colors["Reset"]}" option and {Colors["Green"]}enable{Colors["Reset"]} it.
    6. {Colors["Green"]}Connect{Colors["Reset"]} now your device to your computer trough USB cable and check your device screen.
    7. {Colors["Green"]}Allow{Colors["Reset"]} the pop-up asking for computer permissions.
    8. Now search inside Developer Options for "{Colors["Red"]}Select USB configuration{Colors["Reset"]}".
    9. Click it and select "{Colors["Green"]}MTP File transfer{Colors["Reset"]}" protocol.'''

    DelayedPrint(instructions, sleepDelay)

    input(f'\n\t=> Press {Colors["Green"]}Enter{Colors["Reset"]} key to continue : ')

    print(f'\n    10. Now search for "{Colors["Red"]}OEM Unlocking{Colors["Reset"]}" option in Developer options and {Colors["Green"]}ENABLE{Colors["Reset"]} it!')
    print(
        f'''
        {Colors["Red"]}IF{Colors["Reset"]} YOU CANNOT FIND THAT OPTION THEN LOOK AT THESE DOCUMENTATION :
        \t1. "{Colors["Blue"]}https://krispitech.com/fix-the-missing-oem-unlock-in-developer-options/{Colors["Reset"]}"
        \t2. "{Colors["Blue"]}https://www.quora.com/Why-do-some-mobile-companies-refuse-to-unlock-bootloaders-like-Huawei-and-Realme{Colors["Reset"]}"
        '''
        )

    input(f'\n\t=> Press {Colors["Green"]}Enter{Colors["Reset"]} key to continue : ')
    print()





def Install_AdbFastboot():
    Download(
        URLink = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip",
        FileName = "platform-tools.zip"
    )

    ExtractZip(
        Zip_FileName = "platform-tools.zip",
        DestinationPath = "Tools"
    )
    print(
        f"{Colors['Red']}Removing{Colors['Reset']} platform-tools.zip",
        end = ''
    )
    os.remove('Downloads\\plattools.zip')

    print(f'      [{Colors["Green"]}Done{Colors["Green"]}!]')

    AddToEnvironmentPath(f'{os.getcwd()}\\Tools')


def Check_AdbConnection() -> bool:
    try:
        AdbDevices_output = subprocess.check_output("adb devices", stderr = subprocess.STDOUT, shell = True).strip()
        return AdbDevices_output[-6:] == b'device'

    except subprocess.CalledProcessError:
        print(
            f'''
            {Colors["Red"]}Cannot determinate{Colors["Reset"]} USB Connection!
            This could be because Adb&Fastboot or USB Drivers are not correctly installed...'''
            )
        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
        raise SystemExit()
    
def Check_FastbootConnection() -> bool:
    try:
        FastbootDevices_output = subprocess.check_output("fastboot devices", stderr = subprocess.STDOUT, shell = True).strip()
        return FastbootDevices_output[-6:] == b'device'
        
    except subprocess.CalledProcessError:
        print(
            f'''
            {Colors["Red"]}Cannot determinate{Colors["Reset"]} USB Connection!
            This could be because Adb&Fastboot or USB Drivers are not correctly installed...'''
            )
        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
        raise SystemExit()


def Install_GoogleUSBDriver():  #Required for all devices that use Fastboot Mode
    pass

def Install_MTKDriver():    #Chinese phones
    pass

def Download_Magisk():

    try: #Just check for latest versions of Magisk  --SOME DEVICES NEED CUSTOM MAGISK VERSION!
        response = requests.get('https://api.github.com/repos/topjohnwu/Magisk/releases?per_page=1').json()[0]
        html_url = response["html_url"]
        version = html_url.split("/")[-1]
        filename = f"Magisk-{version}.apk"

        Download(
            URLink = f"https://github.com/topjohnwu/Magisk/releases/download/{version}/{filename}",
            FileName = "Magisk.apk"
        )

    except: #Shouldn't be a problem if somehow the api doesn't work, magisk will be donloaded on V25.2
        print(
            f'''{Colors["Red"]}Failed{Colors["Reset"]} to download the latest version of Magisk!
            Downloading {Colors["Green"]}Magisk V25.2{Colors["Reset"]}...'''
        )
        Download(
            URLink = f"https://github.com/topjohnwu/Magisk/releases/download/v25.2/Magisk-v25.2.apk",
            FileName = "Magisk.apk"
        )


#Other functions for other devices...

def Samsung_Requirements(Phone):
    def Install_SamsungUSBDrivers(InstallationStatus: bool):
        Download(
            URLink = "https://developer.samsung.com/sdp/file/2ad30860-0932-44e3-bf63-765a5cfa1010",
            FileName = "SamsungUSB-installer.exe"
        )

        #Let's not reboot the computer and try to check if the USB Communication works, if not then the pc will require reboot (Or Windows Driver signature offline)
        print(
            f'Please, follow the instructions that the installer shows!'
        )
        os.startfile(f'{os.getcwd()}\\Downloads\\SamsungUSB-installer.exe')
        print('Installation Completed!')

        #HAVE TO WORK ON THAT
        if not InstallationStatus: #This can be converted into a function like : checkAdbConnection() (If not connected, check USB drivers) 
            print(
                f'''
                The USB communication cannot be enstablished!
                Try to reboot your computer or try to {Colors["Red"]}disable{Colors["Reset"]} Windows Driver Signature Verification : 
                \t[{Colors["Blue"]}https://answers.microsoft.com/en-us/windows/forum/all/permanent-disable-driver-signature-verification/009c3498-bef8-4564-bb52-1d05812506e0{Colors["Reset"]}]'''
            )

    def Download_Firmware():
        def Download_Status(Status: str):
            path = os.getcwd() + "\\Downloads\\"
            versions = str(subprocess.check_output(f'samloader -m GT-I8190N -r XME checkupdate', stderr = subprocess.STDOUT, shell = True), encoding = 'utf-8')[:-2]
            if Status == 'New Download':
                try:
                    os.system(f'samloader --dev-model {Phone.Model} --dev-region {Phone.Region} download --fw-ver {versions} --do-decrypt --out-dir {path}')
                except ConnectionAbortedError:
                    print(f'Your {Colors["Red"]}internet connection{Colors["Reset"]} has been stopped or aborted!\nPlease {Colors["Green"]}check{Colors["Reset"]} your internet connection!')
                    input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to confirm if your internet connection works : ")
                    if isConnected():
                        Download_Status(Status = 'Resume Downlad') 
                    else:
                        raise SystemExit()
                
                except Exception as ex:
                    print(f'Cannot start or continue {Phone.Model} firmware\'s download for an unknown error!')
                    input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
                    raise SystemExit()

            elif Status == 'Resume Download':
                print(f'{Colors["Green"]}Resuming{Colors["Reset"]} the download...')
                try:
                    os.system(f'samloader --dev-model GT-I8190N --dev-region XME download --resume --fw-ver {versions} --do-decrypt --out-dir {path}')

                except ConnectionAbortedError:
                    print(f'Your internet connection has been stopped or aborted!\nPlease check your internet connection!')
                    input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to confirm if your internet connection works : ")
                    if isConnected():
                        Download_Status(Status = 'Resume Downlad') 
                    else:
                        raise SystemExit()

                except Exception as ex:
                    print('Cannot start or continue {Phone.Model} firmware\'s download for an unknown error!')
                    input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
                    raise SystemExit()

        
        print(f'''
                    [Firmware Downloader] by (@Samloader)
        ''')
        Pip_Installer(Package = 'git+https://github.com/samloader/samloader.git', Package_Name = 'samloader')

        print(f'Your device ({Phone.Model}) is currently running on Android V{Phone.AndroidVersion} and {Phone.PDA} version.\t[Region : {Phone.Region}]\n')
        Download_Status('New Download')


    def Unlock_Bootloader():
        print(f'''\n
        [{Colors["Red"]}Bootloader unlock{Colors["Reset"]} Step]\t[{Colors["Green"]}Advance Download Mode{Colors["Reset"]}]
        \t\t[{Colors["Red"]}All phone data will be erased{Colors["Reset"]}!]
        1. {Colors["Red"]}Unplug{Colors["Reset"]} phone cable from pc and {Colors["Red"]}power off{Colors["Reset"]} your phone.
        2. Press and hold {Colors["Red"]}volume up{Colors["Reset"]} and {Colors["Red"]}volume down{Colors["Reset"]} buttons {Colors["Green"]}and{Colors["Reset"]} (while holding) connect the USB cable to the computer.
        \t[{Colors["Red"]}IF{Colors["Reset"]} your phone has {Colors["Red"]}BIXBI button{Colors["Reset"]} then press and hold it too!]
        3. You can release buttons once a {Colors["Blue"]}blue screen{Colors["Reset"]} appears.
        
        You should now see a screen like this :
            {Colors["Green_Highlight"]}A custom OS can cause critical problems{Colors["Reset"]} 
            {Colors["Green_Highlight"]}in phone and installed applications.{Colors["Reset"]} 
        
            {Colors["Green_Highlight"]}if you want to download a custom OS,{Colors["Reset"]} 
            {Colors["Green_Highlight"]}press the volume up key.{Colors["Reset"]} 
            {Colors["Green_Highlight"]}Otherwise, press the volume down key to cancel.{Colors["Reset"]} 

            \b\b---------------------------------------------------

            {Colors["Green_Highlight"]}Volume up: Continue{Colors["Reset"]} 
            {Colors["Green_Highlight"]}Volume up long press: Device unlock mode{Colors["Reset"]} 
            {Colors["Green_Highlight"]}Volume down: Cancel (restart phone){Colors["Reset"]} 

        4. Press and hold volume up button until see {Colors["Red"]}bootloader unlock menu{Colors["Reset"]}.
        5. Press again the volume up button to {Colors["Green"]}confirm{Colors["Reset"]} the bootloader unlock process.

        The phone will now reboot.
        ''')
        
        input(f'Press {Colors["Green"]}ENTER{Colors["Reset"]} {Colors["Red"]}if{Colors["Reset"]} the phone has been rebooted : ')

        print(f'''
        Your phone has now been rebooted into {Colors["Blue"]}Welcome Screen{Colors["Reset"]}.
        Configure all you need to finish the Welcome Screen's setup.     [You can also skip this configuration, just click on "Next"]
        Open your system settings and {Colors["Red"]}configure{Colors["Reset"]} WI-FI network.      [{Colors["Red"]}Important{Colors["Reset"]}!]

        Once done enable again developer options.
        ''')
        if askUser('Need help on how to enable Developer options?'):
            SetupDeviceForUSBCommunication()
        
        if askUser('Is "OEM Unlocking" option "greyed out"?'):
                print(f'[{Colors["Red"]}Great{Colors["Reset"]}!]\nYour phone\'s bootloader has been {Colors["Green"]}unlocked correctly{Colors["Reset"]}!') 
        else:
            print("This means your phone's bootloader hasn't been unlocked correctly!")
            if askUser('Wanna continue anyway?'):
                print(f"[{Colors['Green']}Ok!{Colors['Reset']}]")
            else:
                input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
                raise SystemExit()


    print(
        f'{Colors["Green"]}Installing{Colors["Reset"]} Samsung requirements...'
    )

    Install_AdbFastboot()
    Download_Magisk()

    #TODO: Create a Firmware donload function and give the user 2 options : update to latest firmware (Need to flash it before patching) or run on current firmware (need PDA and CSS codes)
