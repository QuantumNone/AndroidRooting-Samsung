# [AutoRootUtiilities.py] file will contain several functions, where mostly of them are required for the Setup.py and for Main.py files
import os, platform, ctypes, shutil, socket, urllib.request, zipfile, subprocess, requests
from time import sleep
sleepDelay = 2

# Colors for String formatting :
Colors = {
    "Reset": "\033[0m",
    "Grey": "\033[1;30m",
    "Red": "\033[1;31m",
    "Green": "\033[1;32m",
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
def askUser(question) -> bool:
    while "the answer is invalid":
        reply = (
            str(input(question + Colors["Green"] + " (Y/N) : " + Colors["Reset"]))
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
    REMOTE_SERVER = "one.one.one.one"
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception:
        pass
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
            f"{Colors['Green']}\nDownloading{Colors['Reset']} {FileName} to {DestinationPath}"
        )
        urllib.request.urlretrieve(URLink, DestinationPath)
        print(f"{Colors['Green']}\tDone!{Colors['Reset']}")

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


# Extracts a zip
def ExtractZip(Zip_FileName: str, DestinationPath: str):
    print(
        f"{Colors['Green']}Extracting{Colors['Reset']} {Zip_FileName} to {DestinationPath}",
        end = "",
    )

    with zipfile.ZipFile(Zip_FileName, "r") as zip_ref:
        zip_ref.extractall(DestinationPath)

    print(f"{Colors['Green']}\tDone!{Colors['Reset']}")


# This checks for the existance of a file within the AutoRooting directory, using relative paths.
# Inputs should be formatted so AutoRooting/Downloads/Dockerfile is input as Downloads/Dockerfile
def checkfile(filename: str):
    basepath = os.getcwd() + "\\"
    if os.path.isfile(basepath + filename):
        return True
    else:
        return False



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

    print(f'\t{Colors["Green"]}Done{Colors["Green"]}!')

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

        print(f"")


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

def Samsung_Requirements():
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

    def Download_Firmware(DEV_MODEL: str, DEV_REGION: str):
        pass

    print(
        f'{Colors["Green"]}Installing{Colors["Reset"]} Samsung requirements...'
    )

    Install_AdbFastboot()
    Download_Magisk()

    #TODO: Create a Firmware donload function and give the user 2 options : update to latest firmware (Need to flash it before patching) or run on current firmware (need PDA and CSS codes)
