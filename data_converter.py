from ast import arg
from email.mime import image
import json
import os
import random
import shutil
from collections import OrderedDict
from typing import List, Tuple
import argparse


def subdirs(folder: str, join: bool = True, prefix: str = None, suffix: str = None, sort: bool = True) -> List[str]:
    if join:
        l = os.path.join
    else:
        def l(x, y): return y
    res = [l(folder, i) for i in os.listdir(folder) if os.path.isdir(os.path.join(folder, i))
           and (prefix is None or i.startswith(prefix))
           and (suffix is None or i.endswith(suffix))]
    if sort:
        res.sort()
    return res


def subfiles(folder: str, join: bool = True, prefix: str = None, suffix: str = None, sort: bool = True) -> List[str]:
    if join:
        l = os.path.join
    else:
        def l(x, y): return y
    res = [l(folder, i) for i in os.listdir(folder) if os.path.isfile(os.path.join(folder, i))
           and (prefix is None or i.startswith(prefix))
           and (suffix is None or i.endswith(suffix))]
    if sort:
        res.sort()
    return res

def copy_directory(source: str,target: str):
    if os.path.exists(target):
        shutil.rmtree(target)

    ignore_files=list(["processing","preprocessing","models","raw","reviewed"])
    if os.path.exists(source):
        shutil.copytree(source, target,ignore=shutil.ignore_patterns("processing","preprocessing","models","raw","reviewed"))
        print('copy dir finished!')

def nifti_files(folder: str, join: bool = True, sort: bool = True) -> List[str]:
    return subfiles(folder, join=join, sort=sort, suffix='.nii.gz')


def save_json(obj, file: str, indent: int = 4, sort_keys: bool = True) -> None:
    with open(file, 'w') as f:
        json.dump(obj, f, sort_keys=sort_keys, indent=indent)


def get_parent_dir(path=None, offset=-1):
    result = path if path else __file__
    for i in range(abs(offset)):
        result = os.path.dirname(result)
    return result

def save_volume_to_task_directory(cases:list,orgin_dir:str,task_dir:str,test_count,case_nume)->Tuple:

    #生成一个索引，并shuffle
    keys = [i for i in range(case_nume)]
    random.shuffle(keys)
    print(keys)
    train_list =[]
    test_list = []
    i = 0
    for key in keys:
        label = cases[key][:-7] + ".nii.gz"
        img = cases[key][:-13] + ".nii.gz"
        targetlabel = cases[key][:-18] + ".nii.gz"

        print(f"label:{label},img:{img}")

        if i < test_count:

            test_list.append(img)
            shutil.move(os.path.join(orgin_dir, img),
                        os.path.join(task_dir, "imagesTs", img))
            shutil.move(os.path.join(orgin_dir, label),
                        os.path.join(task_dir, "labelsTr", targetlabel))                        
        else:
            train_list.append(img)

            shutil.move(os.path.join(orgin_dir, img),
                        os.path.join(task_dir, "imagesTr", img))
            shutil.move(os.path.join(orgin_dir, label),
                        os.path.join(task_dir, "labelsTr", targetlabel))
        i = i+1
    
    return (train_list,test_list)

def rename_files(file_path:str):
    work_dir = get_parent_dir(file_path)
    cases = subfiles(file_path, join=False,suffix= ".nii.gz")
    root_dir = os.path.join(work_dir, "labels_new")
    os.makedirs(root_dir, exist_ok=True)
    for it in cases:
        print(f"{it}\n")
        shutil.copy(os.path.join(file_path, it),
        os.path.join(root_dir, it[:-7] + "_0000_label.nii.gz"))

def rename_nii_file(file_path:str):

    work_dir = get_parent_dir(file_path)
    cases = subfiles(file_path, join=False,suffix= ".nii.gz")
    #root_dir = os.path.join(work_dir, "labels_new")
    #os.makedirs(root_dir, exist_ok=True)
    for it in cases:
        print(f"{it}\n")
        shutil.move(os.path.join(file_path, it),
        os.path.join(file_path, it[:-7] + "_0000.nii.gz"))



