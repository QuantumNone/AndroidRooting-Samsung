
# [AutoRootUtiilities.py] file will contain several functions, where mostly of them are required for the Setup.py and for Main.py files

import os, platform, ctypes, shutil, socket, urllib.request, zipfile, subprocess, requests, sys, tarfile
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

OSDriveLetter = str(subprocess.check_output(f'echo %USERPROFILE%', stderr = subprocess.STDOUT, shell = True))[2:4] + '\\'
DownloadsFolder = os.getcwd() + '\\Downloads\\'
ToolsFolder = os.getcwd() + '\\Tools\\'
class function: #Used just by Type Hinting for understanding variable type
    pass


try:
    os.mkdir("Tools")
except FileExistsError:
    pass
try:
    os.mkdir("Downloads")
except FileExistsError:
    pass


def Quit(ExceptionName: Exception, Message: str) -> Exception:
    print(Message)
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


Pip_Installer(Package = 'tqdm')
from tqdm import tqdm

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

AddToEnvironmentPath(Directory = DownloadsFolder)
AddToEnvironmentPath(Directory = ToolsFolder)

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

def Check_AdbConnection(DriversInstaller: function, AdbRetries: int = 0) -> None:
    print(f'{Colors["Green"]}Checking{Colors["Reset"]} Adb Connection...', end = '')
    try:
        AdbDevices_output = subprocess.check_output("adb devices", stderr = subprocess.STDOUT, shell = True, encoding = 'utf-8').strip()
        if not AdbDevices_output[-6:] == 'device':
            if AdbRetries == 2:
                Quit(ExceptionName = SystemExit(), Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} determinate Adb Connection!')
            elif AdbRetries == 1:
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

    print(f'\t[{Colors["Green"]}Connected{Colors["Reset"]}!]')
    
    
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


#Other functions for other devices...

