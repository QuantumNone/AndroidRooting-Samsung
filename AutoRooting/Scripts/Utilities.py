#Copyright (C) <2023> by <Quantum>


# [AutoRootUtiilities.py] file will contain several functions, where mostly of them are required for the Setup.py and for Main.py files

import os, platform, ctypes, shutil, urllib.request, zipfile, subprocess, requests, sys, tarfile
from tqdm import tqdm
from time import sleep
sleepDelay = 2

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
    print('\n', Message)
    input(f"Press {Colors['Red']}ENTER{Colors['Reset']} to exit : ")
    raise ExceptionName

def find_files(root_dir: str, extension: str, file_name: str, NoExtension: bool = False) -> list[str]:
    #This is because some files (such as boot.img) are renamed with an other extension, for example lz4
    return [root_dir + f for f in os.listdir(root_dir) if (f.startswith(file_name) and (NoExtension or f.endswith(f'.{extension}')))]

def CheckFile(Filename: str, Directory = f'{os.getcwd()}\\') -> bool:
    return os.path.isfile(f'{Directory}{Filename}')

# Checks if whatever executable provided (as string) exists in $PATH
def checkTool(name: str) -> bool:
    return shutil.which(name) is not None

def Pip_Installer(Package: str, Package_Name: str = '') -> None:
    if not Package_Name: 
        Package_Name = Package
    try:
        #sys.executable returns python version
        subprocess.run([sys.executable, '-m', 'pip', 'install', Package, '-q'], check=True)
    except subprocess.CalledProcessError as ex:
        Quit(ExceptionName = ex(), Message = f'An {Colors["Red"]}Unknown Error{Colors["Reset"]} came out while trying to download {Package_Name} : {Package}')


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

def Download(URLink: str, FileName: str, retries: int = 2) -> None:
    try:
        if os.path.getsize(DownloadsFolder + FileName) <= 1_000_000:
            os.remove(DownloadsFolder + FileName)

        if FileName in os.listdir(DownloadsFolder):
            return
    except:
        pass

    DestinationPath = DownloadsFolder + FileName
    try:
        print(f"{Colors['Green']}\nDownloading{Colors['Reset']} {FileName} {Colors['Green']}to{Colors['Reset']} {DestinationPath}")
        with tqdm(miniters=1, desc = f'{Colors["Green"]}Download progress{Colors["Reset"]}') as DownFile:  #Progress bar
            urllib.request.urlretrieve(
                URLink, 
                DestinationPath, 
                reporthook = DownFile.update()
            )
        print(f"[{Colors['Green']}Done{Colors['Reset']}!]")

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
        if retries > 0:
            Download(URLink, FileName, retries - 1)
    except:
        Quit(ExceptionName = DownloadFailedError(), Message = f"{FileName} failed to be downloaded for some reason.")


# Gets zip file name and extracts its contents inside a path : Zip_FileName = 'Ajk.zip', DestinationPath = ToolsFolder -> inside ToolsFolder will be extracted all files
def ExtractZip(Zip_FileName: str, DestinationPath: str, HasFolderInside: bool):
    
    if not HasFolderInside:
        DestinationPath += Zip_FileName[:-4]

    Zip_Path = DownloadsFolder + Zip_FileName
    try:
        if os.path.getsize(ToolsFolder + Zip_FileName[:-4]) <= 1_000_000: #Checks if folder's size is 0Kb, if so remove it and re-extract the zip file
            os.remove(ToolsFolder + Zip_FileName[:-4])
    except:
        pass
    
    if Zip_FileName[:-4] in os.listdir(ToolsFolder):
        return

    print(f"{Colors['Green']}Extracting{Colors['Reset']} {Zip_FileName} {Colors['Green']}to{Colors['Reset']} {DestinationPath}")
    
    with zipfile.ZipFile(Zip_Path, "r") as zip_ref:
        try:
            zip_ref.extractall(DestinationPath, pwd = None, members = tqdm(zip_ref.infolist(), desc = f'{Colors["Green"]}Extraction progress{Colors["Reset"]}'))

        except zipfile.error as ex:
            Quit(ExceptionName = ex(), Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} Extract {Zip_FileName}!')

    print(f"[{Colors['Green']}Done{Colors['Reset']}!]")



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
        DestinationPath = ToolsFolder,
        HasFolderInside = True
    )
    print(
        f"{Colors['Red']}Removing{Colors['Reset']} platform-tools.zip",
        end = ''
    )
    os.remove('Downloads\\plattools.zip')

    print(f'[{Colors["Green"]}Done{Colors["Green"]}!]')

