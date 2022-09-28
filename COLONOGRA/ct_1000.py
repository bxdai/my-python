from asyncore import read
import os
import sys
import SimpleITK as sitk
import time
from tqdm import tqdm, trange
from batchgenerators.utilities.file_and_folder_operations import subfiles,subdirs
import shutil

def read_dcm(filepath):
    series_id = sitk.ImageSeriesReader.GetGDCMSeriesIDs(filepath)
    series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(filepath, series_id[0])
    series_reader = sitk.ImageSeriesReader() 
    series_reader.SetFileNames(series_file_names)  
    images = series_reader.Execute()
    return images


file_test = '//192.168.100.4/data/meddata/CTSpine1K/COLONOGRA'

def read_files():
    g = os.walk(file_test)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            print(file_name)

list_dir_Path = ["start",]
def listdirs(file_test):
    for line in os.listdir(file_test):
        fullpath = os.path.join(file_test,line)
        if os.path.isdir(fullpath):
            listdirs(fullpath)
            #print (fullpath)
        elif os.path.isfile(fullpath):
            current_dir_name = os.path.dirname(fullpath)
            last_dir_name = str(list_dir_Path[len(list_dir_Path) - 1])
            #last_dir_name.split('\\').
            if current_dir_name != last_dir_name:
                list_dir_Path.append(os.path.dirname(fullpath))
                print(os.path.dirname(fullpath))

def write_txt():
    with open('colonogra.txt', mode='a') as filename:
        for i in list_dir_Path:
            new_path = i.replace("\\","/")
            filename.write(new_path)
            filename.write('\n') # 换行


def read_txt(file_path:str):
    with open(file_path, 'r') as f:
        f_list = f.readlines()
        return f_list

def read_folders():
    g = os.listdir(file_test)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            print(file_name)

target_dir = "/mnt/data/meddata/CTSpine1K/COLONOGRA/nii_gz_files"

def analyze_file_directories(file_path:str):
    list_f = file_path.split("/")
    f8 = list_f[7]
    f10 = list_f[9]
    f10_list = f10.split("-")[0].split(".")[0]
    target_file = os.path.join(target_dir,f8+"_"+ f10_list+"_0000.nii.gz")
    file_path= file_path[:-1]
    print(file_path)
    if len(os.listdir(file_path)) > 10 and not os.path.exists(target_file):
        image = read_dcm(file_path)
        sitk.WriteImage(image, target_file)

def select_img_from_label():
    file_path = '/mnt/data/meddata/CTPelvic1K/COLONOG'
    #img_path ='/mnt/data/meddata/CTPelvic1K/COLONOG/img'
    origin_img_path = "/mnt/data/meddata/CTSpine1K/COLONOGRA/nii_gz_files"
    target_image_path = os.path.join(file_path,"img")
    target_label_path = os.path.join(file_path,"seg")
    volume_label_list = subfiles(target_label_path, join=False,suffix= ".nii.gz")
    i = 1
    for it in tqdm(volume_label_list, desc='Processing'):
    #for it in volume_label_list:
        print(f"{it[:-13]}\n")
        print(it)
        target_file = os.path.join(target_image_path,it[:-13]+".nii.gz")
        source_file = os.path.join(origin_img_path,it[:-13]+".nii.gz")
        if os.path.exists(source_file) and not os.path.exists(target_file):
        #shutil.move(os.path.join(file_path,it),os.path.join(target_label_path,it))
            shutil.copy(source_file,target_file)
            print("current index:",i)
            i = i+1
            pass



if __name__ == '__main__':


    #1
    # listdirs(file_test)
    # write_txt()
    #2.
    # files_list = read_txt("./data/c1.txt")
    # for i in tqdm(range(len(files_list)), desc='Processing'):
    #     #time.sleep(0.05)
    #     analyze_file_directories(files_list[i])
    #     print(files_list[i])
    #3.
    select_img_from_label()
