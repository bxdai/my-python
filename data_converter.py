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
        label = cases[key]
        img = label[:-13] + ".nii.gz"

        print(f"label:{label},img:{img}")

        if i < test_count:

            test_list.append(img)
            shutil.move(os.path.join(orgin_dir, img),
                        os.path.join(task_dir, "imagesTs", img))
            shutil.move(os.path.join(orgin_dir, label),
                        os.path.join(task_dir, "labelsTr", label))                        
        else:
            train_list.append(img)

            shutil.move(os.path.join(orgin_dir, img),
                        os.path.join(task_dir, "imagesTr", img))
            shutil.move(os.path.join(orgin_dir, label),
                        os.path.join(task_dir, "labelsTr", label))
        i = i+1
    
    return (train_list,test_list)


def convert(input: str, task_name: str,test_num:int = -1) -> None:

    #1.创建任务文件夹
    work_dir = os.getenv('nnUNet_raw_data_base')
    #work_dir = get_parent_dir(input)
    root_dir = os.path.join(work_dir, task_name)
    os.makedirs(os.path.join(root_dir, "imagesTr"), exist_ok=True)
    os.makedirs(os.path.join(root_dir, "imagesTs"), exist_ok=True)
    os.makedirs(os.path.join(root_dir, "labelsTr"), exist_ok=True)
    print(root_dir)

    #2.读取lable获取，获取标注总数
    cases = subfiles(input, join=False,suffix= "label.nii.gz")
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
    dataset_train_files,dataset_test_files = save_volume_to_task_directory(cases,input,root_dir,test_count,n)

    # save json
    with open("C:/Users/Bxd/Desktop/data_test/labels.json", 'r') as f:
        temp = json.loads(f.read())
        #print(temp)
        print(temp['labels'])

    json_dict = OrderedDict()
    json_dict['name'] = task_name
    json_dict['description'] = "Feature points "
    json_dict['tensorImageSize'] = "3D"
    json_dict['reference'] = "see visual3d database"
    json_dict['licence'] = "see visual3d database"
    json_dict['release'] = "0.0"
    json_dict['modality'] = {
        "0": "CT",
    }
    json_dict['labels'] = temp['labels']
    json_dict['numTraining'] = train_count
    json_dict['numTest'] = test_count

    json_dict['training'] = [{'image': "imagesTr/%s" % i, "label": "labelsTr/%s" % i} for i in
                            dataset_train_files]
    json_dict['validation'] =  []
    json_dict['test'] = ["imagesTs/%s" %
                        i for i in dataset_test_files]

    save_json(json_dict, os.path.join(root_dir, "dataset.json"))

if __name__ == '__main__':
    #parser = argparse.ArgumentParser()
    #parser.add_argument("-i", '--input_dir', help= "source directory", required=False)
    #parser.add_argument('-t', "--Task_xxxx", required=False, help="task name")
    #parser.add_argument('-m', '--mapping_file', help='id mapping file.',required=False)
    convert("C:/Users/Bxd/Desktop/data_test", "Task188_test",1)
    #work_dir = os.getenv('nnUNet_raw_data_base')
    #print(work_dir)
