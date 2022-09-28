#%%
import os
import sys
import SimpleITK as sitk
import time
from tqdm import tqdm, trange
from batchgenerators.utilities.file_and_folder_operations import subfiles,subdirs
import shutil
from typing import List

#%%
def replace_seg_to_null():
    img_path = "//mnt/label/standard/Task501_CTSpine1K/label"
    imgs_dir_list =   [os.path.join(img_path, i) for i in os.listdir(img_path) if os.path.isdir(os.path.join(img_path, i))]

    for path in imgs_dir_list:
        img_cases = subfiles(path, join=True,suffix=".nii.gz")
        for img in tqdm(img_cases, desc='Processing img'):
       
            new_img = img.replace("_seg","",1)
            print(f"{img}")
            print(f"{new_img}\n")
            os.rename(img,new_img)

def add_zero():

    # img_path = "//mnt/label/standard/Task501_CTSpine1K/data"
    # imgs_dir_list =   [os.path.join(img_path, i) for i in os.listdir(img_path) if os.path.isdir(os.path.join(img_path, i))]

    #imgs_dir_list =["//mnt/label/standard/Task501_CTSpine1K/data/Verse"]
    imgs_dir_list =["/mnt/label/standard/Task004_Hippocampus/reviewed/img"]
    for path in imgs_dir_list:
        #seg_path = os.path.join(key,"seg")
        img_cases = subfiles(path, join=True,suffix= ".nii.gz")
        for img in tqdm(img_cases, desc='Processing img'):
            target = img[:-7] +"_0000.nii.gz"
            print(f"{img}")
            print(f"{target}\n")
            os.rename(img,target)
#%%
add_zero()
#replace_seg_to_null()
# %%
import torch
a = torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(a.shape)
b = torch.tensor([[11, 22, 33], [44, 55, 66], [77, 88, 99]])
print(b.shape)
c = torch.stack([a, b], 0)
d = torch.cat([a, b], 0)
print(c.shape)
print(d.shape)
print(a)
print(b)
print(c)
print(d)

# %%
