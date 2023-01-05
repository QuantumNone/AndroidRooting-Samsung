# [AutoRootUtiilities.py] file will contain several functions, where mostly of them are required for the Setup.py and for Main.py files
import os, platform, ctypes, shutil, socket, urllib.request, zipfile
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
    if platform.system() == "Windows":
        return "Windows"
    elif platform.system() == "Linux":
        return "Linux"
    raise UnsupportedPlatformError(
        f"{Colors['Red']}Unsupported Platform! {Colors['Reset']}\nOnly Windows or Linux are supported.\nIf you are on a Windows or Linux machine, please report this error."
    )


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
        raise AdminStateUnknownError("Cannot determine whether the user is an admin!")


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
    os.system(f'setx PATH = "{Directory};%PATH%"')


# Checks if whatever executable provided (as string) exists in $PATH
def checkTool(name: str) -> bool:
    return shutil.which(name) is not None


class DownloadFailedError(Exception):
    pass


TryAgainTimes = (
    0  # This lets the code know that the download has been re-started more than N times
)


def download(URLink: str, FileName: str):  # Downloads a file
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
            Ok_IAmConnected = input(
                "Press 'Enter' key if you are connected to Internet : "
            )  # This input is like a delay : when the user is correctly connected to internet then the program will continue
            download(URLink, FileName)

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

                download(URLink, FileName)
            else:
                raise DownloadFailedError(
                    "The user stopped the download process - Execution cannot continue."
                )
    except:
        raise DownloadFailedError(
            f"{FileName} failed to be downloaded for some reason.\nThe application cannot continue."
        )

    TryAgainTimes = 0


# Extracts a zip
def extractZip(Zip_FileName: str, DestinationPath: str):
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
