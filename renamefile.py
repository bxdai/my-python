#%%
from ast import arg
from email.mime import image
import json
import os
from posixpath import split
import random
import shutil
from collections import OrderedDict
from typing import List, Tuple
import argparse
from batchgenerators.utilities.file_and_folder_operations import subdirs,subfiles

#%%
def get_parent_dir(path=None, offset=-1):
    result = path if path else __file__
    for i in range(abs(offset)):
        result = os.path.dirname(result)
    return result

def rename_nii_file(file_path:str):

    work_dir = get_parent_dir(file_path)
    cases = subfiles(file_path, join=False,suffix= ".nii.gz")
    #root_dir = os.path.join(work_dir, "labels_new")
    #os.makedirs(root_dir, exist_ok=True)
    for it in cases:
        print(f"{it}\n")
        shutil.move(os.path.join(file_path, it),
        os.path.join(file_path, it[:-7] + "_0000.nii.gz"))

def rename_label_files(file_path:str):
    work_dir = get_parent_dir(file_path)
    cases = subfiles(file_path, join=False,suffix= ".nii.gz")
    root_dir = os.path.join(work_dir, "labels_new")
    os.makedirs(root_dir, exist_ok=True)
    for it in cases:
        print(f"{it}\n")
        shutil.copy(os.path.join(file_path, it),
        os.path.join(root_dir, it[:-7] + "_0000_label.nii.gz"))
#nii_file_name = 'D:/medicalData/CTPelvic1K_dataset/dataset/COLONOG'
nii_file_name = '//192.168.100.4/data/meddata/CTPelvic1K/KITS19/img'
rename_nii_file(nii_file_name)
#rename_nii_file("//192.168.100.4/data/meddata/Abdomen/Abdomen/RawData/Testing/img")
#rename_label_files("C:/Users/Bxd/Desktop/test_landmark_3d/input")
#%%
#根据label 选择img

def select_img_from_label():
    file_path = '//192.168.100.4/data/meddata/CTPelvic1K/KITS19/seg'
    #img_path = "D:/medicalData/CTPelvic1K_dataset/dataset/COLONOG"
    img_path = "//192.168.100.4/data/meddata/CTPelvic1K/KITS19"
    origin_img_path = "//192.168.100.4/data/meddata/CTPelvic1K/KITS19/all"
    target_image_path = os.path.join(img_path,"img")
    target_label_path = os.path.join(img_path,"seg")
    volume_label_list = subfiles(file_path, join=False,suffix= ".nii.gz")
    for it in volume_label_list:
        #print(f"{it[:-13]}\n")
        print(it)
        shutil.move(os.path.join(file_path,it),os.path.join(target_label_path,it))
        #shutil.move(os.path.join(img_path,it[:-13]+".nii.gz"),os.path.join(target_image_path,it[:-13]+".nii.gz"))
        shutil.move(os.path.join(origin_img_path,it),os.path.join(target_image_path,it))
select_img_from_label()

#%%
def rename_kits19_files():
    file_path = "//192.168.100.4/data/meddata/CTPelvic1K/KITS19/img"

    volume_list = subfiles(file_path, join=False,suffix= ".nii.gz")
    for it in volume_list:
        #img_name =it.split('_')[1] + "_" + it.split('_')[2] +"_"+ it.split('_')[3]
        img_name ="kits19_" + it.split('_')[1]
        #img_name =it.split('-')[0] + "_" + it.split('-')[1]
        #img_name = it[:-19]
        print(f"{img_name}")
        if os.path.exists(os.path.join(file_path,it)):
            os.rename(os.path.join(file_path, it), os.path.join(file_path,img_name))
            #os.rename(os.path.join(file_path, it), os.path.join(file_path,img_name + "_0000_label.nii.gz"))
            pass
