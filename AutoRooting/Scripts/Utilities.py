#Copyright (C) <2023> by <Quantum>


# [AutoRootUtiilities.py] file will contain several functions, where mostly of them are required for the Setup.py and for Main.py files

import os, platform, ctypes, shutil, urllib.request, zipfile, subprocess, requests, sys, tarfile
from tqdm import tqdm

# Colors for String formatting :
Colors: dict[str, str] = {
    "Reset": "\033[0m",

    "Italic": "\033[1;3m",
    "Underline": "\033[1;4m",
    "Double_Underline": "\033[1;21m",
    "Strike_Trhough": "\033[1;9m",
    "Flash": "\033[1;5m",   #Only in Latest Terminals

    "White_Highlight": "\033[1;7m",
    "Black_Highlight": "\033[1;40m",
    "Red_Highlight": "\033[1;41m",
    "Grey_Highlight": "\033[1;47m",
    "Yellow_Highlight": "\033[1;43m",
    "Blue_Highlight": "\033[1;44m",
    "Magenta_Highlight": "\033[1;45m",
    "Cyan_Highlight": "\033[1;46m",

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

DownloadsFolder = os.getcwd() + '\\Downloads\\'
ToolsFolder = os.getcwd() + '\\Tools\\'
class function: #Used just by Type Hinting for understanding variable type
    pass

def Quit(ExceptionName: Exception, Message: str) -> Exception:
    print('\n' + Message)
    input(f"Press {Colors['Red']}ENTER{Colors['Reset']} to exit : ")
    raise ExceptionName

def find_files(root_dir: str, extension: str, file_name: str, NoExtension: bool = False) -> list[str]:
    #This is because some files (such as boot.img) are renamed with an other extension, for example lz4
    return [root_dir + f for f in os.listdir(root_dir) if (f.startswith(file_name) and (NoExtension or f.endswith(f'.{extension}')))]

def CheckFile(Filename: str, Directory = f'{os.getcwd()}\\') -> bool:
    return os.path.isfile(Directory + Filename)

# Checks if whatever executable provided (as string) exists in $PATH
def checkTool(name: str, path: str = '') -> bool:
    if path:
        return CheckFile(Filename=name, Directory=path)
    return shutil.which(name) is not None

def Pip_Installer(Package: str, Package_Name: str = '') -> None:
    if not Package_Name:
        Package_Name = Package
    print(f'{Colors["Green"]}Installing{Colors["Reset"]} {Package_Name} package...'.ljust(150), end = '')
    if not Package_Name: 
        Package_Name = Package
    try:
        #sys.executable returns python version
        subprocess.run([sys.executable, '-m', 'pip', 'install', Package, '-q'], check=True)
    except subprocess.CalledProcessError as ex:
        Quit(
            ExceptionName = ex,
            Message = f'An {Colors["Red"]}Unknown Error{Colors["Reset"]} came out while trying to download {Package_Name}'
        )
    print(f'[{Colors["Green"]}Done{Colors["Reset"]}]!')
    


def Extract_tar(file_path: str, extract_path: str) -> None:
    print(f"{Colors['Green']}Extracting{Colors['Reset']} {file_path} {Colors['Green']}to{Colors['Reset']} {extract_path}")
    with tarfile.open(file_path, "r") as tar:
        files = tar.getmembers()
        for file in tqdm(files, desc = f'{Colors["Green"]}Extraction progress{Colors["Reset"]}'):
            tar.extract(file, path = extract_path)

    print(f"[{Colors['Green']}Done{Colors['Reset']}!]")

def Create_tar(file_path: str, directory: str) -> None:
    print(f"{Colors['Green']}Extracting{Colors['Reset']} {file_path} {Colors['Green']}to{Colors['Reset']} {directory}")
    with tarfile.open(file_path, "w:gz") as tar:
        for file in tqdm(os.listdir(directory), desc = f'{Colors["Green"]}Extraction progress{Colors["Reset"]}'):
            tar.add(os.path.join(directory, file), arcname = file)

    print(f"[{Colors['Green']}Done{Colors['Reset']}!]")

# Prompts the user (y/n)
def askUser(question: str) -> bool:
    while "the answer is invalid":
        reply = (
            str(input(f'{question}  ({Colors["Green"]}Yes{Colors["Reset"]}/{Colors["Red"]}No{Colors["Reset"]}) : '))
            .lower()
            .strip()
        )
        if reply == "yes": return True
        if reply == "no": return False

def askUserForChoice(question: str, Choice1: str, Choice2: str) -> None:
    while "the answer is invalid":
        reply = (
            str(input(question + f'\n\t[{Colors["Green"]}{Choice1}{Colors["Reset"]} / {Colors["Red"]}{Choice2}{Colors["Reset"]}] : '))
            .lower()
            .strip()
        )
        if reply == Choice1.lower(): return True
        if reply == Choice2.lower(): return False

class UnsupportedPlatformError(Exception):
    pass

# getPlatform returns variables for supported platforms.
def getPlatform() -> str:
    if platform.system() in ["Windows", "Darwin", "Linux"]:
        return platform.system()
    Quit(ExceptionName = UnsupportedPlatformError(), Message = f"{Colors['Red']}Unsupported Platform! {Colors['Reset']}\nOnly Windows or Linux are supported.\nIf you are on a Windows or Linux machine, please report this error.")

# Checks if the script has Elevated Priviledges only on Windows! In case this program will run on Unix-like systems then need to modify this function 
def isElevated():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except:
        return False

# Returns the free disk space, in bytes
def getDiskSpace() -> int:
    return shutil.disk_usage(os.getcwd())[2] #Free memory available


# Checks if dns exists and can ping a known good server
def isConnected() -> bool:
    print('Running Connection Test...')
    print('Connection Status : ', end = '')
    try:
        urllib.request.urlopen('http://google.com', timeout=2)
        print(f'\t\t[{Colors["Green"]}Online!{Colors["Reset"]}]')
        return True
    except urllib.error.URLError:
        print(f'\t\t[{Colors["Red"]}Offline!{Colors["Reset"]}]')
        return False
    

#This function adds a path to Windows Environment path and will be removed once the session (program) will be closed
def AddToEnvironmentPath(Directory: str) -> None:
    path = os.environ["PATH"]
    if Directory not in path.split(os.pathsep):
        print(f'{Colors["Green"]}Adding{Colors["Reset"]} {Directory} to the {Colors["Green"]}User Environment{Colors["Reset"]} Path Temporally...'.ljust(150), end = '')
        os.environ["PATH"] = f"{Directory}{os.pathsep}{path}"
        print(f'\t\t[{Colors["Green"]}Done!{Colors["Reset"]}]')


def DriverInstaller():
    """Installs a requested driver"""
    print('Disabling Windows Driver Signature Verification... ')
    # os.system('bcdedit /set testsigning on')


class DownloadFailedError(Exception):
    pass


def Download(URLink: str, FileName: str, retries: int = 2) -> None: #Note that some download links could expire, so need to update them...
    """
    This function will download any file from a given URLink under the name FileName in DownloadsFolder
    
    Download(URLink = 'google.com/DownloadFile.zip', FileName = 'File1.zip')
    """
    try:
        if os.path.getsize(DownloadsFolder + FileName) <= 5_000:
            os.remove(DownloadsFolder + FileName)

        if FileName in os.listdir(DownloadsFolder):
            return
    except:
        pass

    DestinationPath = DownloadsFolder + FileName
    try:

        print(f"\n{Colors['Green']}Downloading{Colors['Reset']} {FileName} {Colors['Green']}to{Colors['Reset']} {DestinationPath}")
        response = requests.get(URLink, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024 #1 Kibibyte
        progress = tqdm(miniters=1, total=total_size, unit='MB', unit_scale=True, desc=f'{Colors["Green"]}Download progress{Colors["Reset"]}')

        with open(DestinationPath, "wb") as file:
            for data in response.iter_content(block_size):
                progress.update(len(data))
                file.write(data)

        progress.close()
        print(f"{Colors['Red']} -> {Colors['Reset']}[{Colors['Green']}Done{Colors['Reset']}!]\n")

    except requests.exceptions.ConnectionError:  # If the download has been interrupted for Connection Lost or the connection was Forcibly closed
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
        if retries > 0:
            Download(URLink, FileName, retries - 1)
    except:
        Quit(ExceptionName = DownloadFailedError(), Message = f"{FileName} failed to be downloaded for some reason.")

    try:
        if os.path.getsize(DownloadsFolder + FileName) <= 5_000:
            Quit(
                ExceptionName = SystemExit(),
                Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} download {FileName} for unknown reason!\nThe file seems {Colors["Red"]}corrupted{Colors["Reset"]}!'
            )
    except Exception as ex:
        Quit(
            ExceptionName = ex,
            Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} find {FileName} file for unknown reason!\nMaybe the file package is {Colors["Red"]}corrupted{Colors["Reset"]}!'
        )


