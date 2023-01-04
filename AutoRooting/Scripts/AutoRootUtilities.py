


#[AutoRootUtiilities.py] file will contain several functions, where mostly of them are required for the Setup.py and for Main.py files
import os, platform, ctypes, shutil, socket, urllib.request, zipfile


#Colors for String formatting :
Colors = {
    "Reset": '\033[0m',
    "Grey": '\033[1;30;48m',
    "Red": '\033[1;31;48m',
    "Green": '\033[1;32;48m',
    "Yellow": '\033[1;33;48m',
    "Blue": '\033[1;34;48m', 
    "Magenta": '\033[1;35;48m',
    "Cyan": '\033[1;36;48m',
    "White": '\033[1;37;48m'
}
#Usage Example : print(Colors["Red"] + 'Color that string' + Colors["Reset"])


#Prompts the user (y/n)
def askUser(question) -> bool:
    while "the answer is invalid":
        reply = str(input(question + Colors["Green"] + ' (Y/N) : ' + Colors["Reset"])).lower().strip()
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
    raise UnsupportedPlatformError(f"{Colors['Red']}Unsupported Platform! {Colors['Reset']}\nOnly Windows or Linux are supported.\nIf you are on a Windows or Linux machine, please report this error.")


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

#Checks if the script has Elevated Priviledges. On Linux, this means uid 0, while on wnidows we check if user is an admin.
def isElevated(): 
    try:
        return os.getuid() == 0
    except AttributeError:
        pass
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError:
        raise AdminStateUnknownError("Cannot determine whether the user is an admin!")


#Returns the free disk space, in bytes
def getDiskSpace(): 
    total, used, free = shutil.disk_usage(os.getcwd())
    return free


#Checks if dns exists and can ping a known good server
def isConnected() -> bool:
    print(f"\nRunning {Colors['Red']}Internet Connection Test{Colors['Reset']}...")
    
    print(f"{Colors['Red']}Connection Status{Colors['Reset']} : ", end='')
    REMOTE_SERVER = "one.one.one.one"
    try: 
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        s.close()
        print(f"{Colors['Green']}Online{Colors['Reset']}")
        return True
    except Exception: 
        pass

    print(f"{Colors['Green']}Offline{Colors['Reset']}")
    return False


#Checks if whatever executable provided (as string) exists in $PATH
def checkTool(name: str) -> bool: 
    return shutil.which(name) is not None



class DownloadFailedError(Exception):
    pass

TryAgainTimes = 0 #This lets the code know that the download has been re-started more than N times
def download(URLink: str, FileName: str): #Downloads a file
    DestinationPath = os.getcwd() + "\\Downloads\\" + FileName
    try:
        print(f"{Colors['Green']}\nDownloading{Colors['Reset']} {FileName} to {DestinationPath}")
        urllib.request.urlretrieve(URLink, DestinationPath)
        print(f"{Colors['Green']}\tDone!{Colors['Reset']}")

    except urllib.error.ContentTooShortError: #If the download has been interrupted for Connection Lost or the connection was Forcibly closed
        print(f"{Colors['Red']}Failed{Colors['Reset']} to download {FileName}...")
        
        if not isConnected():
            print("\t[Please make sure you are connected to Internet!]")
            Ok_IAmConnected = input("Press 'Enter' key if you are connected to Internet : ") #This input is like a delay : when the user is correctly connected to internet then the program will continue
            download(URLink, FileName)

        elif isConnected(): #If the connection is stable then the connection was Forcibly closed by AntiVirus or an other process.
            print("\t[The download process has been stopped from an unknown source!]")
            
            if askUser(f"\Dooo you want try again to download {FileName} ? "):
                TryAgainTimes += 1
                if TryAgainTimes == 2:
                    raise DownloadFailedError(Colors["Red"] + f"[The file {FileName} has failed to be downloaded too many times...]" + Colors["Reset"])

                download(URLink, FileName)
            else:
                raise DownloadFailedError("The user stopped the download process")
    except:
        raise DownloadFailedError(f"The {FileName} failed to be downloaded for some reason.\nThe application cannot continue!")

    
    TryAgainTimes = 0



#Extracts a zip
def extractZip(Zip_FileName: str, DestinationPath: str):
    print(f"{Colors['Green']}Extracting{Colors['Reset']} {Zip_FileName} to {DestinationPath}", end = '')

    with zipfile.ZipFile(Zip_FileName, 'r') as zip_ref:
        zip_ref.extractall(DestinationPath)
    print(f"{Colors['Green']}\tDone!{Colors['Reset']}")


#This checks for the existance of a file within the AutoRooting directory, using relative paths. 
#Inputs should be formatted so AutoRooting/Downloads/Dockerfile is input as Downloads/Dockerfile
def checkfile(filename: str):
    basepath = os.getcwd() + "\\"
    if os.path.isfile(basepath + filename):
        return True
    else:
        return False
