#Copyright (C) <2023> by <Quantum>

class Phones:
    def __init__(self) -> None:
        self.CPU_Architecture = 'arm64-v8a'
        self.BuildNumber = 'TD1A.220804.009.A2'
        self.Product = 'panther'

Device = Phones()

from Utilities import Colors, Download, ExtractZip, Quit, DownloadsFolder, requests, Check_FastbootConnection, subprocess, sleep, GetFileName_FromZip, askUser, SetupDeviceForUSBCommunication, Patch_Image_File, ConfigureMagisk, Download_Magisk
import os
from bs4 import BeautifulSoup




def Download_Firmware() -> None:
        """
        This function downloads latest stock firmware into DownloadsFolder\\Firmware 
        and extracts boot.img into Firmware\\Extracted_Files
    
         -> Returns an available Adb Connection! 
        """
        
        #Build numeber is essential to download the correct current version, else need to update to latest versin possible which require more steps (line 4)
        print(f'{Colors["Green"]}Looking{Colors["Reset"]} for {Device.BuildNumber} Firmware version...'.ljust(150), end = '')

        URL = "https://developers.google.com/android/images"
        session = requests.session()
        session.cookies.set("devsite_wall_acks", "nexus-image-tos") #Cookie added to 'bypass' Google TOS. Need to work on this if it's accepted by google or not...
        
        response = session.get(URL)

        
        if response.status_code != 200:
            Quit(
                ExceptionName = SystemExit(),
                Message = r'\nCannot open a HTTP request on https://developers.google.com/android/ota for unknown reason!'
            )
        # Parsing del HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Search for all tags 'a'
        for line in soup.find_all('a'):
            try:
                # Getting link from the tag if it's present, else do not add anything
                link = str(line).split('href="')[1].split('">')[0].strip() # https://dl.google.com/dl/android/aosp/cheetah-td1a.220804.009.a2-factory-8e7393e1.zip
                # Only '.zip' links can be added to the list, they are direct download link
            except:
                pass

            if Device.BuildNumber.lower() in link and Device.Product.lower() in link:
                print(f'[{Colors["Green"]}Found{Colors["Reset"]}!]')
                Download(
                    URLink = link,
                    FileName = 'Firmware.zip'
                )
                ExtractZip(
                    Zip_FileName = 'Firmware.zip',
                    DestinationPath = DownloadsFolder,
                    HasFolderInside = True,
                    Rename = True
                )
                Images_Folder = [Image_Zip for Image_Zip in os.listdir(DownloadsFolder + 'Firmware\\') if Image_Zip.endswith('.zip')][0]
                try:
                    os.mkdir(DownloadsFolder + 'Firmware\\Extracted_Files')
                except:
                    pass

                global BootImage_Name
                BootImage_Name = 'init_boot.img' if GetFileName_FromZip(Zip_Path = DownloadsFolder + f'Firmware\\{Images_Folder}', FileName = 'init_boot.img') else 'boot.img'
                ExtractZip(
                    Zip_FileName = f'Firmware\\{Images_Folder}',
                    SpecificFile = BootImage_Name,
                    DestinationPath = DownloadsFolder + 'Firmware\\Extracted_Files',
                    HasFolderInside = True
                )
                global BootImage_Path
                BootImage_Path = DownloadsFolder + f'Firmware\\Extracted_Files\\{BootImage_Name}'

                return
        else:
            Quit(
                ExceptionName = SystemExit(),
                Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} find any firmware version for {Device.BuildNumber} version!'
            )