# Gets zip file name and extracts its contents inside a path : Zip_FileName = 'Ajk.zip', DestinationPath = ToolsFolder -> inside ToolsFolder will be extracted all files
def ExtractZip(Zip_FileName: str, DestinationPath: str, HasFolderInside: bool, Rename: bool = False, SpecificFile: str = ''):

    ListDir_Before = set(os.listdir(DestinationPath))
    try:
        if os.path.getsize(DestinationPath + Zip_FileName[:-4]) <= 5_000: #Checks if folder's size is 5Kb, if so remove it and re-extract the zip file
            os.remove(ToolsFolder + Zip_FileName[:-4])
    except:
        pass

    if SpecificFile:
        try:
            if os.path.getsize(DestinationPath + SpecificFile) <= 5_000:
                os.remove(ToolsFolder + SpecificFile)
                return
        except:
            pass
    
    Zip_Path = DownloadsFolder + Zip_FileName
    
    if Zip_FileName[:-4] in os.listdir(ToolsFolder) or Zip_FileName[:-4] in os.listdir(DestinationPath):
        try:
            if os.path.getsize(DownloadsFolder + Zip_FileName[:-4]) >= 5_000: #Checks if folder's size is 5Kb, if so remove it and re-extract the zip file
                return
        except:
            pass
        try:
            if os.path.getsize(ToolsFolder + Zip_FileName[:-4]) >= 5_000: #Checks if folder's size is 5Kb, if so remove it and re-extract the zip file
                return
        except:
            pass

    if not HasFolderInside:
        DestinationPath += Zip_FileName[:-4]
        
    print(f"{Colors['Green']}Extracting{Colors['Reset']} {Zip_FileName} {Colors['Green']}to{Colors['Reset']} {DestinationPath}")
    
    with zipfile.ZipFile(Zip_Path, "r") as zip_ref:
        try:
            if SpecificFile:
                zip_file = zipfile.ZipFile(Zip_Path)
                file_size = zip_file.getinfo(SpecificFile).file_size
                with tqdm(total=file_size, unit='B', unit_scale=True, desc = f'{Colors["Green"]}Extraction progress{Colors["Reset"]}') as pbar:
                    with zip_file.open(SpecificFile) as zip_file_obj, open(DestinationPath + '\\' + SpecificFile, 'wb') as out_file:
                        while True:
                            data = zip_file_obj.read(4096)
                            if not data:
                                break
                            out_file.write(data)
                            pbar.update(len(data))
                # zip_ref.extract(member = SpecificFile, path = DestinationPath, pwd = None)
            else:
                zip_ref.extractall(path = DestinationPath, pwd = None, members = tqdm(zip_ref.infolist(), unit='MB', desc = f'{Colors["Green"]}Extraction progress{Colors["Reset"]}'))

        except zipfile.error as ex:
            Quit(
                ExceptionName = ex, 
                Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} Extract {Zip_FileName}!'
            )
        except Exception as ex:
            Quit(
                ExceptionName = ex, 
                Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} Extract {Zip_FileName} for unknown reasons!'
            )


    ListDir_After = set(os.listdir(DestinationPath))
    if Rename and HasFolderInside:
        Extracted_FolderName = list(ListDir_After - ListDir_Before)[0]
        try:
            os.mkdir(DownloadsFolder + Zip_FileName[:-4])
        except:
            pass
        subprocess.check_output(f'move {DownloadsFolder}{Extracted_FolderName}\* {DownloadsFolder}{Zip_FileName[:-4]}', stderr = subprocess.STDOUT, shell = True)
        # subprocess.check_output(f'rmdir {DownloadsFolder}Temp\\', stderr = subprocess.STDOUT, shell = True)
        try:
            os.rmdir(DownloadsFolder + Extracted_FolderName)
        except:
            pass

    print(f"{Colors['Red']} -> {Colors['Reset']}[{Colors['Green']}Done{Colors['Reset']}!]\n")
    

