#Copyright (C) <2023> by <Quantum>
from Scripts.Utilities import *

Pip_Installer(Package = 'selenium')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def OnePlus_Requirements(Device: object):

    def Install_OnePlusUSBDrivers():
        Install_USBDrivers(
            Model = 'Oneplus',
            URL = 'https://doc-14-7c-docs.googleusercontent.com/docs/securesc/mpd87nm19v31j1fgop1dnpipp02448lp/knvt3q720cc3icvekbp8co8o1ri6l89h/1677339000000/15363273046932124377/12401289761959382876/10OkwDG_kHttsPn21rLRjN4REKeS-wF7H?e=download&ax=AB85Z1CMjNFha5D4go1Q4E-TlWOgm6ph4HobcaCaiwoJtrsKANG5lMC5ABPNiHVjmpEHs_kC966poI-fuOvtxASRyG0jkJcSOkselZYM1bojYdWb0MtK0RKug7UtCUpXQfqQYpnE_GAVMWM_lyQfOzLk4EUJPjPLSn45goGw3OGZQ8eYFU_-pkRirm8Zsm2uagzYEJKIRNU8OGPr8FD-Q_9T0MqAvEirVutuLi912oT_hEHvWUTT0AI1f7h44R3iozlPdHg5qOG9LfT8VBXTBlX2FTNY_HNs05QwbSv0f0sFBJC4Pz6O3Ml7ibKMsWBhy5Jbu0wR5_Yzy8D0k12yS2GxwfKUOKrQ06aL4TsTqHF8I2vEt59dqoyCpTXwBJ8ycX_t-oAFTofHOyTCE_H29djQCPc3v9HT7Bzsqtvxp3p4Gov_kZprRh4OFC93ndtuy9IyhplIldXIp0uAelv5onoImdcA7ek1npNK5NTr-I0X12_xiv1zr2t907JHkk6tF_F3DXRjV18OfKXGkGZ7ZsJOoP5BEIOSEu4XJK2m2gN6E2S5WJtuUcOhh3_6RAKaoJASq-XvCMmnmTYF4x97UJYuzY0Fa0IxFjeVHJz1DhLSzTeks_VE_udWt_GV7nqOLzgJ0stCw2QhcNA-bT9HROKBFyxFlwq7oxmBo_ubOEQicdmJgViAbWRs_khcEh03gCMOFxy7cEU3QLh8BXjW0maiyIr8CMfcWF2RcFXTK7JUStz-Lrrl6wkqFrJMLie_VjCPowZOjCSTpaoBBTtTmMl37B-qJm1mGsrX8fzD7Y52gY5ullMp6YuxYjAmRndgKkmqmA5Ss_ujAvzwb79B2IEpUmNZ69wKwI6TwDbbNhvHcPuhFSm5dQ9liJqqVnMTpmNcVvEtIu4yDC52N9rQxd9vJqwzV7R0TwolKcc8GhDo8zcbNO4jrDGS4KVcR7aWk_vTwVv2JlKOHhVOfnbcon1HD33yEjieaPc4ZFZjT3nWgtRrd-M8L1h6TY2NnEbEG-oxMyplQm1fZ1mCy5nxf3i1zSMTXCCdmbXvR5fXgtDAL4HiBbjgSAqoeN6WI_RGuy4WKtaHj-JG4n0hwLK8j4o2&uuid=977a5a2b-3103-43a4-8ec3-8fba2e149e23&authuser=1&nonce=7po53tiitnme4&user=12401289761959382876&hash=hdtr6d0dfbm8dnfelufohtt18oi0hj96',
            isZip = True,
            Exe_File = 'OnePlus USB Drivers\\OnePlus_USB_Drivers_Setup.exe'
        )

    
    def Unlock_Bootloader() -> None:
        """
        This function unlocks phone's bootloader (OEM). 
        The userhas to manually accept Unlocking.
    
            -> Returns an available Adb Connection! 
        """
        print(f'\n[{Colors["Green"]}Starting{Colors["Reset"]}] Unlocking process...')
        Check_AdbConnection(AdbOrFastboot='Adb', DriversInstaller = Install_OnePlusUSBDrivers)
        print(f'{Colors["Green"]}Rebooting{Colors["Reset"]} phone into {Colors["Red"]}Bootloader Mode{Colors["Reset"]}...')
        os.system('adb reboot bootloader')
        sleep(6)    #Normal reboot time
        while 'Checking for fastboot connection':
            if Check_AdbConnection(AdbOrFastboot='Fastboot'):
                return
            sleep(3)
        
        print(f'{Colors["Red"]} -> {Colors["Reset"]}[{Colors["Green"]}In Bootloader Mode{Colors["Reset"]}!]\n[{Colors["Red"]}Unlocking bootloader{Colors["Reset"]}...]')
        Unlocking = str(subprocess.check_output(f'fastboot flashing unlock', stderr = subprocess.STDOUT, shell = True), encoding='utf-8')
        if not 'OKAY' in Unlocking:
            Unlocking = str(subprocess.check_output(f'fastboot oem unlock', stderr = subprocess.STDOUT, shell = True), encoding='utf-8')

        if not 'OKAY' in Unlocking:
            Unlocking = str(subprocess.check_output(f'fastboot flashing unlock_critical', stderr = subprocess.STDOUT, shell = True), encoding='utf-8')
        
        if not 'OKAY' in Unlocking:
            Quit(
                ExceptionName = SystemExit(),
                Message = f'{Colors["Red"]}Cannot{Colors["Reset"]} unlock this OnePlus ({Device.Model}) phone!'
            )

        print(f'{Colors["Red"]}Now{Colors["Reset"]} follow the instructions shown on your phone\'s screen to {Colors["Red"]}confirm the unlocking{Colors["Reset"]} of the bootloader (Click volume up key to choose "{Colors["Red"]}Unlock the bootloader{Colors["Reset"]}" and confirm)!')
        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to confirm that you confirmed Unlocking (Now the phone should reboot) : ")
        
        print(f'\nYour phone should now boot successfully in {Colors["Cyan"]}Welcome Screen{Colors["Reset"]}!')
        print(f'{Colors["Green"]}Skip{Colors["Reset"]} all skippable things such as {Colors["Green"]}Cloud Backup{Colors["Reset"]} and {Colors["Green"]}Google Account{Colors["Reset"]}')
        print(f'{Colors["Red"]}Configure internet connection{Colors["Reset"]}!')

        input(f"\n\tPress {Colors['Green']}ENTER{Colors['Reset']} if you have done all : ")

        SetupDeviceForUSBCommunication()
        Check_AdbConnection(AdbOrFastboot = 'Adb')


    def Download_Firmware() -> None:
        """
        This function downloads latest stock firmware into DownloadsFolder\\Firmware 
        and extracts boot.img into Firmware\\Extracted_Files

            -> Returns an available Adb Connection!
        """
        
        def Get_Link() -> str:
            URL = "https://service.oneplus.com/global/search/search-detail?id=2096329&articleIndex=1"
            print(f'{Colors["Green"]}Opening{Colors["Reset"]} {URL} website to get firmware download link...')
            print(f'{Colors["Green"]}_________________________________________________________________________________________________{Colors["Reset"]}')

            if checkTool(name = 'msedge.exe', path = "C:\Program Files (x86)\Microsoft\Edge\Application\\"):
                Edge_Options = webdriver.EdgeOptions()
                Edge_Options.add_argument('--start-minimized')
                Edge_Options.add_argument('--log-level=3')
                browser = webdriver.Edge(options = Edge_Options)
            elif checkTool(name = 'chrome.exe', path = 'C:\Program Files (x86)\Google\Chrome\Application\\'):
                Chrome_Options = webdriver.ChromeOptions()
                Chrome_Options.add_argument('--start-minimized')
                Chrome_Options.add_argument('--log-level=3')
                browser = webdriver.Chrome(options = Chrome_Options)
            elif checkTool(name = 'firefox.exe', path = 'C:\Program Files\Mozilla Firefox\\'):
                Firefox_Options = webdriver.FirefoxOptions()
                Firefox_Options.add_argument('--headless')
                Firefox_Options.add_argument('--log-level=3')
                browser = webdriver.Firefox(options = Firefox_Options)
            else:
                Quit(
                    ExceptionName = SystemExit,
                    Message = f'{Colors["Red"]}Cannot find{Colors["Reset"]} any browser on this computer!\nMake sure that one of these browsers is installed : {Colors["Green"]}Microsoft Edge{Colors["Reset"]}, {Colors["Green"]}Chrome{Colors["Reset"]} or {Colors["Green"]}Firefox{Colors["Reset"]}'
                )
            #Safari browser if mac
            browser.get(URL)
            delay = 5  # seconds
            selector = ".search-detail--wrapper_content table"
            try:
                table = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                table_html = table.get_attribute("outerHTML")
                for td in table_html.split('\n'):
                    try:
                        td: str = td.split('href="')[1].split('" target')[0]
                        if (Device.Model).lower().replace(' ', '') in td.lower():
                            link = td
                            browser.close() # Takes time to close the browser 3-5 seconds
                            return link.strip()
                    except:
                        pass
                Quit(
                    ExceptionName = SystemExit,
                    Message = f'{Colors["Red"]}Cannot find{Colors["Reset"]} any firmware for {Device.Model}!'
                )
            except TimeoutException:
                browser.close()
                Quit(
                    ExceptionName = SystemExit,
                    Message = f'TimeoutException!\nCannot parse {URL} webpage!'
                )

        
        print(f'\n{Colors["Green"]}Looking{Colors["Reset"]} for {Device.Model} Firmware version...')
        link = Get_Link()
        print(f'{Colors["Green"]}_________________________________________________________________________________________________{Colors["Reset"]}')
        print(f'\n{Colors["Red"]} -> {Colors["Reset"]}[{Colors["Green"]}Server{Colors["Reset"]}]: {link}')
        Download(
            URLink = link,
            FileName = 'Firmware.zip'
        )
        if GetFileName_FromZip(Zip_Path = DownloadsFolder + 'Firmware.zip', FileName = 'payload.bin'):
            ExtractZip(
                Zip_FileName = 'Firmware.zip',
                DestinationPath = DownloadsFolder,
                HasFolderInside = False,
                SpecificFile = 'payload.bin'
            )

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
            #NOT EVERY FIRMWARE HAS THE SAME FILES, FOR OLDER FIRMWARES PAYLOAD.BIN DOESN'T EXISTS
            #All oneplus devices can be rooted but need to work on their firmware
            print(f'\n{Colors["Green"]}Extracting{Colors["Reset"]} Firmware images from payload.bin : \n')
            os.system(f'{sys.executable} {ToolsFolder}payload_dumper-master\\payload_dumper.py {DownloadsFolder}Firmware\\payload.bin --out {DownloadsFolder}Firmware\\Extracted_Files')
            print(f'{Colors["Reset"]}{Colors["Red"]} -> {Colors["Reset"]}[{Colors["Green"]}Done{Colors["Reset"]}!]\n')

        else: #Andorid 8 or lower:
            ExtractZip(
                Zip_FileName = 'Firmware.zip',
                DestinationPath = DownloadsFolder,
                HasFolderInside = False
            )
            if not os.path.exists(DownloadsFolder + 'Firmware\\Extracted_Files'):
                os.mkdir(DownloadsFolder + 'Firmware\\Extracted_Files')
            os.replace(f'{DownloadsFolder}Firmware\\boot.img', f'{DownloadsFolder}Firmware\\Extracted_Files\\boot.img')
                

    def Firmware_Flashing():
        """
        This function reboots the device into fastboot mode, flashes all stock firmware images.
        Then flashes patched_boot.img istantly after flashing stock firmware images.
        Patching process has be done first to be able to root the phone.
         -> Returns an available Adb Connection.
        """
        Check_AdbConnection(AdbOrFastboot = 'Adb')
        print(f'\n{Colors["Green"]}Starting{Colors["Reset"]} Firmware flashing process...')
        
        print(f'\n{Colors["Green"]}Rebooting{Colors["Reset"]} into {Colors["Green"]}Fastboot Mode{Colors["Reset"]}...')
        os.system('adb reboot-bootloader')
        print(f'\n{Colors["Green"]}Waiting{Colors["Reset"]} for {Colors["Green"]}Fastboot{Colors["Reset"]} Connection...')
        Check_AdbConnection(AdbOrFastboot = 'Fastboot')
        print(f'\n{Colors["Green"]}Starting{Colors["Reset"]} Flashing process...\n')

        Main_Images = ['boot.img', 'dtbo.img', 'modem.img', 'recovery.img']
        Images = [image for image in os.listdir(f'{DownloadsFolder}Firmware\\Extracted_Files') if image.endswith('.img') and image not in Main_Images and (image != 'vbmeta.img' or image != 'vbmeta_system.img')]
        
        for image in Main_Images:
            print(f'{Colors["Red"]} -> {Colors["Reset"]}{Colors["Red"]}Flashing{Colors["Reset"]} {image[:-4]} partition...\n')
            Flashing_Output = str(subprocess.check_output(f'fastboot flash {image[:-4]} {DownloadsFolder}Firmware\\Extracted_Files\\{image}', stderr=subprocess.STDOUT, shell = True))
            if 'failed' in Flashing_Output.lower():
                print(f'\n{Colors["Red"]}Cannot{Colors["Reset"]} flash {image[:-4]} partition...\n')
        
        Flashing_Output = str(subprocess.check_output(f'fastboot --disable-verity flash vbmeta {DownloadsFolder}Firmware\\Extracted_Files\\vbmeta.img', stderr=subprocess.STDOUT, shell = True), encoding = 'utf-8')
        if 'failed' in Flashing_Output.lower():
            print(f'\n{Colors["Red"]}Cannot{Colors["Reset"]} flash vbmeta partition...\n')
        Flashing_Output = str(subprocess.check_output(f'fastboot --disable-verity flash vbmeta_system {DownloadsFolder}Firmware\\Extracted_Files\\vbmeta_system.img', stderr=subprocess.STDOUT, shell = True), encoding = 'utf-8')
        if 'failed' in Flashing_Output.lower():
            print(f'\n{Colors["Red"]}Cannot{Colors["Reset"]} flash vbmeta_system partition...\n')
        
        Flashing_Output = str(subprocess.check_output('fastboot reboot fastboot', stderr=subprocess.STDOUT, shell = True))
        sleep(5)
        Check_AdbConnection(AdbOrFastboot='Fastboot')

        for image in Images:
            print(f'{Colors["Red"]} -> {Colors["Reset"]}{Colors["Red"]}Flashing{Colors["Reset"]} {image[:-4]} partition...\n')
            Flashing_Output = str(subprocess.check_output(f'fastboot flash {image[:-4]} {DownloadsFolder}Firmware\\Extracted_Files\\{image}', stderr=subprocess.STDOUT, shell = True), encoding = 'utf-8')
            if 'failed' in Flashing_Output.lower():
                print(f'\n{Colors["Red"]}Cannot{Colors["Reset"]} flash {image[:-4]} partition...\n')
        
        
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