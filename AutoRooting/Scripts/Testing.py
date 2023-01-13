

from AutoRootUtilities import *



def Download_Status(Status: str):
    path = os.getcwd() + "\\Downloads\\"
    versions = str(subprocess.check_output(f'samloader -m GT-I8190N -r XME checkupdate', stderr = subprocess.STDOUT, shell = True), encoding = 'utf-8')[:-2]
    if Status == 'New Download':
        try:
            os.system(f'samloader --dev-model GT-I8190N --dev-region XME download --fw-ver {versions} --do-decrypt --out-dir {path}')
        except ConnectionAbortedError:
            print(f'Your {Colors["Red"]}internet connection{Colors["Reset"]} has been stopped or aborted!\nPlease {Colors["Green"]}check{Colors["Reset"]} your internet connection!')
            input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to confirm if your internet connection works : ")
            if isConnected():
                Download_Status(Status = 'Resume Downlad') 
            else:
                raise SystemExit()
        
        except Exception as ex:
            print('Cannot start or continue {Phone.Model} firmware\'s download for an unknown error!')
            input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
            raise SystemExit()

    elif Status == 'Resume Download':
        print(f'{Colors["Green"]}Resuming{Colors["Reset"]} the download...')
        try:
            os.system(f'samloader --dev-model GT-I8190N --dev-region XME download --resume --fw-ver {versions} --do-decrypt --out-dir {path}')

        except ConnectionAbortedError:
            print(f'Your internet connection has been stopped or aborted!\nPlease check your internet connection!')
            input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to confirm if your internet connection works : ")
            if isConnected():
                Download_Status(Status = 'Resume Downlad') 
            else:
                raise SystemExit()

        except Exception as ex:
            print('Cannot start or continue {Phone.Model} firmware\'s download for an unknown error!')
            input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
            raise SystemExit()

Download_Status('New Download')