def GetFileName_FromZip(Zip_Path: str, FileName) -> bool:
    try:
        with zipfile.ZipFile(Zip_Path, "r") as zip_ref:
            namelist = zip_ref.namelist()
            if FileName in namelist:
                return True
            return False
    except Exception as ex:
        Quit(ExceptionName = ex, Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} find {FileName} file!')


def Install_USBDrivers(Model: str, URL: str, Exe_File: str, isZip: bool, HasFolderIn: bool = False) -> None:
    print(f'{Colors["Green"]}Installing{Colors["Reset"]} {Model} {Colors["Green"]}USB drivers{Colors["Reset"]}...')
    Download(
        URLink = URL,
        FileName = f'{Model}Drivers.zip'
    )
    if isZip:
        ExtractZip(
            Zip_FileName = f'{Model}Drivers.zip',
            DestinationPath = ToolsFolder,
            HasFolderInside = HasFolderIn
        )
        
    print(f'\n{Colors["Red"]}Executing{Colors["Reset"]} USB driver installer...')
    print(f'\n{Colors["Red"]}Please{Colors["Reset"]} follow the {Colors["Red"]}instructions{Colors["Reset"]} given by the installer!')

    if isZip:
        os.startfile(f'{ToolsFolder}{Model}Drivers\\{Exe_File}')
    else:
        os.startfile(ToolsFolder + Exe_File)

    print(f'{Colors["Red"]} -> {Colors["Reset"]}[{Colors["Green"]}Installation Completed{Colors["Reset"]}!]')
    

