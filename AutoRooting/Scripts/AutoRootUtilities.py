
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


os.mkdir("Tools", "Downloads", exist_ok = True)


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
        subprocess.run([sys.executable, '-m', 'pip', 'install', Package], check=True)
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
    with tarfile.open(file_path, "w") as tar:
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
        print(f'{Colors["Green"]}Adding{Colors["Reset"]} {Directory} to the {Colors["Green"]}User Environment{Colors["Reset"]} Path Temporally...', end = '')
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
        if os.path.getsize(DownloadsFolder + FileName) == 0:
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


# Gets zip file name and extracts its contents inside a path : Zip_FileName = 'Ajk.zip', DestinationPath = DownloadsFolder -> inside DownloadsFlder will be extracted all files
def ExtractZip(Zip_FileName: str, Zip_Path: str, DestinationPath: str):
    DestinationPath += Zip_FileName[:-4]
    try:
        if os.path.getsize(DownloadsFolder + Zip_FileName) == 0:
            os.remove(DownloadsFolder + Zip_FileName)

        if Zip_FileName[:-4] in os.listdir(ToolsFolder):
            return
    except:
        pass

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
        Zip_Path = DownloadsFolder + "platform-tools.zip",
        DestinationPath = ToolsFolder
    )
    print(
        f"{Colors['Red']}Removing{Colors['Reset']} platform-tools.zip",
        end = ''
    )
    os.remove('Downloads\\plattools.zip')

    print(f'[{Colors["Green"]}Done{Colors["Green"]}!]')

    AddToEnvironmentPath(ToolsFolder)

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
    return True
    
    
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
    def Install_SamsungUSBDrivers(InstallationStatus: bool = True):
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



    def Download_Firmware():
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
                            print(f'Trying with "{Colors["Grey"]}{region}{Colors["Reset"]}"... \t[{Colors["Red"]}Not worked{Colors["Reset"]}!]')
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
            versions = GetFirmwareVersion() if versions not in locals() else versions

            if Status == 'New Download':
                try:    #Need to check if some firmwares have .enc2 extension, because if so then samloader will raise an error during decrypting
                    os.system(f'samloader --dev-model {Phone.Model} --dev-region {Phone.Region} download --fw-ver {versions} --do-decrypt --out-file {DownloadsFolder + "Firmware.zip.enc4"}')
                
                except ConnectionAbortedError:
                    print(f'Your {Colors["Red"]}internet connection{Colors["Reset"]} has been stopped or aborted!\nPlease {Colors["Green"]}check{Colors["Reset"]} your internet connection!')
                    input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} to confirm if your internet connection works : ")
                    
                    if isConnected():
                        Download_Status(Status = 'Resume Downlad')
                    else:
                        raise SystemExit()
                
                except Exception as ex:
                    Quit(ExceptionName = SystemExit(), Message = f'Cannot start or continue {Phone.Model} firmware\'s download for an unknown error!')

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
                    Quit(ExceptionName = SystemExit(), Message = f'Cannot start or continue {Phone.Model} firmware\'s download for an unknown error!')
        
        print(f'''
                    [Firmware Downloader] by (@Samloader)
        ''')
        Pip_Installer(Package = 'git+https://github.com/samloader/samloader.git', Package_Name = 'samloader')

        print(f'Your device ({Phone.Model}) is currently running on Android V{Phone.AndroidVersion} and {Phone.PDA} version.\t[Region : {Phone.Region}]\n')
        
        Download_Status('New Download')
        print(f'Firmware has been downloaded correctly!')
        sleep(sleepDelay)
        
        ExtractZip(
            Zip_FileName = 'Firmware.zip',
            Zip_Path = DownloadsFolder + 'Firmware.zip',
            DestinationPath = DownloadsFolder + 'Firmware\\'
        )

        if askUser(f'Do you want to delete Firmware.zip to free up disk space in your pc [{Colors["Green"]}Recommended{Colors["Reset"]}] ?'):
            os.remove(f'{DownloadsFolder}Firmware.zip')

    def Unlock_Bootloader(): #SHOULD RETURN AN AVAILABLE USB CONNECTION
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
                input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
                raise SystemExit()

    def Install_Odin(): #Just ask the user to accept to download odin under his responsability and let the program do all automatic process
        DownloadPath = os.listdir(DownloadsFolder)
        DownloadPathFolder = os.startfile(DownloadsFolder)
        if 'Odin3_v3.14.4.exe' in DownloadPath:
            return

        if askUserForChoice(f'''
Flashing {Colors["Green"]}latest{Colors["Reset"]} downloaded firmware is {Colors["Green"]}ESSENTIAL to avoid{Colors["Reset"]} phone soft-brick!
{Colors["Green"]}AutoRoot{Colors["Reset"]} program is {Colors["Green"]}not legally allowed{Colors["Reset"]} to distribuite Odin.exe tool (Firmware Flasher)!
You will have to download the software manually and voluntarily accept AutoRoot's use of Odin.exe!
This program is not forcing your in any way to download this tool!

\t{Colors["Red"]}By typing "YES I CONFIRM" you accept what said above, else type "NO I DON'T CONFIRM"{Colors["Reset"]} : ''',
            Choice1 = 'YES I CONFIRM',
            Choice2 = 'NO I DON\'T CONFIRM'
):
            print(
                f'''
    Here is the link to download Odin.exe : [{Colors["Blue"]}https://odindownload.com/download/Odin3_v3.14.4.zip{Colors["Reset"]}]',
    Make sure to {Colors["Red"]}Extract{Colors["Reset"]} the zip file and move all the files extracted into the right folder :',
        [{Colors["Green"]}SS_DL.dll{Colors["Reset"]}]             ───┐
        [{Colors["Green"]}Odin3.ini{Colors["Reset"]}]             ───┫______   [{Colors["Green"]}{DownloadsFolder}{Colors["Reset"]}]
        [{Colors["Green"]}Odin3_v3.14.4.exe{Colors["Reset"]}]     ───┫
        [{Colors["Green"]}cpprest141_2_10.dll{Colors["Reset"]}]   ───┘'''
            )
            os.startfile(DownloadPathFolder)
            input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} to confirm that you mooved these files : ")
            DownloadPath = os.listdir(DownloadsFolder)
            if 'Odin3_v3.14.4.exe' not in DownloadPath:
                print(f'\t{Colors["Red"]}Cannot{Colors["Reset"]} find Odin3_v3.14.4.exe in {DownloadPathFolder}')
                print('Make sure that you installed Odin V3.14.4 and that it is inside the given path!')
                Install_Odin()

    def Firmware_Flashing(Patch: bool):
        def BetterOutput(text: str):
            for line in text:
                print(f'   {Colors["Green_Highlight"]}{line}{{Colors["Reset"]}}')

        Install_Odin()
        if askUserForChoice(f'''
    Do you want to {Colors["Red"]}flash{Colors["Reset"]} the firmware {Colors["Red"]}manually{Colors["Reset"]} with a detailed guide on how to do it [{Colors["Green"]}Recommended{Colors["Reset"]}] 
                                            OR
    {Colors["Red"]}Let{Colors["Reset"]} AutoRoot.py flash it automatically [{Colors["Red"]}Might be instable{Colors["Reset"]}] ?''',
    Choice1 = 'Manual', #True
    Choice2 = 'Automatic' #False
        ):

            print(f'\t[You choosed {Colors["Green"]}Manual{Colors["Reset"]} Method!]')
            print(f'Now open Odin program with {Colors["Green"]}Administrator rights{Colors["Reset"]} and click {Colors["Green"]}Ok{Colors["Reset"]}!')

            os.startfile(os.startfile(DownloadsFolder))
            input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} to continue : ")

            Check_AdbConnection()
            print('Rebooting Samsung to Download Mode...')
            os.system('adb reboot download')
            sleep(5)

            if not askUser(f'Now you shold be able to see, for example, [{Colors["Red"]}<ID:0/003> Added!!{Colors["Reset"]}], right?'):
                print('If the phone is in download mode and is connected to the computer via USB cable then the only problem could be USB Drivers...')
                Install_SamsungUSBDrivers()
                Firmware_Flashing()

            print(f'{Colors["Red"]}Perfect{Colors["Reset"]}!\nNow we are going to upload firmware files : ')
            global AP_File #TODO : Check if this works
            AP_File = find_files(root_dir = os.getcwd() + '\\Downloads\\Firmware\\', extension = 'md5', file_name='AP_')[0]

            if Patch:
                AP_File = DownloadsFolder + 'Firmware\\AP_Patched.tar'

            print(f'''
Now click on :                  [{Colors["Red"]}Might take 1-2 minutes{Colors["Reset"]}]
    - {Colors["Red"]}BL{Colors["Reset"]} and choose : {find_files(root_dir = DownloadsFolder + 'Firmware//', extension = 'md5', file_name = 'BL_')[0]}
    - {Colors["Red"]}AP{Colors["Reset"]} and choose : {AP_File}
    - {Colors["Red"]}CP{Colors["Reset"]} and choose : {find_files(root_dir = DownloadsFolder + 'Firmware//', extension = 'md5', file_name = 'CP_')[0]}
    - {Colors["Red"]}CSC{Colors["Reset"]} and choose : {find_files(root_dir = DownloadsFolder + 'Firmware//', extension = 'md5', file_name = 'CSC_')[0]}
            ''')

            input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} to continue : ")
            print(f'Now click on {Colors["Green"]}Start{Colors["Reset"]} button to start flashing\nYou should now see a similar output to this : ')
            text = '''
    <ID:0/003>Added!!
    <OSM>Enter CS for MD5..
    <OSM>CheckMD5.. Do not unplug the cable..
    <OSM>Please wait..
    <OSM>Checking MD5 finised Sucessfully..
    <OSM>Leave CS..
    <ID:0/003>Odin engine v(ID:3.14.4)
    <ID:0/003>File analysis..
    <ID:0/003>Total Binary size: 6593M
    <ID:0/003>SetupConnection..
    <ID:0/003>Initialization..
    <ID:0/003>Set PIT file..
    <ID:0/003>DO NOT TURN OFF TARGET!!!
    <ID:0/003>Get PIT for mapping..
    <ID:0/003>Firmware update start..
    <ID:0/003>NAND Write Start!!
    <ID:0/003>SingleDownload.
    <ID:0/003>sboot.bin
    <ID:0/003>param.bin
    <ID:0/003>up_param.bin
    <ID:0/003>cm.bin
    <ID:0/003>keystorage.bin
    <ID:0/003>boot.img
    <ID:0/003>recovery.img
    <ID:0/003>system.img
    <ID:0/003>vendor.img
    <ID:0/003>dt.img
    <ID:0/003>dtbo.img
    <ID:0/003>vbmeta.img
    <ID:0/003>modem.bin
    <ID:0/003>modem_debug.bin
    <ID:0/003>product.img
    <ID:0/003>RQT_CLSE!!
    <ID:0/003>RES OK!!
    <ID:0/003>Remomved!!
    <ID:0/003>Remain Port .... 0
    <OSM> All Threads completed. (succeed 1 / failed 0)
'''
            BetterOutput(text)
            input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} if the firmware has been flashed successfully [<OSM> All Threads completed. (succeed 1 / failed 0)] : ")
            print(f'\nNow {Colors["Red"]}Press and Hold{Colors["Reset"]} down volume down and power keys untill phone reboots')
            sleep(6)
            print(f'Now you device should be updated to {Phone.AndoidVersion} Android version!\nNow you have to configure Welcome screen, setup WI-FI and enable again developer options...')
            
            input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to show how to enable Developer options and USB Communication : ")
            SetupDeviceForUSBCommunication()
            
            input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to continue : ")
            Check_AdbConnection()






        else:
            print(f'You choosed {Colors["Red"]}Automatic{Colors["Reset"]} Method!')
            Pip_Installer(Package = 'Pywinauto')
            sleep(sleepDelay)
            import pywinauto

    
    def Firmware_Unpacking():
        def lz4_Extractor(File: str):
            #Once the extraction is completed then the file will be in the same directory where it was
            Download(
                URLink = 'https://github.com/lz4/lz4/releases/download/v1.9.4/lz4_win64_v1_9_4.zip', 
                FileName = 'lz4.zip'
            )
            ExtractZip(
                Zip_FileName = 'lz4.zip',
                Zip_Path = DownloadsFolder + 'lz4.zip',
                DestinationPath = ToolsFolder
            )
            os.system(f'{ToolsFolder}lz4\\lz4.exe {File}')

        

        Extract_tar(
            file_path = AP_File, 
            extract_path = DownloadsFolder + 'Firmware\\Extracted_AP'
        )

        Boot_File: str = find_files(
            root_dir = DownloadsFolder + 'Firmware\\Extracted_AP\\',
            extension = 'lz4',
            NoExtension = True, 
            file_name = 'boot'
        )[0]

        Recovery_File: str = find_files(
            root_dir = DownloadsFolder + f'Firmware\\Extracted_AP\\',
            extension = 'lz4',
            NoExtension = True, 
            file_name = 'recovery'
        )[0]

        if Boot_File.endswith('.lz4'):
            lz4_Extractor(File = Boot_File)
            Boot_File = Boot_File[:-4] #boot.img.lz4 -> boot.img
        
        if Recovery_File.endswith('.lz4'):
            lz4_Extractor(File = Recovery_File)
            Recovery_File = Recovery_File[:-4]


        


    def Patch_AP_File(): #TODO : Create an autopatching script by using magisk manager native binaries :    
        print('Now it\'s time to patch Firmware Binaries in order to root your device!')
        print('Installing Magisk Manager on your phone...')
        FilePath = os.getcwd() + '\\Downloads\\Magisk.apk'
        os.system(f'adb install {FilePath}') #There might be installation errors like 'unknown surces' not allowed
        FilePath = os.getcwd() + '\\Downloads\\Firmware\\' + AP_File
        print(f'Sending {AP_File} to /Storage/emulated/0/Download/', end = '')
        os.system(f'adb push {FilePath} /Storage/emulated/0/Download/') #need to Implement progress bar
        print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')
        print('Now search for Magisk application on your phone and open it')
        print('Now click on first "Install" button (near to "Magisk" name) and allow magisk to access phone\'s storage')
        print('') #Here will be all explaination of Magisk patching methods (Patch vbmeta in boot image etc)
        

    print(
        f'{Colors["Green"]}Installing{Colors["Reset"]} Samsung requirements...'
    )

    Install_AdbFastboot()
    Download_Magisk()

    #TODO: Create a Firmware donload function and give the user 2 options : update to latest firmware (Need to flash it before patching) or run on current firmware (need PDA and CSS codes)