def Check_AdbConnection(DriversInstaller: function = False, AdbRetries: int = 0) -> None:
    print(f'{Colors["Green"]}Checking{Colors["Reset"]} Adb Connection...'.ljust(150), end = '')
    try:
        AdbDevices_output = subprocess.check_output("adb devices", stderr = subprocess.STDOUT, shell = True, encoding = 'utf-8').strip()
        if not AdbDevices_output[-6:] == 'device':
            if AdbRetries == 2:
                Quit(ExceptionName = SystemExit(), Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} determinate Adb Connection!')
            elif AdbRetries == 1:
                if DriverInstaller:
                    DriversInstaller()

            elif AdbRetries == 0:
                print(
                f'''
            {Colors["Red"]}Cannot determinate{Colors["Reset"]} USB Connection!
    Please, make sure "{Colors["Red"]}USB debugging{Colors["Reset"]}" option is enabled and the {Colors["Green"]}USB cable{Colors["Reset"]} is plugged in your Android and in your Computer's USB port!
    If this message comes out on your Android's screen then allow it:
        {Colors["Green_Highlight"]}Allow USB debugging? {Colors["Reset"]}
        {Colors["Green_Highlight"]}The computer's RSA key fingerprint is :{Colors["Reset"]}
        {Colors["Green_Highlight"]}1B:28:11:B0:AC:F4:E6:1E:01:0D {Colors["Reset"]}           [For example]
        {Colors["Green"]}☑ {Colors["Reset"]}{Colors["Green_Highlight"]}Always allow from this computer {Colors["Reset"]}
                    cancel  {Colors["Green"]}OK{Colors["Reset"]}
                    ''')

            input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} to try again the connection : ")
            Check_AdbConnection(DriversInstaller, AdbRetries + 1)

    except subprocess.CalledProcessError:
        Quit(
            ExceptionName = SystemExit(), 
            Message = f'''
    {Colors["Red"]}Cannot determinate{Colors["Reset"]} USB Connection!
    This could be because Adb&Fastboot or USB Drivers are not correctly installed...'''
        )

    print(f'[{Colors["Green"]}Connected{Colors["Reset"]}!]')
    
    
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


def Install_GoogleUSBDriver():  #Required for all devices that use Fastboot Mode
    pass

def Install_MTKDriver():    #Chinese phones
    pass

def Download_Magisk():

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