def convert(input: str, output: str,task_name: str,test_num:int = -1) -> None:

    #1.创建任务文件夹
    if len(output) == 0 :
        work_dir = os.getenv('nnUNet_raw_data_base') +"/nnUNet_raw_data"
    else:
        work_dir = output
    #work_dir = get_parent_dir(input)
    root_dir = os.path.join(work_dir, task_name)
    os.makedirs(os.path.join(root_dir, "imagesTr"), exist_ok=True)
    os.makedirs(os.path.join(root_dir, "imagesTs"), exist_ok=True)
    os.makedirs(os.path.join(root_dir, "labelsTr"), exist_ok=True)
    print(root_dir)

    #2.读取lable获取，获取label总数
    cases = subfiles(os.path.join(input,"marked"), join=False,suffix= "label.nii.gz")
    print(cases)
    n = len(cases)
   
    #测试的个数:在nnunet里面实际是验证集合
    test_count = 0
    #训练的个数
    train_count = 0
    if test_num == -1:
        train_count = int(n*0.9)
        test_count = n-train_count
    else:
        test_count = test_num
        train_count = int(n-test_num)
    print(train_count)
    print(test_count)

    #3.随机分配数据去test和train
    #dataset_file_list = save_volume_to_task_directory(input,root_dir,test_num=2)
    dataset_train_files,dataset_test_files = save_volume_to_task_directory(cases,os.path.join(input,"marked"),root_dir,test_count,n)

    # save json
    json_dict = OrderedDict()

    
    with open(os.path.join(input,"task.json"), 'r',encoding='UTF-8') as f:
        task_json = json.loads(f.read())

        json_dict['name'] = task_name
        json_dict['description'] = task_json['description']
        json_dict['tensorImageSize'] =  task_json['tensorImageSize']
        json_dict['reference'] =  task_json['reference'] 
        json_dict['licence'] = task_json['licence']
        json_dict['relase'] = task_json['relase']
        json_dict['modality'] =  task_json['modality']
  
  
    with open(os.path.join(input,"labels.json"), 'r',encoding='UTF-8') as f:
        labels_json = json.loads(f.read())
        json_dict['labels'] = labels_json['labels']
        #print(temp)
        print(labels_json['labels'])

    json_dict['numTraining'] = train_count
    json_dict['numTest'] = test_count

    json_dict['training'] = [{'image': "./imagesTr/%s.nii.gz" % i[:-12], "label": "./labelsTr/%s.nii.gz" % i[:-12]} for i in
                            dataset_train_files]
    json_dict['validation'] =  []
    json_dict['test'] = ["./imagesTs/%s.nii.gz" %
                        i[:-12] for i in dataset_test_files]

    save_json(json_dict, os.path.join(root_dir, "dataset.json"))

if __name__ == '__main__':

    default_task_nanme = 'Task201_pelvic'
    default_input = "C:/Users/Bxd/Desktop/task_pelvis"
    default_temp_dir = os.path.join(os.getenv('nnUNet_raw_data_base'),"temp",os.path.basename(default_input))
    default_output = os.getenv('nnUNet_raw_data_base') +"/nnUNet_raw_data"
    default_num = -1


    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--input',default=default_input, help= "source directory", required=False)
    parser.add_argument('-t', "--task_name",default=default_task_nanme, required=False, help="taskNUM_XXX")
    parser.add_argument('-tmp', '--temp', default=default_temp_dir,help='temporary folders',required=False)
    parser.add_argument('-o', '--output', default=default_output,help='output directory',required=False)
    parser.add_argument('-n', '--test_number', default=default_num,help='test set number',required=False)

    args = parser.parse_args()
    print(f"input_dir:{args.input}\n")
    print(f"temp_dir:{args.temp}\n")
    print(f"output_dir:{args.output}\n")
    print(f"task_name:{args.task_name}\n")

    copy_directory(args.input,args.temp)
    convert(args.temp,args.output,args.task_name,args.test_number)
    shutil.rmtree(args.temp)
    # convert("C:/Users/Bxd/Desktop/data_test", "Task188_test",1)
    # work_dir = os.getenv('nnUNet_raw_data_base')
    #print(work_dir)

    #input_dir = "//192.168.100.4/label/markroot/task_pelvis"
   

    #rename_files("\\\\192.168.100.4\\Data\\meddata\\KiTS2021\\labelsTr")
    #rename_nii_file("\\\\192.168.100.4\\label\\markroot\\task_pelvis\\raw")
 