rename_kits19_files()
#%%
#file_path = 'D:/medicalData/CTPelvic1K_dataset/dataset/CTPelvic1K_dataset1_mask_mappingback'
#file_path = 'D:/medicalData/CTPelvic1K_dataset/dataset/CTPelvic1K_dataset3_mask_mappingback'
#file_path = 'D:/medicalData/CTPelvic1K_dataset/dataset/ipcai2021_dataset6_Anonymized'
#file_path = 'D:/medicalData/CTPelvic1K_dataset/dataset/CTPelvic1K_dataset6_data'
#file_path = 'D:/medicalData/CTPelvic1K_dataset/dataset/CTPelvic1K_dataset7_mask'
#file_path = 'D:/medicalData/CTPelvic1K_dataset/dataset/CTPelvic1K_dataset7_data'
#file_path = "D:/medicalData/CTPelvic1K_dataset/dataset/CTPelvic1K_dataset2_mask_mappingback"
#file_path = 'D:/medicalData/CTPelvic1K_dataset/dataset/CTPelvic1K_dataset5_mask_mappingback'
#file_path = 'D:/medicalData/CTPelvic1K_dataset/dataset/CTPelvic1K_dataset4_mask_mappingback'
#file_path = 'D:/medicalData/CTPelvic1K_dataset/dataset/CERVIX/all'
file_path = "//192.168.100.4/data/meddata/CTPelvic1K/KITS19/Unlabeled images"

volume_list = subfiles(file_path, join=False,suffix= ".nii.gz")
for it in volume_list:
    #img_name =it.split('_')[1] + "_" + it.split('_')[2] +"_"+ it.split('_')[3]
    img_name =it.split('_')[0] + "_" + it.split('_')[1]
    #img_name =it.split('-')[0] + "_" + it.split('-')[1]
    #img_name = it[:-19]
    print(f"{it}\n")
    print(img_name)
    if not os.path.exists(os.path.join(file_path,img_name + ".nii.gz")):
        os.rename(os.path.join(file_path, it), os.path.join(file_path,img_name + ".nii.gz"))
        #os.rename(os.path.join(file_path, it), os.path.join(file_path,img_name + "_0000_label.nii.gz"))
        pass
#%%
# 处理dataset5 Cervix
def rename_Cervix_from_label():
    file_path = 'D:/medicalData/CTPelvic1K_dataset/dataset/CERVIX'
    img_path = 'D:/medicalData/CTPelvic1K_dataset/dataset/CERVIX'
    origin_path = 'D:/medicalData/CTPelvic1K_dataset/dataset/CERVIX/all'
    target_image_path = os.path.join(img_path,"img")
    target_label_path = os.path.join(img_path,"seg")
    volume_label_list = subfiles(target_label_path, join=False,suffix= ".nii.gz")
    for it in volume_label_list:
        print(f"{it[:-24]}\n")
        source_file = os.path.join(origin_path, it[:-24] +"_Image_0000.nii.gz")
        target_file = os.path.join(target_image_path, it[:-24] +"_Image_0000.nii.gz")
        print(source_file)
        if os.path.exists(source_file) and not os.path.exists(target_file):
            print(target_file)
        #print(it)
            shutil.move(source_file,target_file)
        #shutil.move(os.path.join(img_path,it[:-13]+".nii.gz"),os.path.join(target_image_path,it[:-13]+".nii.gz"))
rename_Cervix_from_label()


#%%
#删除文件的0000
def remove_nii_file_zero(file_path:list[str]):

    work_dir = get_parent_dir(file_path)
    cases = subfiles(file_path, join=False,suffix= ".nii.gz")
    #root_dir = os.path.join(work_dir, "labels_new")
    #os.makedirs(root_dir, exist_ok=True)
    for it in cases:
        print(f"{it[:-13]}\n")
        #shutil.move(os.path.join(file_path, it),
        #os.path.join(file_path, it[:-13] + ".nii.gz"))

remove_nii_file_zero()

#%%
# 逐个处理
i = 602
print(os.getcwd())
g = os.walk(os.path.join(os.getcwd(),"input"))#在input目录下执行本脚本
for path, dir_list, file_list in g:
  for file_name in file_list:
    filename = os.path.join(path, f"img{i}.IMA")
    print(file_name)
    os.rename(os.path.join(path, file_name), filename)
   


    #生成的文件类似：img836_segment.nii.gz->label836.nii.gz
    segfile = os.path.join(path, f"img{i}_segment.nii.gz")
    labelfile = os.path.join(path, f"label{i}.nii.gz")
    os.rename(segfile, labelfile)

    i = i + 1
#%%
import SimpleITK as sitk
def read_dcm(filepath):
    series_id = sitk.ImageSeriesReader.GetGDCMSeriesIDs(filepath)
    series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(filepath, series_id[0])
    series_reader = sitk.ImageSeriesReader() 
    series_reader.SetFileNames(series_file_names)  
    images = series_reader.Execute()
    return images

