#Copyright (C) <2023> by <Quantum>

class Phones:
    def __init__(self) -> None:
        self.Model = 'OnePlus 9 Pro'
        self.CPU_Architecture = 'arm64-v8a'
        self.BuildNumber = '11.2.10.10.LE15DA'
        self.Product = 'panther'

Device = Phones()

from Utilities import *
# Pip_Installer(Package = 'webdriver-manager selenium pandas', Package_Name = 'webdriver-manager, selenium and pandas')
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup



def Download_Firmware() -> None:
    """
    This function downloads latest stock firmware into DownloadsFolder\\Firmware 
    and extracts boot.img into Firmware\\Extracted_Files

        -> Returns an available Adb Connection!
    """
    
    #Build number is essential to download the correct current version, else need to update to latest versin possible which require more steps
    
    def Get_DownloadLink() -> str:
        URL = "https://xiaomifirmwareupdater.com/miui/excalibur/stable/V13.0.2.0.SJXINXM/" #This download page must exists, if not then cannot download firmware version.
        session = requests.session()
        response = session.get(URL)

        
        if response.status_code != 200:
            Quit(
                ExceptionName = SystemExit(),
                Message = f'\n{Colors["Red"]}Cannot{Colors["Reset"]} open a HTTP request on {URL} for unknown reason!\nMaybe the website is {Colors["Red"]}offline{Colors["Reset"]} or doesn\' exists!'
            )
        # Parsing del HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        for line in soup.find_all('h5'):
            try:
                # Normally, the direct download link is something like : 'https://bigota.d.miui.com/V13.0.7.0.SMQINXM/sunstone_in_global_images_V13.0.7.0.SMQINXM_20230210.0000.00_12.0_in_17133dc219.tgz'
                # And the tag is : 
                # <button type="button" id="download" class="btn btn-primary" style="margin: 7px;" 
                # onclick="if (!window.__cfRLUnblockHandlers) return false; window.open('https://bigota.d.miui.com/V13.0.2.0.SJXINXM/excalibur_in_global_images_V13.0.2.0.SJXINXM_20221109.0000.00_12.0_in_2455ff95e7.tgz', '_blank');">
                link = str(line).split('window.open(\'')[1].split("', '")[0].strip()
                if link.endswith('.tgz'): # .tgz file extension is the Fastboot Firmware type (Which includes all system files), while .zip is for Recovery Firmware type (Which includes files for an update. It doesn't contain boot.img)
                    return link
                # Only '.zip' links can be added to the list, they are direct download link
            except:
                pass
        else: #TODO: Maybe, if tgz doesn't exists, try to download Recovery.zip which should contain boot.img
            Quit(
                ExceptionName = SystemExit(),
                Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} find any firmware version for {Device.BuildNumber} version!'
            )
        
    
    print(f'{Colors["Green"]}Looking{Colors["Reset"]} for {Device.BuildNumber} Firmware version...'.ljust(150), end = '')
    link = Get_DownloadLink()
    print(f'[{Colors["Green"]}Found{Colors["Reset"]}!]')
    Download(
        URLink = link,
        FileName = 'Firmware.tgz'
    )

    # There are 3 different firmware type : 
    # payload.bin in the root dir which contains all images. Need to extract using Payload-dumper
    # boot.img in the root dir -> just extract it
    # flash_all.bat in the root dir and boot.img in the images folder
    ExtractZip(
        Zip_FileName = 'Firmware.tgz',
        DestinationPath = DownloadsFolder,
        HasFolderInside = True,
        Rename = True
    )

    if CheckFile(Filename = 'payload.bin', Directory = DownloadsFolder + 'Firmware'):
        SpecificFile = 'payload.bin'
    elif CheckFile(Filename = 'boot.img', Directory = DownloadsFolder + 'Firmware\\images'):
        SpecificFile = 'images\\boot.img'
    elif CheckFile(Filename = 'boot.img', Directory = DownloadsFolder + 'Firmware'):
        SpecificFile = 'boot.img'
    else:
        Quit(
            ExceptionName = SystemExit(),
            Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} find boot.img file inside Firmware folder!'
        )
        
    if SpecificFile == 'payload.bin':
        Download(
            URLink = 'https://codeload.github.com/QuantumNone/Payload_Dumper/zip/refs/heads/master',
            FileName = 'Payload-Dumper.zip'
        )
        ExtractZip(
            Zip_FileName = 'Payload-Dumper.zip',
            DestinationPath = ToolsFolder,
            HasFolderInside = True
        )
        
        Pip_Installer(Package = 'protobuf==3.20.1')
        Pip_Installer(Package = 'six')
        Pip_Installer(Package = 'bsdiff4')
        
        print(f'\n{Colors["Green"]}Extracting{Colors["Reset"]} Firmware images from payload.bin : \n')
        os.system(f'{sys.executable} {ToolsFolder}payload_dumper-master\\payload_dumper.py {DownloadsFolder}Firmware\\payload.bin --out {DownloadsFolder}Firmware\\Extracted_Files')
        print(f'{Colors["Reset"]}{Colors["Red"]} -> {Colors["Reset"]}[{Colors["Green"]}Done{Colors["Reset"]}!]\n')

    else:
        print(f'{Colors["Green"]}Mooving{Colors["Reset"]} boot.img into Extracted_Files folder...'.ljust(150), end = '')
        if not os.path.isdir(DownloadsFolder + 'Firmware\\Extracted_Files'):
            os.mkdir(DownloadsFolder + 'Firmware\\Extracted_Files')
        # os.replace(DownloadsFolder + f'Firmware\\{SpecificFile}', DownloadsFolder + 'Firmware\\Extracted_Files\\boot.img')
        shutil.copy(src = DownloadsFolder + f'Firmware\\{SpecificFile}', dst = DownloadsFolder + 'Firmware\\Extracted_Files')
        print(f'[{Colors["Green"]}Done{Colors["Reset"]}!]')

    Check_AdbConnection(AdbOrFastboot = 'Adb')

Download_Firmware()
# SearchFile_inZip(FileName = 'boot.img', Zip_path = DownloadsFolder + 'Firmware.tgz')

# def SearchFile_inZip(FileName: str, Zip_path: str) -> str:
#     """This researches a specific FileName inside a zip file and if it's present, it returns the path of the file."""
#     if Zip_path.endswith('.tgz'): #Reading large and COMPRESSED archives takes lot of time (30 seconds normally)
#         from tarfile import open as Topen
#         with Topen(Zip_path, 'r:gz') as zipFile:
#             for member in zipFile.getmembers():
#                 print(member)
#                 if member.isfile():
#                     if member.name == FileName:
#                         print(member.name)
        
