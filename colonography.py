from asyncore import read
import os
import sys
import SimpleITK as sitk
import time
from tqdm import tqdm, trange


def read_dcm(filepath):
    p_dir = os.path.dirname(filepath)
    #series_id = sitk.ImageSeriesReader.GetGDCMSeriesIDs(filepath)
    series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(filepath)
    series_reader = sitk.ImageSeriesReader() 
    series_reader.SetFileNames(series_file_names)  
    images = series_reader.Execute()
    return images


file_test = '//192.168.100.4/data/meddata/CTSpine1K/COLONOGRA'

def read_files():
    g = os.walk(file_test)#在input目录下执行本脚本
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

target_dir = "//192.168.100.4/data/meddata/CTSpine1K/COLONOGRA/nii_gz_files"

# listdirs(file_test)
# write_txt()

def analyze_file_directories(file_path:str):
    list_f = file_path.split("/")
    f8 = list_f[8]
    f10 = list_f[10]
    f10_list = f10.split("-")[0].split(".")[0]
    target_file = os.path.join(target_dir,f8+"_"+ f10_list+"_0000.nii.gz")
    file_path= file_path[:-2]
    print(file_path)
    image = read_dcm(file_path)
    sitk.WriteImage(image, target_file)
    pass




if __name__ == '__main__':
    files_list = read_txt("./data/c1.txt")
    for i in tqdm(range(len(files_list)), desc='Processing'):
        #time.sleep(0.05)
        analyze_file_directories(files_list[i])
        print(files_list[i])