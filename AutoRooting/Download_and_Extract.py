import requests
import zipfile
import subprocess

def Download_and_Extract(URL, DownloadPath = str(subprocess.check_output('echo %USERPROFILE%\\Downloads', stderr=subprocess.STDOUT, shell = True))[2:-5]):
    FileName =URL.split('/')[-1]
    save_path = DownloadPath + '\\' + FileName

    print(f'Downloading {FileName} to {DownloadPath}')
    r = requests.get(URL, stream=True)

    file = open(save_path, 'wb').write(r.content)
    
    #Extract the zip file
    with zipfile.ZipFile(save_path, 'r') as zipref:
        print(f'Extracting {FileName}...')
        zipref.extractall(save_path.replace(FileName, ''))
