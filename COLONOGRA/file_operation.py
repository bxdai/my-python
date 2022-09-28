#
#%%
import os
import sys
import SimpleITK as sitk
import time
from tqdm import tqdm, trange
from batchgenerators.utilities.file_and_folder_operations import subfiles,subdirs
import shutil
from typing import List


my_file_list =[
"/mnt/data/meddata/CTPelvic1K/CERVIX",
"/mnt/data/meddata/CTPelvic1K/CLINIC",
"/mnt/data/meddata/CTPelvic1K/COLONOG",
"/mnt/data/meddata/CTPelvic1K/KITS19",]

# my_file_list =["/mnt/data/meddata/CTPelvic1K/ABDOMEN",
# "/mnt/data/meddata/CTPelvic1K/CERVIX",
# "/mnt/data/meddata/CTPelvic1K/CLINIC",
# "/mnt/data/meddata/CTPelvic1K/COLONOG",
# "/mnt/data/meddata/CTPelvic1K/KITS19",]

my_file_list3 =[
"/mnt/data/meddata/CTPelvic1K/ABDOMEN",
]

#%%
def add_suffex(file_path:List[str],suffix=".nii.gz"):
     for key in file_path:
        img_path = os.path.join(key,"img")
        #seg_path = os.path.join(key,"seg")
        img_cases = subfiles(img_path, join=True,suffix= None)
        #seg_cases = subfiles(seg_path, join=True,suffix= ".nii.gz")
        for img in tqdm(img_cases, desc='Processing img'):
             #print(f"{img[:-12]}\n")
             os.rename(img,img+ "_0000.nii.gz")
        # for seg in tqdm(seg_cases, desc='Processing seg'):
        #     os.rename(seg,seg+ ".nii.gz")

add_suffex(["/mnt/data/meddata/CTPelvic1K/ABDOMEN"])
#%%
#删除文件的0000

def remove_file_zero(file_Path:str):
    img_cases = subfiles(file_Path, join=True,suffix= ".nii.gz")
    for img in tqdm(img_cases, desc='Processing img'):
             os.rename(img,img[:-12] + ".nii.gz")


def remove_nii_file_zero(file_path:List[str]):

    for key in file_path:
        img_path = os.path.join(key,"img")
        seg_path = os.path.join(key,"seg")
        img_cases = subfiles(img_path, join=True,suffix= ".nii.gz")
        seg_cases = subfiles(seg_path, join=True,suffix= ".nii.gz")
        for img in tqdm(img_cases, desc='Processing img'):
             os.rename(img,img[:-12] + ".nii.gz")
        for seg in tqdm(seg_cases, desc='Processing seg'):
            os.rename(seg,seg[:-18] + ".nii.gz")
 

#remove_nii_file_zero(my_file_list3)
#remove_file_zero("/mnt/data/meddata/CTPelvic1K/CERVIX/Unlabeled images")
#remove_file_zero("/mnt/data/meddata/CTPelvic1K/KITS19/Unlabeled images")
remove_nii_file_zero(["/mnt/label/standard/Task_CTPelvic1K/reviewed/MSD_T10"])
# %%