def Samsung_Requirements(Phone):
    def Install_SamsungUSBDrivers(InstallationStatus: bool = True) -> None:
        Download(
            URLink = "https://developer.samsung.com/sdp/file/2ad30860-0932-44e3-bf63-765a5cfa1010",
            FileName = "SamsungUSB-installer.exe"
        )

        #Let's not reboot the computer and try to check if the USB Communication works, if not then the pc will require reboot (Or Windows Driver signature offline)
        print(
            f'Please, follow the instructions that the installer shows!'
        )
        os.startfile(f'{DownloadsFolder}SamsungUSB-installer.exe')
        print('Installation Completed!')

        #HAVE TO WORK ON THAT
        if not InstallationStatus: #This can be converted into a function like : checkAdbConnection() (If not connected, check USB drivers) 
            print(
                f'''
                The USB communication cannot be enstablished!
                Try to reboot your computer or try to {Colors["Red"]}disable{Colors["Reset"]} Windows Driver Signature Verification : 
                \t[{Colors["Blue"]}https://answers.microsoft.com/en-us/windows/forum/all/permanent-disable-driver-signature-verification/009c3498-bef8-4564-bb52-1d05812506e0{Colors["Reset"]}]'''
            )
            
            Quit(
                ExceptionName = SystemExit(),
                Message = f'{Colors["Red"]}Cannot Install Correctly{Colors["Reset"]} USB Drivers!'
            )

    def Unlock_Bootloader() -> None: #SHOULD RETURN AN AVAILABLE USB CONNECTION
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

          ---------------------------------------------------

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
        
        if askUser(f'Is "OEM Unlocking" option "{Colors["Grey"]}greyed out{Colors["Reset"]}"?'):
                print(f'[{Colors["Red"]}Great{Colors["Reset"]}!]\nYour phone\'s bootloader has been {Colors["Green"]}unlocked correctly{Colors["Reset"]}!') 
        else:
            print("This means your phone's bootloader hasn't been unlocked correctly!")
            if askUser('Wanna continue anyway?'):
                print(f"[{Colors['Green']}Ok!{Colors['Reset']}]")       #If unlocking bootloader instructions were followed rightly (phone formatted) some devices (like huawei) might not have "OEM Unlocking" greyed out...
            else:
                input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
                raise SystemExit()

    def Install_Heimdall() -> None: #The phone has to be in download mode
        
            
        Download(
            URLink = "https://download1076.mediafire.com/ha3x6kwdi36g/zyge4l2ifk9nxk6/Heimdall.zip",
            FileName = "Heimdall.zip"
        )
        
        ExtractZip(
            Zip_Path = DownloadsFolder + 'Heimdall.zip',
            DestinationPath = ToolsFolder,
            HasFolderInside = False
        )

        os.rename(ToolsFolder + 'Heimdall\\zadig-2.4.exe', ToolsFolder + 'Heimdall\\zadig.exe')

        #This might be a 'USBDriver installation' function
        #TODO : In order to stop doing things multiple times (like drivers installation), create a config file where to store informations about what this program did.
        print(f'{Colors["Green"]}In order to{Colors["Reset"]} setup USB communication, you need to install Samsung drivers {Colors["Green"]}manually{Colors["Reset"]}...')
        print(f'{Colors["Green"]}Rebooting{Colors["Reset"]} Samsung to {Colors["Blue"]}Download Mode{Colors["Reset"]}...')
        os.system('adb reboot download')
        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} if the device is in Download Mode : ")
        print(f'{Colors["Green"]}zadig.exe{Colors["Reset"]} (a Driver installer application) will be executed!')    #TODO : check if zadig reboots pc once driver is installed
        os.startfile(ToolsFolder + 'Heimdall\\zadig.exe')

        print(f'''
Now follow these {Colors["Red"]}instructions{Colors["Reset"]} : 
    1. From the menu chose Options -> {Colors["Green"]}List All Devices{Colors["Reset"]}.

    2. From the USB Device list chose "{Colors["Green"]}Samsung USB Composite Device{Colors["Reset"]}" or "{Colors["Green"]}Gadget Serial{Colors["Reset"]}".

    3. Press "{Colors["Green"]}Install Driver{Colors["Reset"]}", click "{Colors["Green"]}Yes{Colors["Reset"]}" to the prompt and if you receive
    a message about being unable to verify the publisher of the driver
    click "Install this driver software anyway".

        {Colors["Red"]}NOTE{Colors["Reset"]}:    [IF YOU DON'T SEE YOUR DEVICE IN 'Device list' then your device might be unsupported!]

    4. Done!

    5. Close zadig application.
        ''')

        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to continue : ")

    def Download_Firmware() -> None: #Returns "Firmware" folder inside Downloads folder. Inside it there are all .md5 files
        def Download_Status(Status: str):
            #This dict contains all supported firmware regions, there could be a better way to implement this...
            Samsung_Regions: dict(str, list[str]) = {
                'Algeria': ['ALG', 'ALR'],
                'Argentina': ['ANC', 'ARO', 'CTI', 'UFN', 'PSN'],
                'Aruba': ['ARU'],
                'Australia': ['OPP', 'OPS', 'VAU', 'XSA', 'TEL', 'HUT'],
                'Austria': ['AOM', 'DRE', 'MAX', 'MOB', 'MOK', 'ONE', 'TRG', 'ATO'],       
                'Baltic': ['SEB'],
                'Belarus': ['MTB', 'VEL'],
                'Belgium': ['BAE', 'BSE', 'PRO', 'XEB'],
                'Bosnia-Herzegovina': ['BHO', 'BHT', 'TEB'],
                'Brazil': ['BTA', 'BTM', 'TMR', 'ZTA', 'ZVV', 'ZTO', 'ZTM'],
                'Bulgaria': ['CMF', 'GBL', 'MTE', 'MTL', 'OMX', 'PLX', 'VVT'],
                'Cambodia': ['RCG'],
                'Canada': ['RGS', 'BMC', 'TLS'],
                'Chile': ['CHB', 'CHE', 'CHL', 'CHT'],
                'China': ['CUH', 'INT', 'TEC', 'TIY', 'CMC', 'CHN', 'M00'],
                'Colombia': ['COB', 'COL', 'COM', 'CGU'],
                'Costa Rica': ['ICE'],
                'Croatia': ['CRO', 'TRA', 'TWO', 'VIP'],
                'Cyprus': ['CYV'],
                'Czech': ['ETL', 'KBN', 'OSK', 'VDC', 'XCS', 'XEZ', 'TMZ', 'O2C'],
                'Denmark': ['DTL'],
                'Dominica': ['CST', 'DCN', 'DOR'],
                'Dominican Rep': ['CDR', 'TDR'],
                'Ecuador': ['BBE'],
                'Egypt': ['EGY'],
                'El Salvador': ['DGC', 'TBS'],
                'Finland': ['ELS', 'SAU'],
                'France': ['OFR', 'AUC', 'BOG', 'COR', 'DIX', 'FTM', 'NRJ', 'ORC', 'ORF', 'SFR', 'UNI', 'VGF', 'XEF'],
                'Germany': ['DBT', 'DTM', 'DUT', 'EPL', 'MAN', 'MBC', 'VD2', 'VIA', 'XEG'],
                'Ghana': ['SPN'],
                'Greece': ['AOC', 'COS', 'EUR', 'GER', 'TGR', 'VGR', 'CYO'],
                'Guatemala': ['PCS'],
                'Hong Kong': ['TGY'],
                'Hungary': ['PAN', 'VDH', 'WST', 'TMO', 'XEH', 'TMH'],
                'India': ['HFC', 'HYA', 'INA', 'IND', 'INU', 'IMS', 'REL', 'TAT', 'INS'],
                'Indonesia': ['AXI', 'SAR', 'XSE'],
                'Iran': ['THR'],
                'Ireland': ['3IE', 'VDI'],
                'Israel': ['CEL', 'PCL', 'PTR'],
                'Italy': ['GOM', 'HUI', 'ITV', 'OMN', 'TIM', 'VOM', 'WIN', 'XET', 'FWB'],
                'Ivory Coast': ['IRS', 'SIE'],
                'Jamaica': ['JBS', 'JCN', 'JCW'],
                'Japan': ['DCM', 'SBM', 'VFK'],
                'Jordan': ['LEV'],
                'Kazakhstan': ['EST', 'KCL', 'KMB', 'KZK', 'SKZ'],
                'Kenya': ['KEL', 'KEN'],
                'Korea': ['SKT'],
                'Libyan Arab Rep': ['MMC'],
                'Lithuania': ['TLT'],
                'Luxemburg': ['LUX'],
                'Macao': ['VTN'],
                'Macedonia': ['TMC', 'MBM'],
                'Malaysia': ['CCM', 'MXS', 'FMG', 'FME', 'XME'],
                'Mexico': ['SEM', 'TCE', 'TMM', 'UNE'],
                'Mongolia': ['MPC'],
                'Morocco': ['WAN', 'FWD', 'MAT', 'MED', 'SNI', 'MWD'],
                'Netherlands': ['BEN', 'MMO', 'ONL', 'QIC', 'TFT', 'TNL', 'VDF', 'VDP', 'XEN', 'KPN'],
                'New Zealand': ['VNZ'],
                'Nigeria': ['ECT', 'GCR', 'MML'],
                'Norway': ['TEN'],
                'Pakistan': ['WDC', 'PAK'],
                'Panama': ['BPC', 'PCW', 'PBS'],
                'Peru': ['PEB', 'PET', 'SAM'],
                'Philippines': ['FAM', 'XTC', 'GLB', 'XTE', 'SMA'],
                'Poland': ['ERA', 'IDE', 'PLS', 'PRT', 'XEO'],
                'Portugal': ['OPT', 'TMN', 'TPH', 'XEP', 'TCL'],
                'Puerto Rico': ['CEN', 'PCI', 'TPR'],
                'Romania': ['CNX', 'HAT', 'ORO', 'COA'],
                'Russia': ['AZC', 'BLN', 'EMT', 'ERS', 'GEO', 'MTV', 'SER', 'SNT'],
                'Saudi Arabi': ['JED'],
                'Serbia Montenegro': ['MSR', 'PMN', 'SMO', 'TSR', 'TOP'],
                'Singapore': ['BGD', 'XSO', 'XSP'],
                'Slovakia': ['GTL', 'IRD', 'TMS', 'ORS'],
                'Slovenia': ['MOT', 'SIM'],
                'South Africa': ['XFA', 'XFC', 'XFM', 'XFV', 'XFE'],
                'South West Asia': ['SWA'],
                'Spain': ['AMN', 'EUS', 'FOP', 'XEC', 'ATL'],
                'Sweden': ['BAU', 'BCN', 'BME', 'BSG', 'BTH', 'COV', 'HTS', 'SEN', 'TET', 'TLA', 'XEE', 'VDS', 'TNO'],
                'Switzerland': ['AUT', 'ORG', 'MOZ', 'SUN', 'SWC'],
                'Taiwan': ['TWM', 'BRI', 'TCC', 'TCI', 'CWT'],
                'Tanzania': ['SOL'],
                'Temporary': ['TEM'],
                'Thailand': ['CAT', 'THE', 'THL', 'THO', 'THS'],
                'The UAE': ['MID', 'ARB', 'XSG', 'AFR', 'ITO'],
                'The UK': ['BTC', 'O2I', 'O2U', 'ORA', 'TMU', 'TSC', 'VOD', 'XEU', 'VIR', 'H3G', 'CPW'],
                'The USA': ['AWS', 'DOB', 'TMB', 'CLW'],
                'Tunisia': ['ABS', 'RNG'],
                'Turkey': ['BAS', 'KVK', 'TUR', 'TLP', 'TRC'],
                'Ukraine': ['KVR', 'SEK', 'UMC'],
                'Uzbekistan': ['UZB'],
                'Venezuela': ['VMT'],
                'Vietnam': ['XXV', 'PHU', 'XEV', 'DNA', 'FPT', 'SPT', 'TLC', 'VTC', 'VTL']
            }

            def Get_WorkingVersion():   #If the user's phone's region cannot be found inside Samsung Firmware server then we get any available ("wrong" region won't cause any brick)
                for country in Samsung_Regions: #country = 'Algeria'
                    for region in Samsung_Regions[country]: #region = 'ALG' then region = 'ALR'...
                        try: #If the region is found then we get it's version
                            versions = str(
                                subprocess.check_output(
                                    f'samloader -m {Phone.Model} -r {region} checkupdate', 
                                    stderr = subprocess.STDOUT, 
                                    shell = True), 
                                encoding = 'utf-8')[:-2]

                            print(f'Found a downloadable firmware region ["{Colors["Green"]}{country}{Colors["Reset"]}" : {region}]!')
                            Phone.Region = region #Important : change user's phone's region information because this firmware will be flashed on the device...
                            return versions
                        except:
                            print(f'Trying with "{Colors["Grey"]}{region}{Colors["Reset"]}"...'.ljust(150), f'[{Colors["Red"]}Not worked{Colors["Reset"]}!]')
                            pass

                #This is raised if no region has been found, because if found then the execution of this function terminates with the return statement 'return versions'
                Quit(ExceptionName = SystemExit(), Message = f'Cannot find any {Phone.Model} firmware version!') 

            def GetFirmwareVersion() -> str:
                try: #This is the first check : if the region given from adb is not found then samloader raises an Exception, so we check if there is any region available for this device
                    versions = str(
                        subprocess.check_output(
                            f'samloader -m {Phone.Model} -r {Phone.Region} checkupdate', 
                            stderr = subprocess.STDOUT, 
                            shell = True), 
                        encoding = 'utf-8')[:-2]

                except Exception:
                        print(f'{Colors["Red"]}Cannot{Colors["Reset"]} find any version on "{Colors["Green"]}{Phone.Region}{Colors["Reset"]}" Region!')
                        if askUser(f'Do you want to download any other firmware version [{Colors["Green"]}Recommended{Colors["Reset"]}] ?'):
                            versions = Get_WorkingVersion()
                        else:
                            raise SystemExit()
                return versions
            versions = GetFirmwareVersion() if versions not in locals() else versions #This is because Dowload_Status() can be called more times

            if Status == 'New Download':
                try:    #Need to check if some firmwares have .enc2 extension, because if so then samloader will raise an error during decrypting       #Maybe samloader manages it automatically, so no need
                    os.system(f'samloader --dev-model {Phone.Model} --dev-region {Phone.Region} download --fw-ver {versions} --do-decrypt --out-file {DownloadsFolder + "Firmware.zip.enc4"}')
                
                except ConnectionAbortedError:
                    print(f'Your {Colors["Red"]}internet connection{Colors["Reset"]} has been stopped or aborted!\nPlease {Colors["Green"]}check{Colors["Reset"]} your internet connection!')
                    input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} to confirm if your internet connection works : ")
                    
                    if isConnected():
                        Download_Status(Status = 'Resume Downlad')
                    else:
                        raise SystemExit()
                
                except Exception as ex:
                    Quit(ExceptionName = ex(), Message = f'Cannot start or continue {Phone.Model} firmware\'s download for an unknown error!')

            elif Status == 'Resume Download': #This is helpfull when the user gets its firmware file corrupted or stopped cause of internet or keyboard issue
                print(f'{Colors["Green"]}Resuming{Colors["Reset"]} the download...')
                try: #There could be an error here : if the download stops during 'download process' then it will run without issues BUT 
                    #if samloader was decrypting the file and something happens and we resume download then the file extension changes from .zip (changed from .enc4 by samloader during decrypting) then the decryption won't work...
                    os.system(f'samloader --dev-model {Phone.Model} --dev-region {Phone.Region} download --resume --fw-ver {versions} --do-decrypt --out-file {DownloadsFolder + "Firmware.zip.enc4"}')

                except ConnectionAbortedError:
                    print(f'Your internet connection has been stopped or aborted!\nPlease check your internet connection!')
                    input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} to confirm if your internet connection works : ")
                    
                    if isConnected():
                        Download_Status(Status = 'Resume Downlad') 
                    else:
                        raise SystemExit()

                except Exception as ex:
                    Quit(ExceptionName = ex(), Message = f'Cannot start or continue {Phone.Model} firmware\'s download for an unknown error!')
        
        print(f'''
                    [Firmware Downloader] by (@Samloader)
        ''')
        Pip_Installer(Package = 'git+https://github.com/samloader/samloader.git', Package_Name = 'samloader')

        print(f'Your device ({Phone.Model}) is currently running on Android V{Phone.AndroidVersion} and {Phone.PDA} version.\t[Region : {Phone.Region}]\n')
        
        Download_Status('New Download')
        print(f'Firmware has been downloaded correctly!')
        sleep(1)
        
        ExtractZip(
            Zip_FileName = 'Firmware.zip',
            DestinationPath = DownloadsFolder,
            HasFolderInside = False
        )

        if askUser(f'Do you want to delete Firmware.zip to free up disk space in your pc [{Colors["Green"]}Recommended{Colors["Reset"]}] ?'):
            os.remove(f'{DownloadsFolder}Firmware.zip')

    def Firmware_Unpacking() -> None: #Returns a created folder "Extracted_Files" -> Downloads/Firmware/Extracted_Files
        print(f'\n{Colors["Green"]}Unpacking{Colors["Reset"]} Firmware files...')
        def lz4_Extractor(Files_Path: str) -> None:
            #Once the extraction is completed then the file will be in the same directory where it was
            for File in os.listdir(Files_Path):
                if File.endswith('.lz4'):
                    print(f'{Colors["Green"]}Extracting{Colors["Reset"]} {File}')
                    os.system(f'{ToolsFolder}lz4\\lz4.exe f"{Files_Path}\\{File}" -f')
                    os.remove(Files_Path + '\\' + File)

        
        Download(
            URLink = 'https://github.com/lz4/lz4/releases/download/v1.9.4/lz4_win64_v1_9_4.zip', 
            FileName = 'lz4.zip'
        )
        ExtractZip(
            Zip_FileName = 'lz4.zip',
            DestinationPath = ToolsFolder,
            HasFolderInside = True
        )

        for md5 in os.listdir(DownloadsFolder + 'Firmware\\'):
            Extract_tar(
                file_path = DownloadsFolder + 'Firmware\\' + md5, 
                extract_path = DownloadsFolder + f'Firmware\\Extracted_Files\\'
            )

        lz4_Extractor(Files_Path = DownloadsFolder + 'Firmware\\Extracted_Files\\')

    def Firmware_Flashing() -> None: #Need to fix heimdall : Need to know how it actually works : --resume and when --no-reboot...
        def CreateFlashingCommand(ExtractedFirmFiles_Path: str) -> str:
            #How's the pit file : 
            # --- Entry #0 ---
            # Binary Type: 0 (AP)
            # Device Type: 8 (Unknown)
            # Identifier: 80
            # Attributes: 2 (STL Read-Only)
            # Update Attributes: 1 (FOTA)
            # Partition Block Size/Offset: 0
            # Partition Block Count: 1204
            # File Size (Obsolete): 0
            # Partition Name: BOOTLOADER
            # Flash Filename: sboot.bin

            while True:
                Connection = subprocess.check_output('heimdall detect', stderr = True, shell = True)
                if Connection:
                    break
                print(f'{Colors["Red"]}Cannot{Colors["Reset"]} detect device...\nAre you sure that your device is in download mode or is connected to computer?')
                input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to try again the connection : ")

            class Partition:
                def __init__(self, PartitionName, FileName) -> None:
                    self.PartitionName = PartitionName
                    self.FileName = FileName

            PitOutput = subprocess.check_output('heimdall print-pit --no-reboot', cwd = ToolsFolder + 'Heimdall\\', stderr = subprocess.STDOUT, shell = True) #encoding might be needed
            lines = [[line.rstrip() for line in PitOutput]]

            Partitions = list()

            for line in lines:
                if 'Partition Name' in PreviousLine:
                    PartitionName = line.split(': ')[1] #Partition Name: BOOTLOADER

                if 'Flash Filename' in line: #Flash Flename: sboot.bin
                    Partitions.append(Partition(PartitionName, FileName = line.split(': ')[1]))
                PreviousLine = line

            FilesInDirectory = [f for f in os.listdir(ExtractedFirmFiles_Path) if os.path.isfile(os.join(ExtractedFirmFiles_Path, f))]

            for Part in Partitions:
                if Part.FileName not in FilesInDirectory: #Checking whatever device's partition's file exists
                    Partitions.remove(Part)

            Command = 'heimdall flash --resume '
            for Part in Partitions:
                Command += f' --{Part.PartitionName} {Part.FileName}'

            return Command


        Check_AdbConnection(DriversInstaller=Install_SamsungUSBDrivers)
        os.system('adb reboot download')
        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} if your phone is in {Colors['Blue']}Download Mode{Colors['Reset']} : ")
        #Need to use heimdall detect        #TODO: Check heimdall commands' output
        Heimdall_Command = CreateFlashingCommand()
        print(f'\n\n{Colors["Green"]}Starting{Colors["Reset"]} Flashing process...')
        os.system(Heimdall_Command)
        #Check if need to reboot or not!
        print(f'\n\n[{Colors["Green"]}Finished Flashing{Colors["Reset"]}!]')

    def Patch_AP_File() -> None: #Returns a folder in Firmware's folder called 'PatchedFiles'
        #Possible CPU Architectures : x86_64, x86, arm64-v8a or armeabi-v7a
        if not Phone.CPU_Architecture in ['x86_64', 'x86', 'arm64-v8a', 'armeabi-v7a']:
            Quit(
                ExceptionName = SystemExit(),
                Message = 'Your phone\'s CPU architecture is not supported!\nCannot patch your Firmware\'s images!'
                )

        Download(
            URLink = 'https://download851.mediafire.com/ob36tz7hyqsg/h71rwovkstiyiyf/MagiskBinaries.zip',
            FileName = 'MagiskBinaries.zip'
            )
        ExtractZip(
            Zip_FileName = 'MagiskBinaries.zip',
            DestinationPath = ToolsFolder,
            HasFolderInside = False
            )
        
        print(f'\n\n\t[Now it\'s time to patch {Colors["Green"]}Firmware Binaries{Colors["Reset"]} in order to root your device!]\n')
        OutFolder = f'/data/local/tmp/{Phone.CPU_Architecture}/'
        FilePath = ToolsFolder + 'MagiskBinaries'

        print(f'{Colors["Green"]}Sending{Colors["Reset"]} Magisk Binaries to {OutFolder}'.ljust(150), end = '')
        subprocess.check_output(f'adb push {FilePath}\\{Phone.CPU_Architecture}\\ /data/local/tmp/', stderr=subprocess.STDOUT, shell = True)
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
        # if Phone.IsEncrypted == 'encrypted':      #This is quite optional as if not given then boot_patch.sh COULD remove the encryption from the device... it's just Android security options... (Mind if need a TWRP)
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

    def Setup_MagiskManager() -> None:
        pass


    print(
        f'{Colors["Green"]}Installing{Colors["Reset"]} Samsung requirements...'
    )

    Install_AdbFastboot()
    SetupDeviceForUSBCommunication()
    Check_AdbConnection(DriversInstaller=Install_SamsungUSBDrivers)
    Unlock_Bootloader()
    Check_AdbConnection(DriversInstaller=Install_SamsungUSBDrivers)
    Download_Firmware()
    Firmware_Unpacking()
    Install_Heimdall()
    Firmware_Flashing()
    SetupDeviceForUSBCommunication()
    Check_AdbConnection(DriversInstaller=Install_SamsungUSBDrivers)
    Patch_AP_File()
    os.system(f'mv {DownloadsFolder}Firmware\\ExtractedFiles\\boot.img {DownloadsFolder}Firmware\\ExtractedFiles\\sotck_boot.img')
    os.system(f'mv {DownloadsFolder}Firmware\\PatchedFiles\\new-boot.img {DownloadsFolder}Firmware\\ExtractedFiles\\boot.img')
    os.system(f'adb reboot download')
    Firmware_Flashing()
    SetupDeviceForUSBCommunication()
    Setup_MagiskManager()


    #TODO: Create a Firmware donload function and give the user 2 options : update to latest firmware (Need to flash it before patching) or run on current firmware (need PDA and CSS codes)
