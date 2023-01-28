
class Phones:
    def __init__(self) -> None:
        self.CPU_Architecture = 'arm64-v8a'

Phone = Phones()
from AutoRootUtilities import *
import time


def Patch_AP_File() -> None:  

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
        

Patch_AP_File()








# def ListaCircolare(Lista, A, B, K): #'ListaCircolare' è una funzione che 'accetta' 4 argomenti : 1 di tipo 'list' e gli altri tre di tipo 'int'.
#     #'A' indica l'indice di inizio (all'interno della lista) della lista circolare
#     #'B' indica l'indice di fine della lista circolare (all'interno della lista)
#     #'K' indica gli 'steps' del ciclo che modifica l'indice di ciascun elemento compreso tra inizio (A) e fine (B) 
#     # Esempio di output :
#     # ListaCircolare(Lista = [1, 2, 3, 4, 5], A = 1, B = 3, K = -1)
#     # -> [1, 3, 4, 2, 5]
#     # ListaCircolare(Lista = [1, 2, 3, 4, 5], A = 1, B = 4, K = -1)
#     # -> [1, 3, 4, 5, 2]
#     #
#     # Quindi A e B definiscono una lista su cui 'muovere' i valori 'lungo' gli indici :
#     # I numeri della Lista compresi tra A e B sono [2, 3, 4, 5]
#     # K = -1 indica che ciascun elemento presente all'interno di questa lista sia spostato a sinistra di 1 posizione : [3, 4, 5, 2]
#     # K = -2 : [4, 5, 2, 3]

#     LungAB = len(Lista[A:B])
#     if K > LungAB or K < -(LungAB): 
#         #Questa condizione serve a verificare se gli steps inseriti non siano maggiori del numero di elementi compresi tra A e B :
#         #Se B = 4 e K = -125 allora, se non rendo K < di B, il programma terminerà con un errore.
#         #A-B serve ad indicare il numero di elementi compresi tra A e B, altrimenti, se usassimo N, allora A dovrebbe essere PERFORZA 0 e B PERFORZA len(Lista) -> Significa che A e B sarebbero inutili...
#         K %= LungAB #Il modulo (%) restituisce il resto della divisione tra K e il numero di elementi compresi tra A e B

#     N = len(Lista) #All'interno di questa Lista DEVONO esserci ALMENO 3 elementi
#     if N >= 3:
#         if A >= 0 and A < B < N: #La fine non può mai essere minore dell'inizio e nemmeno maggiore del numero degli elementi presenti in Lista
#             l1 = [] #1 dei metodi per fare questo esercizio è creare una lista vuota senza modificare la lista originale

#             if K > 0: #Spostamento degli elementi verso destra
#                                 #Inizio ad aggiungere alla lista l1 gli ultimi elementi della lista Lista perché così :
#                                 # Data Lista = [1, 2, 3, 4, 5, 6, 7, 8]
#                                 # A = 1; B = 5; K = 2   -> [2, 3, 4, 5, 6]      #Lista[-2] è 7
#                                 # Output deve essere : [5, 6, 2, 3, 4]
#                                 # Perciò gli ultimi due elementi tralsati di due saranno i primi
#                                 # Quindi in questo ciclo for K assumerà valori da -2 fino a 2 (LungAB (5) - K (2) (-> 3)) (c'è anche lo 0, che è il 2)
#                 for indice in range(-K, LungAB - K, 1):
#                     l1.append(Lista[A:B][indice]) #Quindi parto da 5, poi 6, poi 2, 3, 4 e stop
#                     #Lista[A:B][indice] va a selezionare l'elemento (con indice 'indice') tra A e B e lo aggiunge alla lista l1

#             else: #Spostamento degli elementi verso sinistra o nullo (0)
#                 for indice in range(-LungAB - K, -K, 1):
#                     l1.append(Lista[A:B][indice])

            
#             print(l1) #[7, 8, 9]

#         else:
#             print('Errore : Gli argomenti passati alla funzione non sono corretti!')
#     else:
#         print('Errore : La lista non contiene ALMENO 3 elementi!')

# l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# ListaCircolare(Lista = l, A = 2, B = 6, K = -2)
