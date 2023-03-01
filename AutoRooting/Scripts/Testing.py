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





def Download_Firmware() -> None:
    """
    This function downloads latest stock firmware into DownloadsFolder\\Firmware 
    and extracts boot.img into Firmware\\Extracted_Files

        -> Returns an available Adb Connection! 
        -> Returns two global variabls : 
                'BootImage_Name': The name of the image to patch, because it could be recovery.img, boot.img or init_boot.img
                'BootImage_Path': The path where the image to patch is
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

    print(f'\n{Colors["Green"]}Extracting{Colors["Reset"]} Firmware images from payload.bin : \n')
    os.system(f'{sys.executable} {ToolsFolder}payload_dumper-master\\payload_dumper.py {DownloadsFolder}Firmware\\payload.bin --out {DownloadsFolder}Firmware\\Images')
    print(f'{Colors["Reset"]}{Colors["Red"]} -> {Colors["Reset"]}[{Colors["Green"]}Done{Colors["Reset"]}!]\n')


# Download_Firmware()