# The user has to follow these steps in order to be able to use Adb
def SetupDeviceForUSBCommunication():
    print(f'''

    1. Open your device {Colors["Green"]}settings{Colors["Reset"]} and navigate into "About my phone" option.
    2. Search for "{Colors["Red"]}Build number{Colors["Reset"]}" option inside these settings (if you cannot find it try in "{Colors["Green"]}Software Information{Colors["Reset"]}" option).
    3. Tap 7 times on "Build number" option to enable {Colors["Red"]}Developer Options{Colors["Reset"]}.
    4. Go back to settings and {Colors["Red"]}search{Colors["Reset"]} for Developer Options.
    5. Search for "{Colors["Red"]}USB debugging{Colors["Reset"]}" option and {Colors["Green"]}enable{Colors["Reset"]} it.
    6. {Colors["Green"]}Connect{Colors["Reset"]} now your device to your computer trough USB cable and check your device screen.
    7. {Colors["Green"]}Allow{Colors["Reset"]} the pop-up asking for computer permissions.
    8. Now search inside Developer Options for "{Colors["Red"]}Select USB configuration{Colors["Reset"]}".
    9. Click it and select "{Colors["Green"]}MTP File transfer{Colors["Reset"]}" protocol.'''
    )

    input(f'\n\t=> Press {Colors["Green"]}Enter{Colors["Reset"]} key to continue : ')

    print(f'\n    10. Now search for "{Colors["Red"]}OEM Unlocking{Colors["Reset"]}" option in Developer options and {Colors["Green"]}ENABLE{Colors["Reset"]} it!')
    print(
        f'''
        {Colors["Red"]}IF{Colors["Reset"]} YOU CANNOT FIND THAT OPTION THEN LOOK AT THESE DOCUMENTATION :
            1. Missing "OEM Unlocking" options : 
                           "{Colors["Blue"]}https://krispitech.com/fix-the-missing-oem-unlock-in-developer-options/{Colors["Reset"]}"
            2. "OEM Unlocking" shows "Connect to the internet or contact your carrier" : 
                           "{Colors["Blue"]}https://www.quora.com/Why-do-some-mobile-companies-refuse-to-unlock-bootloaders-like-Huawei-and-Realme{Colors["Reset"]}"
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
        DestinationPath = ToolsFolder,  #ToolsFolder is already in local Env. Path.
        HasFolderInside = True #-> "platform-tools"
    )
    print(
        f"{Colors['Red']}Removing{Colors['Reset']} platform-tools.zip",
        end = ''
    )
    os.remove(DownloadsFolder + 'plattools.zip')

    print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')

def Install_AdbDrivers():
    Download(
        URLink = "https://dl.google.com/android/repository/usb_driver_r13-windows.zip",
        FileName = "AdbDrivers.zip"
    )

    ExtractZip(
        Zip_FileName = "AdbDrivers.zip",
        DestinationPath = ToolsFolder,
        HasFolderInside = True #-> "usb_driver" 
    )
    if not checkTool('pnputil.exe'):
        Quit(
            ExceptionName = SystemExit(),
            Message = f'Your windows machine has not {Colors["Red"]}pnputil.exe{Colors["Reset"]} (A driver manager) installed!'
        )

    print(f'{Colors["Green"]}Trying{Colors["Reset"]} to install Google USB Drivers (Adb&Fastboot drivers)...'.ljust(150), end = '')
    
    pnputil_Out = str(subprocess.check_output(f'pnputil /add-driver {ToolsFolder}usb_driver\\android_winusb.inf /install', stderr = subprocess.STDOUT, shell = True), encoding = 'utf-8')
    Published_Name = pnputil_Out.split('\n')[4] if 'Published Name:' in pnputil_Out.split('\n')[4] else ''
    Driver_Info = str(subprocess.check_output('pnputil /enum-drivers', stderr = subprocess.STDOUT, shell = True), encoding = 'utf-8').split('\n')
    Driver_Info = Driver_Info[Driver_Info.index(Published_Name):Driver_Info.index(Published_Name) + 9]
    if 'successfully' not in pnputil_Out:
        Quit(
            ExceptionName = SystemExit(),
            Message = f'\n[{Colors["Red"]}pnputil.exe{Colors["Reset"]}] cannot install or update Adb USB drivers for an unknown reason!' #TODO: Check for any error on using pnputil.exe
        )
    print(f'[{Colors["Green"]}Installed{Colors["Reset"]}!]')    #Same process with Fastboot drivers, to install them the user has to be rebooted into fastboot.

    print('Driver Informations: ')
    for line in Driver_Info:
        Information = line.split(':')[0]
        Info = line.split(':')[1].strip()
        print(f'\t[{Colors["Red"]}{Information}{Colors["Reset"]}]:'.ljust(20), f'{Colors["Green"]}{Info}{Colors["Reset"]}')


def Check_AdbConnection(AdbOrFastboot: str = 'Adb', DriversInstaller: function = Install_AdbDrivers, Retries: int = 4) -> None:
    print(f'\n\n{Colors["Green"]}Checking{Colors["Reset"]} {AdbOrFastboot} Connection...'.ljust(150), end = '')
    try:
        AdbDevices_output = subprocess.check_output(f"{AdbOrFastboot} devices", stderr = subprocess.STDOUT, shell = True, encoding = 'utf-8').strip()
        if not AdbDevices_output[-6:] == 'device':
            if Retries == 0:
                if not askUser(f'\t{Colors["Red"]}Cannot{Colors["Reset"]} determinate {AdbOrFastboot} connection!\n\tDo you want to check it again?'):
                    Quit(
                        ExceptionName = SystemExit(), 
                        Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} determinate Adb Connection!'
                        )
                Check_AdbConnection(AdbOrFastboot, DriversInstaller)

            elif Retries == 1:
                if DriverInstaller:
                    DriversInstaller()
            if Retries == 3 and AdbOrFastboot.lower() == 'adb':
                print(
                f'''
            {Colors["Red"]}\nCannot determinate{Colors["Reset"]} USB Connection!
    Please, make sure "{Colors["Red"]}USB debugging{Colors["Reset"]}" option is enabled and the {Colors["Green"]}USB cable{Colors["Reset"]} is plugged in your Android and in your Computer's USB port!
    If this message comes out on your Android's screen then allow it:
        {Colors["Green_Highlight"]}Allow USB debugging? {Colors["Reset"]}
        {Colors["Green_Highlight"]}The computer's RSA key fingerprint is :{Colors["Reset"]}
        {Colors["Green_Highlight"]}1B:28:11:B0:AC:F4:E6:1E:01:0D {Colors["Reset"]}           [For example]
        {Colors["Green"]}☑ {Colors["Reset"]}{Colors["Green_Highlight"]}Always allow from this computer {Colors["Reset"]}
                    cancel  {Colors["Green"]}OK{Colors["Reset"]}
                    ''')

            input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} to try again the connection : ")
            Check_AdbConnection(AdbOrFastboot, DriversInstaller, Retries - 1)
        #TODO: Improve this process. test it on some machines
        else:
            return True

    except subprocess.CalledProcessError:
        Quit(
            ExceptionName = SystemExit(), 
            Message = f'''
    {Colors["Red"]}Cannot determinate{Colors["Reset"]} USB Connection!
    This could be because Adb&Fastboot or USB Drivers are not correctly installed...'''
        )

    print(f'[{Colors["Green"]}Connected{Colors["Reset"]}!]\n')
    
    
def Check_FastbootConnection() -> bool: #TODO: Work on this function once Samsung setup is finished
    try:
        FastbootDevices_output = subprocess.check_output("fastboot devices", stderr = subprocess.STDOUT, shell = True).strip()
        return FastbootDevices_output[-6:] == b'device'
        
    except subprocess.CalledProcessError:
        Quit(
            ExceptionName = SystemExit(),
            Message = f'''
    {Colors["Red"]}Cannot determinate{Colors["Reset"]} USB Connection!
    This could be because Adb&Fastboot or USB Drivers are not correctly installed...'''
        )

def Download_Magisk(Install: bool = False):

    #it's better to not check for updates because magisk binaries will be compiled in magisk v25.2
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
    if Install:
        Check_AdbConnection()
        print(f'{Colors["Green"]}Installing{Colors["Reset"]} Magisk Manager...'.ljust(150), end = '')
        subprocess.check_output(f'adb install {DownloadsFolder}Magisk.apk', stderr=subprocess.STDOUT, shell = True)
        print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')


def Install_RootChecker():
    Download(
        URLink = 'https://r-static-assets.androidapks.com/rdata/e926f4a430b18c98eed9a6a5208f1cf6/com.joeykrim.rootcheck_v6.5.3-197_Android-4.4.apk',
        FileName = 'RootChecker.apk'
    )
    Check_AdbConnection()
    print(f'{Colors["Green"]}Installing{Colors["Reset"]} Root Checker...'.ljust(150), end = '')
    subprocess.check_output(f'adb install {DownloadsFolder}RootChecker.apk', stderr=subprocess.STDOUT, shell = True)
    print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')

def ConfigureMagisk():
    """
    Once Flashed the patched image the user has to configure Magisk Manager to let it install additional packages.
    Once the user accept, the phone will reboot.
    Asks user if he wants to configure Zygisk
     -> Returns an available Adb Connection
    """

    print(f'\t\t[{Colors["Green"]}Configuring{Colors["Reset"]} Magisk Manager]')
    print(f'{Colors["Green"]}Starting{Colors["Reset"]} Magisk Manager Application...'.ljust(150), end = '')
    subprocess.check_output('adb shell am start -n com.topjohnwu.magisk/.ui.MainActivity filter 55aa8bf', stderr=subprocess.STDOUT, shell = True)
    print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')

    print(f'''
        
    1. {Colors["Red"]}Now{Colors["Reset"]} Magisk Manager will ask you, throught a pop-up, to install {Colors["Green"]}Additional Setup{Colors["Reset"]} like this :
                            {Colors["White_Highlight"]}{Colors["Grey"]} Requires Additional Setup {Colors["Reset"]}
                {Colors["White_Highlight"]} Your device needs additional setup for Magisk to {Colors["Reset"]} 
                {Colors["White_Highlight"]} work properly. Do you want to proceed and reboot? {Colors["Reset"]}
                
                                                {Colors["Cyan"]} CANCEL {Colors["Reset"]}      {Colors["Cyan"]} OK {Colors["Reset"]}

    2. Your phone will {Colors["Green"]}reboot{Colors["Reset"]}...
    ''')
    input(f"Press {Colors['Green']}ENTER{Colors['Reset']} if your device has been booted correctly : ")
    Check_AdbConnection()
    
    def Configure_Zygisk():
        """
        Zygisk is a Magisk library which will run parts of Magisk in the zygote process to make Magisk modules more powerful.
        This Magisk's setting feature is required in order to hide root permissions from apps.
        This function will guide the user on setting up this feature.
         -> Zygisk is supported for Magisk V24 or Higher! 
        """
        print(f' -> {Colors["Green"]}Starting Zygisk{Colors["Reset"]} configuration process...')
        Download(
            URLink = 'https://github.com/kdrag0n/safetynet-fix/releases/download/v2.4.0/safetynet-fix-v2.4.0.zip',
            FileName = 'safetynet-fix.zip'
        )
        Download(
            URLink = 'https://github.com/LSPosed/LSPosed.github.io/releases/download/shamiko-126/Shamiko-v0.6-126-release.zip',
            FileName = 'Shamiko.zip'
        )
        
        print(f'{Colors["Green"]}Pushing{Colors["Reset"]} Safetynet-fix.zip into /sdcard/Download Folder...'.ljust(150), end = '')
        subprocess.check_output(f'adb push {DownloadsFolder}safetynet-fix.zip /sdcard/Download', stderr=subprocess.STDOUT, shell = True)
        print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')
        
        print(f'{Colors["Green"]}Pushing{Colors["Reset"]} Shamiko.zip into /sdcard/Download Folder...'.ljust(150), end = '')
        subprocess.check_output(f'adb push {DownloadsFolder}Shamiko.zip /sdcard/Download', stderr=subprocess.STDOUT, shell = True)
        print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')

        print(f'{Colors["Green"]}Starting{Colors["Reset"]} Magisk Manager Application...'.ljust(150), end = '')
        subprocess.check_output('adb shell am start -n com.topjohnwu.magisk/.ui.MainActivity filter 55aa8bf', stderr=subprocess.STDOUT, shell = True)
        print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')
        print(
    f'''
        Your phone's screen should now show Magisk Manager Application.
        {Colors["Green"]}In order to{Colors["Reset"]} setup Magisk Hide follow these instructions : 

        1. Enter in {Colors["Green"]}Magisk's settings{Colors["Reset"]} by clicking on the small settings wheel on the top right.
        2. {Colors["Green"]}Now{Colors["Reset"]} scroll down to 'Magisk' caption and enable '{Colors["Green"]}Zygisk{Colors["Reset"]}' and '{Colors["Green"]}Enforce DenyList{Colors["Reset"]}' features.
        3. {Colors["Green"]}Reboot{Colors["Reset"]} your phone.
    ''')
        input(f"\n\tPress {Colors['Green']}ENTER{Colors['Reset']} if your device has been booted correctly : ")
    
        print(
    f'''
        4. {Colors["Green"]}Now{Colors["Reset"]} open Magisk Application and click on '{Colors["Green"]}Modules{Colors["Reset"]}' section on the bottom right.
        5. Click on '{Colors["Green"]}Install from storage{Colors["Reset"]}' option on the top.
        6. A File Explorer will now appear. Navigate into {Colors["Green"]}Download Folder{Colors["Reset"]} of your phone and click on '{Colors["Red"]}safetynet-fix.zip{Colors["Reset"]}' file.
        7. Magisk will now start the flashing process...
        8. If the process of flashing is '- Done' then {Colors["Underline"]}go back to 'Modules' section and click back to '{Colors["Green"]}Install from storage{Colors["Reset"]}'{Colors["Reset"]}.
        9. This time click on '{Colors["Red"]}Shamiko.zip{Colors["Reset"]}' file.
        10. Once the flashing process is finished, click on '{Colors["Green"]}Reboot{Colors["Reset"]}'
    ''')
        input(f"\n\tPress {Colors['Green']}ENTER{Colors['Reset']} if your device has been booted correctly : ")

        print(
    f'''
        11. {Colors["Green"]}Now{Colors["Reset"]} go back to Magisk Application and {Colors["Green"]}click on settings{Colors["Reset"]}.
        12. Click on '{Colors["Red"]}DenyList{Colors["Reset"]}' option under 'Magisk' caption.
        13. From there click on the {Colors["Green"]}three dots{Colors["Reset"]} on the top right and click on '{Colors["Green"]}Show System apps{Colors["Reset"]}' feature.
        14. Now search for '{Colors["Green"]}Google Play services{Colors["Reset"]}Google Play services' and click on it.
        15. From there make sure that {Colors["Green"]}only{Colors["Reset"]} '{Colors["Green"]}com.google.android.gms{Colors["Reset"]}' and '{Colors["Green"]}com.google.android.gms.unstable{Colors["Reset"]}' options are {Colors["Green"]}enabled{Colors["Reset"]}.
        {Colors["Red"]} ->{Colors["Reset"]} Once done, {Colors["Underline"]}you'll be able to hide root from apps{Colors["Reset"]} (like banking apps) by just adding them to the 'DenyList'.
    ''')

        print(f'{Colors["Green"]}Zygisk{Colors["Reset"]} has been now configured!')
        Check_AdbConnection()

    if not askUser(f'Do you want to {Colors["Green"]}setup Zygisk{Colors["Reset"]} (It lets you {Colors["Green"]}hide root{Colors["Reset"]} from other applications)?'):
        print(f'{Colors["Green"]}Ok{Colors["Reset"]}, then your phone is now rooted, you can check it by installing "{Colors["Green"]}Root Checker{Colors["Reset"]}".')
        if askUser(f'Do you want to {Colors["Green"]}install{Colors["Reset"]} "{Colors["Green"]}Root Checker{Colors["Reset"]}"?'):
            Install_RootChecker()
        return
    Configure_Zygisk()


def Patch_Image_File(Device: object, BootImage_Name: str = 'boot.img') -> None: #
    """
    Returns a folder in Firmware's folder called 'PatchedFiles'
    The patched file is 'new-boot.img' and will be transfered in 'Extracted_Files' folder under the stock image name {BootImage_Name}.
    The stock image will be named 'stock_{BootImage_Name}'.
        -> Returns and available Adb Connection
    """
    #Possible CPU Architectures : x86_64, x86, arm64-v8a or armeabi-v7a
    if Device.CPU_Architecture not in ['x86_64', 'x86', 'arm64-v8a', 'armeabi-v7a']:    #Maybe add this on the setup or in Main.py...
        Quit(
            ExceptionName = SystemExit(),
            Message = 'Your phone\'s CPU architecture is not supported!\nCannot patch your Firmware\'s images!'
            )

    Download(   #Maybe, with magisk manager version checker there could be a way to download latest binaries available
        URLink = 'https://drive.google.com/u/2/uc?id=1LMdONt1h9RomulwJ7GH0sCO9zd--3I1x&export=download&confirm=t&uuid=fba89616-a873-4e7b-94ae-603014278017&at=ALgDtswLkER--8DnmWFuqkYO_ffR:1676124254434',
        FileName = 'MagiskBinaries.zip'
        )
    ExtractZip(
        Zip_FileName = 'MagiskBinaries.zip',
        DestinationPath = ToolsFolder,
        HasFolderInside = False
        )
    
    Check_AdbConnection()
    print(f'\n\n\t[Now it\'s time to patch {Colors["Green"]}Firmware Binaries{Colors["Reset"]} in order to root your device!]\n')
    OutFolder = f'/data/local/tmp/{Device.CPU_Architecture}/' #Maybe check if every device has this path, maybe not tmp folder. Will adb create this folder in case it doesn't exists?
    FilePath = ToolsFolder + 'MagiskBinaries'

    print(f'{Colors["Green"]}Sending{Colors["Reset"]} Magisk Binaries to {OutFolder}'.ljust(150), end = '')
    subprocess.check_output(f'adb push {FilePath}\\{Device.CPU_Architecture}\\ /data/local/tmp/', stderr=subprocess.STDOUT, shell = True)
    subprocess.check_output(f'adb push {FilePath}\\util_functions.sh {OutFolder}', stderr=subprocess.STDOUT, shell = True)
    subprocess.check_output(f'adb push {FilePath}\\boot_patch.sh {OutFolder}', stderr=subprocess.STDOUT, shell = True)
    subprocess.check_output(f'adb push {FilePath}\\stub.apk {OutFolder}', stderr=subprocess.STDOUT, shell = True)
    print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')
        
    FilePath = DownloadsFolder + 'Firmware\\Extracted_Files'
    #BOOT.IMG or INIT_BOOT.IMG
    print(f'{Colors["Green"]}Sending{Colors["Reset"]} {BootImage_Name} to {OutFolder}'.ljust(150), end = '')
    subprocess.check_output(f'adb push {FilePath}\\{BootImage_Name} {OutFolder}', stderr=subprocess.STDOUT, shell = True)
    print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')

    #RECOVERY.IMG
    if 'recovery.img' in os.listdir(FilePath):
        print(f'{Colors["Green"]}Sending{Colors["Reset"]} recovery.img to {OutFolder}'.ljust(150), end = '')
        subprocess.check_output(f'adb push {FilePath}\\recovery.img {OutFolder}', stderr=subprocess.STDOUT, shell = True)
        print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')
        BootImage_Name = 'recovery.img'

    subprocess.check_output(f'adb shell "chmod +x {OutFolder}magiskboot"', stderr=subprocess.STDOUT, shell = True)
    subprocess.check_output(f'adb shell "chmod +x {OutFolder}boot_patch.sh"', stderr=subprocess.STDOUT, shell = True)

    print(f'{Colors["Green"]}Parsing{Colors["Reset"]} {BootImage_Name} ...'.ljust(150), end = '')
    os.system(f"adb shell \"echo '/data/local/tmp/arm64-v8a/magiskboot unpack {OutFolder}{BootImage_Name}' > {OutFolder}ParseBoot.img.sh\" ") #CHECK: If use os.system() then the script will output what it is doing...
    Parsing = str(subprocess.check_output(f'adb shell "cd {OutFolder} && sh ./ParseBoot.img.sh"', stderr = subprocess.STDOUT, shell = True), encoding='utf-8')

    # Parsing boot image: [/data/local/tmp/arm64-v8a/boot.img]
    # HEADER_VER      [0]
    # KERNEL_SZ       [31562544]
    # RAMDISK_SZ      [5395795]
    # SECOND_SZ       [0]
    # EXTRA_SZ        [477184]
    # OS_VERSION      [9.0.0]
    # OS_PATCH_LEVEL  [2021-05]
    # PAGESIZE        [2048]
    # NAME            [SRPQC03B014KU]
    # CMDLINE         []
    # CHECKSUM        [3f384cb12541963212c74b53545d3a2fa5ec8e09000000000000000000000000]
    # KERNEL_FMT      [raw]
    # RAMDISK_FMT     [gzip]
    # EXTRA_FMT       [raw]
    # SAMSUNG_SEANDROID

    HasRamdisk = 'RAMDISK_SZ      [0]' not in Parsing
    print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')

    #KEEPVERITY, KEEPFORCEENCRYPT, PATCHVBMETAFLAG, RECOVERYMODE
    #KEEPVERITY is generally better to not add it... it just maintains data verification (operating system files are checked to ensure they have not been modified in an unauthorized manner.)
    Image = BootImage_Name
    Parameters = ''
    # if Device.IsEncrypted == 'encrypted':      #This is quite optional as if not given then boot_patch.sh COULD remove the encryption from the device... it's just Android security options... (Mind if need a TWRP)
    #     Parameters += 'KEEPFORCEENCRYPT'

    if not HasRamdisk:
        print(f'{Colors["Red"]}Detected{Colors["Reset"]} that your phone does not have {Colors["Green_Highlight"]}ramdisk{Colors["Reset"]}!')
        print(f'\t -> {Colors["Red"]}Using{Colors["Reset"]} {Colors["Green"]}recovery.img{Colors["Reset"]} instead of boot.img !')
        Parameters += 'RECOVERYMODE'
        Image = 'recovery.img'


    print(f'{Colors["Green"]}Running{Colors["Reset"]} patching process...'.ljust(150), end = '')
    subprocess.check_output(f'adb shell sh {OutFolder}/boot_patch.sh {OutFolder}/{Image} {Parameters}', stderr=subprocess.STDOUT, shell = True) #CHECK: If use os.system() then the script will output what it is doing...
    print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')
    

    print(f'{Colors["Red"]}Getting{Colors["Reset"]} Directory\'s files...')
    DirectoryFiles = str(subprocess.check_output(f'adb shell "ls -1 {OutFolder}"', stderr=subprocess.STDOUT, shell=True), encoding = 'utf-8').split('\n')
    print(f'\t{Colors["White"]}{OutFolder}{Colors["Reset"]} :')
    for line in DirectoryFiles:
        line = line.strip()
        if not line: continue
        if line.endswith('.img'):
            line = line.replace(line, f'{Colors["Cyan"]}{line}{Colors["Reset"]}')
        elif line.endswith('.sh') or line == 'extra':   #elif just to avoid making useless if statements...
            line = line.replace(line, f'{Colors["Magenta"]}{line}{Colors["Reset"]}')
        elif line.endswith('.a'):
            line = line.replace(line, f'{Colors["Grey"]}{line}{Colors["Reset"]}')
        elif line.endswith('.apk'):
            line = line.replace(line, f'{Colors["Blue"]}{line}{Colors["Reset"]}')
        elif line == 'kernel':
            line = line.replace(line, f'{Colors["Red"]}{line}{Colors["Reset"]}')
        elif line == 'busybox':
            line = line.replace(line, f'{Colors["Yellow"]}{line}{Colors["Reset"]}')
        print('\t\t\t └⇀', line)

    print(f'\n{Colors["Green"]}Pulling{Colors["Reset"]} patched files...'.ljust(150), end = '')
    subprocess.check_output(f'adb pull {OutFolder} {DownloadsFolder}Firmware\\PatchedFiles', stderr=subprocess.STDOUT, shell = True)
    print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')

    subprocess.check_output(f'move {DownloadsFolder}Firmware\\Extracted_Files\\boot.img {DownloadsFolder}Firmware\\Extracted_Files\\stock_{BootImage_Name}', stderr=subprocess.STDOUT, shell = True)
    subprocess.check_output(f'move {DownloadsFolder}Firmware\\PatchedFiles\\new-boot.img {DownloadsFolder}Firmware\\Extracted_Files\\{BootImage_Name}', stderr=subprocess.STDOUT, shell = True)

    print('\n\n')


#Other functions for other devices...
