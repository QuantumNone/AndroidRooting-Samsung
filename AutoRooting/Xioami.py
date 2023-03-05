#Copyright (C) <2023> by <Quantum>
from Scripts.Utilities import *
from bs4 import BeautifulSoup

def Xioami_Requirements(Device: object):

    def Install_XioamiUSBDrivers():
        Install_AdbDrivers()

    def Unlock_Bootloader() -> None:
        """
        This function unlocks phone's bootloader (OEM). 
        The userhas to manually setup Xioami Account in phone settings and has to accept oem unlocking in fastboot.
    
            -> Returns an available Adb Connection! 
        """
        #'OEM Unlocking' options should be already enabled by Setup() function in Main.py
        Check_AdbConnection(AdbOrFastboot='Adb', DriversInstaller = Install_XioamiUSBDrivers)
        print(f'\n[{Colors["Green"]}Starting{Colors["Reset"]}] Unlocking process...')
        print(f'{Colors["Red"]}Make sure{Colors["Reset"]} that you created a "{Colors["Red"]}Mi Account{Colors["Reset"]}" and added it on your phone trough your phone settings : "{Colors["Grey"]}Mi Account{Colors["Reset"]}" option in home screen in settings!')
        print(f'Open {Colors["Green"]}Developer Options{Colors["Reset"]} and search for "{Colors["Grey"]}Mi Unlock status{Colors["Reset"]}" option and {Colors["Green"]}tap{Colors["Reset"]} on it!')
        print(f'{Colors["Green"]}Make sure{Colors["Reset"]} that you read and follow the instructions given in that screen and click on "{Colors["Grey"]}Add account and device{Colors["Reset"]}" option.')
        input(f"Press {Colors['Red']}ENTER{Colors['Reset']} if you successfully connected the account : ")

        Download(
            URLink = 'http://miuirom.xiaomi.com/rom/u1106245679/6.5.406.31/miflash_unlock-en-6.5.406.31.zip',
            FileName = 'Xioami-Unlock-Tool.zip'
        )
        ExtractZip(
            Zip_FileName = 'Xioami-Unlock-Tool.zip',
            DestinationPath = ToolsFolder,
            HasFolderInside = False
        )
        
        print(f'{Colors["Green"]}Starting{Colors["Reset"]} Mi Unlock Tool...')
        os.startfile(ToolsFolder + 'Xioami-Unlock-Tool\\miflash_unlock.exe')
        print(f'Please, {Colors["Green"]}Log In{Colors["Reset"]} with your Mi account on "{Colors["Green"]}Mi Unlock Tool{Colors["Reset"]}"')
        input(f"Press {Colors['Red']}ENTER{Colors['Reset']} if you successfully logged in Mi Unlock Tool : ")

        print(f'{Colors["Green"]}Rebooting{Colors["Reset"]} phone into {Colors["Red"]}Bootloader Mode{Colors["Reset"]}...')
        os.system('adb reboot bootloader')
        sleep(6)    #Normal reboot time
        while 'Checking for fastboot connection':
            if Check_AdbConnection(AdbOrFastboot='Fastboot'):
                return
            sleep(3)
        
        print(f'{Colors["Red"]} -> {Colors["Reset"]}[{Colors["Green"]}In Bootloader Mode{Colors["Reset"]}!]\n')
        print(f'{Colors["Green"]}Checking{Colors["Reset"]} Bootloader status...')
    #     print(
    #         f'''
    # | No. |    SN    |    Product    |    Status    |    Message    |
    # |  1  | 77d64176 |     venus     |    {Colors["Blue"]}Locked{Colors["Reset"]}    |               |


    #                     Refresh(F5)  Unlock(F6)
    #     {Colors["Blue"]}Sign out{Colors["Reset"]}

    #     '''
    #     )
        # if not askUser('Right?'):
        #     print(f'Well, it might be a {Colors["Green"]}drivers issue{Colors["Reset"]}...')
        #     print(f'{Colors["Green"]}Click{Colors["Reset"]} on Mi Unlock Tool settings and click on "{Colors["Green"]}Check{Colors["Reset"]}" option.')
        
        
        print(f'{Colors["Green"]}Ok{Colors["Reset"]}, now click on "Unlock" option to unlock bootloader and accept unlocking.')
        #TODO: Check whater this process can be autometed. Libraries to manage with app GUI are trash in this case!
        if askUser(f'{Colors["Green"]}Does{Colors["Reset"]} the tool report "Please unlock {Colors["Red"]}168 hours{Colors["Reset"]} later."?'):
            print(f'{Colors["Red"]}Then{Colors["Reset"]} you have to {Colors["Green"]}wait 7 days{Colors["Reset"]} from now to be able to unlock the bootloader!')
            print(f'There is {Colors["Red"]}no way{Colors["Reset"]} to {Colors["Red"]}bypass{Colors["Reset"]} this waiting!')
            print(f'Without Unlocking bootloader {Colors["Underline"]}there is no way to flash unofficial files{Colors["Reset"]}, and this means that cannot root this device for now!')
            Quit(
                ExceptionName = SystemExit,
                Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} root this device!\n{Colors["Red"]}Must{Colors["Reset"]} wait 7 days in order to be able to unlock the bootloader!'
            )

        
        print(f'{Colors["Green"]}Congratulation{Colors["Reset"]}!\nYour phone bootloader is unlocking!')
        print(f'Your phone is now {Colors["Green"]}erasing data{Colors["Reset"]} and it\'s going to {Colors["Green"]}reboot{Colors["Reset"]}!')
        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} if your phone rebooted completely : ")
        print(f'{Colors["Green"]}Starting{Colors["Reset"]} Setup process...')
        SetupDeviceForUSBCommunication()
        Check_AdbConnection(AdbOrFastboot = 'Adb')

    def Download_Firmware() -> None:
        """
        This function downloads latest stock firmware into DownloadsFolder\\Firmware 
        and extracts boot.img into Firmware\\Extracted_Files

            -> Returns an available Adb Connection!
        """
        
        #Build number is essential to download the correct current version, else need to update to latest versin possible which require more steps
        
        def Get_DownloadLink() -> str:
            URL = "https://xiaomifirmwareupdater.com/miui/excalibur/stable/V13.0.2.0.SJXINXM/" #This download page must exists, if not then cannot download firmware version.
            # The URL should be something like : https://xiaomifirmwareupdater.com/miui/{Device.Region}/stable/{Device.BuildNumber}.{Device.Brand}/ , need to test adb shell getprop on a xioami device...
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

    def Firmware_Flashing():
        """
        This function reboots the device into fastboot mode, flashes all stock firmware images.
        Then flashes patched_boot.img istantly after flashing stock firmware images.
        Patching process has be done first to be able to root the phone.
         -> Returns an available Adb Connection.
        """
        Check_AdbConnection(AdbOrFastboot = 'Adb')

        # It doesn't have any sense trying to flash every partition as there are lot of different scenarios in firmwares type and also lot and different images!
        # So we are going to flash just boot.img which has been patched before.
        print(f'\n{Colors["Green"]}Starting{Colors["Reset"]} Firmware flashing process...')
        
        print(f'\n{Colors["Green"]}Rebooting{Colors["Reset"]} into {Colors["Green"]}Fastboot Mode{Colors["Reset"]}...')
        os.system('adb reboot-bootloader')
        print(f'\n{Colors["Green"]}Waiting{Colors["Reset"]} for {Colors["Green"]}Fastboot{Colors["Reset"]} Connection...')
        Check_AdbConnection(AdbOrFastboot = 'Fastboot')
        print(f'\n{Colors["Green"]}Flashing{Colors["Reset"]} patched boot.img on {Colors["Green"]}boot partition{Colors["Reset"]}...\n')

        # Since the firmware is the current one which is running on user phone, we can just patch boot.img and flash it!
        Flashing_Output = str(subprocess.check_output(f'fastboot flash boot "{DownloadsFolder}Firmware\\Extracted_Files\\boot.img"', stderr=subprocess.STDOUT, shell = True), encoding = 'utf-8')
        # if 'failed' in Flashing_Output.lower(): # It shouldn't fail, it should flash anyways. If something goes wrong the user will see it while rebooting phone...

        print(f'{Colors["Green"]}Rebooting{Colors["Reset"]}...')
        subprocess.check_output(f'fastboot reboot', stderr=subprocess.STDOUT, shell = True) #-w options is optional if the user would like to erase data but it's better to don't erase it, else re-configuration is required...

        
        print(f'\n{Colors["Red"]} -> {Colors["Reset"]}[{Colors["Green"]}Finished{Colors["Reset"]} Flashing process!]\n')
        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} if the phone has rebooted : ")
        Check_AdbConnection(AdbOrFastboot = 'Adb')


    Unlock_Bootloader()
    Download_Firmware()
    Patch_Image_File(
        Device = Device,
        BootImage_Name = 'boot.img'
    )
    Firmware_Flashing()
    ConfigureMagisk()



