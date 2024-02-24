import zipfile
import tarfile
import os
from gdt.core import data_path
asm_path = data_path / 'rxte-asm'
os.chdir(asm_path)
with zipfile.ZipFile('rxte_asm_camera_data.zip','r') as zip_ref:
   zip_ref.extractall()

print ("Unpacking numerous tiny RXTE ASM files. Please be patient.") 
os.chdir('camera_data/cam_dwasc_01')   
tar = tarfile.open("cam_dwasc_01.tar.gz")
tar.extractall()
tar.close

os.chdir('../cam_dwasc_02')   
tar = tarfile.open("cam_dwasc_02.tar.gz")
tar.extractall()
tar.close

os.chdir('../cam_dwasc_03')
tar = tarfile.open("cam_dwasc_03.tar.gz")
tar.extractall()
tar.close

os.chdir('../cam_evasc_01')
tar = tarfile.open("cam_evasc_01.tar.gz")
tar.extractall()
tar.close

os.chdir('../cam_evasc_02')
tar = tarfile.open("cam_evasc_02.tar.gz")
tar.extractall()
tar.close

os.chdir('../cam_evasc_03')
tar = tarfile.open("cam_evasc_03.tar.gz")
tar.extractall()
tar.close

os.chdir('../cam_evasc_04')
tar = tarfile.open("cam_evasc_04.tar.gz")
tar.extractall()
tar.close

print ('Unpacking RXTE ASM Data complete')