def Patch_Image_File(Device: object) -> None: #Returns a folder in Firmware's folder called 'PatchedFiles'
        #Possible CPU Architectures : x86_64, x86, arm64-v8a or armeabi-v7a
        if Device.CPU_Architecture not in ['x86_64', 'x86', 'arm64-v8a', 'armeabi-v7a']:
            Quit(
                ExceptionName = SystemExit(),
                Message = 'Your phone\'s CPU architecture is not supported!\nCannot patch your Firmware\'s images!'
                )

        Download(   #Maybe, with magisk manager version checker there could be a way to download latest binaries available
            URLink = 'https://download851.mediafire.com/ob36tz7hyqsg/h71rwovkstiyiyf/MagiskBinaries.zip',
            FileName = 'MagiskBinaries.zip'
            )
        ExtractZip(
            Zip_FileName = 'MagiskBinaries.zip',
            DestinationPath = ToolsFolder,
            HasFolderInside = False
            )
        
        print(f'\n\n\t[Now it\'s time to patch {Colors["Green"]}Firmware Binaries{Colors["Reset"]} in order to root your device!]\n')
        OutFolder = f'/data/local/tmp/{Device.CPU_Architecture}/'
        FilePath = ToolsFolder + 'MagiskBinaries'

        print(f'{Colors["Green"]}Sending{Colors["Reset"]} Magisk Binaries to {OutFolder}'.ljust(150), end = '')
        subprocess.check_output(f'adb push {FilePath}\\{Device.CPU_Architecture}\\ /data/local/tmp/', stderr=subprocess.STDOUT, shell = True)
        subprocess.check_output(f'adb push {FilePath}\\util_functions.sh {OutFolder}', stderr=subprocess.STDOUT, shell = True)
        subprocess.check_output(f'adb push {FilePath}\\boot_patch.sh {OutFolder}', stderr=subprocess.STDOUT, shell = True)
        subprocess.check_output(f'adb push {FilePath}\\stub.apk {OutFolder}', stderr=subprocess.STDOUT, shell = True)
        print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')
            
        FilePath = DownloadsFolder + 'Firmware\\Extracted_Files'
        #BOOT.IMG
        print(f'{Colors["Green"]}Sending{Colors["Reset"]} boot.img to {OutFolder}'.ljust(150), end = '')
        subprocess.check_output(f'adb push {FilePath}\\boot.img {OutFolder}', stderr=subprocess.STDOUT, shell = True)
        print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')

        #RECOVERY.IMG
        if 'recovery.img' in os.listdir(FilePath):
            print(f'{Colors["Green"]}Sending{Colors["Reset"]} recovery.img to {OutFolder}'.ljust(150), end = '')
            subprocess.check_output(f'adb push {FilePath}\\recovery.img {OutFolder}', stderr=subprocess.STDOUT, shell = True)
            print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')

        subprocess.check_output(f'adb shell "chmod +x {OutFolder}magiskboot"', stderr=subprocess.STDOUT, shell = True)
        subprocess.check_output(f'adb shell "chmod +x {OutFolder}boot_patch.sh"', stderr=subprocess.STDOUT, shell = True)

        print(f'{Colors["Green"]}Parsing{Colors["Reset"]} boot.img ...'.ljust(150), end = '')
        os.system("adb shell \"echo '/data/local/tmp/arm64-v8a/magiskboot unpack /data/local/tmp/arm64-v8a/boot.img' > /data/local/tmp/arm64-v8a/ParseBoot.img.sh\" ")
        Parsing = str(subprocess.check_output('adb shell "cd /data/local/tmp/arm64-v8a && sh ./ParseBoot.img.sh"', stderr = subprocess.STDOUT, shell = True), encoding='utf-8')

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
        Image = 'boot.img'
        Parameters = ''
        # if Device.IsEncrypted == 'encrypted':      #This is quite optional as if not given then boot_patch.sh COULD remove the encryption from the device... it's just Android security options... (Mind if need a TWRP)
        #     Parameters += 'KEEPFORCEENCRYPT'

        if not HasRamdisk:
            print(f'{Colors["Red"]}Detected{Colors["Reset"]} that your phone does not have {Colors["Green_Highlight"]}ramdisk{Colors["Reset"]}!')
            print(f'\t -> {Colors["Red"]}Using{Colors["Reset"]} {Colors["Green"]}recovery.img{Colors["Reset"]} instead of boot.img !')
            Parameters += 'RECOVERYMODE'
            Image = 'recovery.img'


        print(f'{Colors["Green"]}Running{Colors["Reset"]} patching process...'.ljust(150), end = '')
        subprocess.check_output(f'adb shell sh {OutFolder}/boot_patch.sh {OutFolder}/{Image} {Parameters}', stderr=subprocess.STDOUT, shell = True)
        print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')
        

        print(f'{Colors["Red"]}Getting{Colors["Reset"]} Directory\'s files...')
        DirectoryFiles = str(subprocess.check_output(f'adb shell "ls -1 {OutFolder}"', stderr=subprocess.STDOUT, shell=True), encoding = 'utf-8').split('\n')
        print(f'\t{Colors["White"]}{OutFolder}{Colors["Reset"]} :')
        for line in DirectoryFiles:
            line = line.strip()
            if not line: break
            if line.endswith('.img'):
                line = line.replace(line, f'{Colors["Cyan"]}{line}{Colors["Reset"]}')
            if line.endswith('.sh')or line == 'extra':
                line = line.replace(line, f'{Colors["Magenta"]}{line}{Colors["Reset"]}')
            if line.endswith('.a'):
                line = line.replace(line, f'{Colors["Grey"]}{line}{Colors["Reset"]}')
            if line.endswith('.apk'):
                line = line.replace(line, f'{Colors["Blue"]}{line}{Colors["Reset"]}')
            if line == 'kernel':
                line = line.replace(line, f'{Colors["Red"]}{line}{Colors["Reset"]}')
            if line == 'busybox':
                line = line.replace(line, f'{Colors["Yellow"]}{line}{Colors["Reset"]}')
            print('\t\t\t └⇀', line)

        print(f'\n{Colors["Green"]}Pulling{Colors["Reset"]} patched files...'.ljust(150), end = '')
        subprocess.check_output(f'adb pull {OutFolder} {DownloadsFolder}Firmware\\PatchedFiles', stderr=subprocess.STDOUT, shell = True)
        print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')

        print('\n\n')


#Other functions for other devices...