def Firmware_Flashing(Root: bool = False) -> None:
    """
    This function flashes latest stock firmware and logs all in Logs\GPFlashing_log.txt file.
    Once the flashing has been complete the phone won't reboot but, if 'Root' variable is True, it will also flash patched_boot.img file.
    
        -> Returns an available Adb Connection! 
    """

    Check_FastbootConnection()
    print(f'{Colors["Red"]}Starting{Colors["Reset"]} flashing process...')

    for file in os.listdir(DownloadsFolder + 'Firmware'):
        Bootloader_File = file if 'bootloader' in file else ''
        Radio_File = file if 'Radio' in file else ''
        Image_Zip = file if file.endswith('.zip') else ''

    with open(f'{os.getcwd()}\\Logs\\GPFlashing_log.txt', 'w') as FLog:
        #Flashing bootloader partition
        print(f'{Colors["Red"]}Flashing{Colors["Reset"]} bootloader partition...')
        Bootloader_Flashing = str(subprocess.check_output(f'fastboot flash bootloader {Bootloader_File}', stderr = subprocess.STDOUT, shell = True), encoding='utf-8')
        FLog.write(f'Command: fastboot flash bootloader {Bootloader_File}')
        FLog.write(f'Output: \n{Bootloader_Flashing}')
        if 'FAILED' in Bootloader_Flashing:
            Quit(
                ExceptionName = SystemExit(),
                Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} flash bootloader partition for unknown reason!\n{Colors["Red"]}Something went wrong{Colors["Reset"]} on flashing it!\nYour phone might be {Colors["Red"]}soft bricked{Colors["Reset"]}!\nPlease, {Colors["Red"]}contact{Colors["Reset"]} support on github!'
            )
        
        print(f'{Colors["Green"]}Rebooting{Colors["Reset"]} into bootloader...')
        FLog.write('Rebooting: fastboot reboot-bootloader')
        subprocess.check_output('fastboot reboot-bootloader', stderr = subprocess.STDOUT, shell = True)
        sleep(6)
        
        #Flashing radio partition
        print(f'{Colors["Red"]}Flashing{Colors["Reset"]} radio partition...')
        Radio_Flashing = str(subprocess.check_output(f'fastboot flash radio {Radio_File}', stderr = subprocess.STDOUT, shell = True), encoding='utf-8')
        FLog.write(f'Command: fastboot flash radio {Radio_File}')
        FLog.write(f'Output: \n{Radio_Flashing}')
        if 'FAILED' in Radio_Flashing:
            Quit(
                ExceptionName = SystemExit(),
                Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} flash radio partition for unknown reason!\n{Colors["Red"]}Something went wrong{Colors["Reset"]} on flashing it!\nYour phone might be {Colors["Red"]}soft bricked{Colors["Reset"]}!\nPlease, {Colors["Red"]}contact{Colors["Reset"]} support on github!'
            )
        
        print(f'{Colors["Green"]}Rebooting{Colors["Reset"]} into bootloader...')
        FLog.write('Rebooting: fastboot reboot-bootloader')
        subprocess.check_output('fastboot reboot-bootloader', stderr = subprocess.STDOUT, shell = True)
        sleep(6)
        
        #Flashing All Images partitions
        print(f'{Colors["Red"]}Flashing{Colors["Reset"]} firmware partitions...')
        Image_Flashing = str(subprocess.check_output(f'fastboot update {Image_Zip}', stderr = subprocess.STDOUT, shell = True), encoding='utf-8')
        FLog.write(f'Command: fastboot update {Image_Zip}')
        FLog.write(f'Output: \n{Image_Flashing}')
        if 'FAILED' in Image_Flashing:
            Quit(
                ExceptionName = SystemExit(),
                Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} flash radio partition for unknown reason!\n{Colors["Red"]}Something went wrong{Colors["Reset"]} on flashing it!\nYour phone might be {Colors["Red"]}soft bricked{Colors["Reset"]}!\nPlease, {Colors["Red"]}contact{Colors["Reset"]} support on github!'
            )

        print(f'{Colors["Green"]}Rebooting{Colors["Reset"]} into bootloader...')
        FLog.write('Rebooting: fastboot reboot-bootloader')
        subprocess.check_output('fastboot reboot-bootloader', stderr = subprocess.STDOUT, shell = True)
        sleep(6)
        
        #Flashing patched_boot.img partition
        if Root:
            Patched_ImagePath = DownloadsFolder + f'Firmware\\Extracted_Files\\{BootImage_Path}'
            print(f'{Colors["Red"]}Flashing{Colors["Reset"]} {BootImage_Path} {BootImage_Path} partition with the patched_boot.img file...')
            Patch_Flashing = str(subprocess.check_output(f'fastboot flash {Patched_ImagePath[:-4]} {Patched_ImagePath}', stderr = subprocess.STDOUT, shell = True), encoding='utf-8')
            FLog.write(f'Command: fastboot flash {Patched_ImagePath[:-4]} {Patched_ImagePath}')
            FLog.write(f'Output: \n{Patch_Flashing}')
            if 'FAILED' in Patch_Flashing:
                Quit(
                    ExceptionName = SystemExit(),
                    Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} flash patched  partition for unknown reason!\n{Colors["Red"]}Something went wrong{Colors["Reset"]} on flashing it!\nYour phone might be {Colors["Red"]}soft bricked{Colors["Reset"]}!\nPlease, {Colors["Red"]}contact{Colors["Reset"]} support on github!'
                )
        
        print(f'\t{Colors["Green"]}Successfully{Colors["Reset"]} flashed stock partition!')
        FLog.write(f'Successfully flashed stock partition!')
        print(f'{Colors["Green"]}Rebooting{Colors["Reset"]} phone normally...\nIt should take 1-3 minutes to boot.')
        FLog.write('Rebooting: fastboot reboot')
        subprocess.check_output('fastboot reboot', stderr = subprocess.STDOUT, shell = True)
        sleep(6)

        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} if your phone has been rebooted and it\'s in the home screen: ")
        print(f'{Colors["Red"]}Now{Colors["Reset"]} enable again "USB debugging" option in Developer options')
        if askUser(f"{Colors['Green']}Forgot{Colors['Reset']} how to enable 'USB debugging'?"):
            SetupDeviceForUSBCommunication()
        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} if you have enabled 'USB debugging' : ")
        Check_FastbootConnection()
        
        ConfigureMagisk()

#Need to do Patching process : patching init_boot.img or boot.img and rename the patched into the same name of boot.img and replace it into Firmware\\Extracted_Files
# BootImage_Path = DownloadsFolder + f'Firmware\\Extracted_Files\\init_boot.img'
# BootImage_Name = 'init_boot.img'
# Patch_Image_File(Device = Device, BootImage_Name = BootImage_Name)
# print('Downloading...', end = '\n')
# print('\rProgress: ...', end = '')
# # print('\r\b\rDone!')





print(f'''
    
1. {Colors["Red"]}Now{Colors["Reset"]} Magisk Manager will ask you, throught a pop-up, to install {Colors["Green"]}Additional Setup{Colors["Reset"]} like this :
                        {Colors["White_Highlight"]}{Colors["Grey"]} Requires Additional Setup {Colors["Reset"]}
            {Colors["White_Highlight"]} Your device needs additional setup for Magisk to {Colors["Reset"]} 
            {Colors["White_Highlight"]} work properly. Do you want to proceed and reboot? {Colors["Reset"]}
            
                                            {Colors["Cyan"]} CANCEL {Colors["Reset"]}      {Colors["Cyan"]} OK {Colors["Reset"]}
    ''')
