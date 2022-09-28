import SimpleITK as sitk
import numpy as np
import pandas as pd
import argparse
import json

def read_txt(filename:str):
    data_txt = np.loadtxt("./data/labelmapping.txt",delimiter=':')
    id_dict = {}
    data = data_txt.tolist()
    for v in data:
        s,t = v
        id_dict[s] = t
    print(json.dumps(id_dict,ensure_ascii=False,indent=4))
    return id_dict

def read_CSV(filename:str):
    data  = pd.read_csv("./data/labelmapping.csv",header=None)
    label_id_map = {}
    for index,row in data.iterrows():
        #print(row[index])
        print(row[0],row[1],type(row[0]),type(row[1]))
    

# name = "./data/labelmapping.csv"
# txt = "./data/labelmapping.txt"
# #read_CSV(name)
# read_txt(txt)


def chanage_nii_label(input_file:str,output_file:str,id_map:dict):
    img = sitk.ReadImage(fileName= input_file)
    print(type(img)) # <class 'SimpleITK.SimpleITK.Image'>
    data_np = sitk.GetArrayFromImage(img)

    new_data = data_np.copy()
    for k in id_map.keys():
        g = np.where(data_np== k)
        new_data[g]=id_map[k]

    # NumPy 阵列转为 SimpleITK 影像
    sitkImage = sitk.GetImageFromArray(new_data,
    isVector=img.GetNumberOfComponentsPerPixel()>1)
    sitkImage.SetOrigin(tuple(img.GetOrigin()))
    sitkImage.SetSpacing(tuple(img.GetSpacing()))
    sitkImage.SetDirection(img.GetDirection())
    sitk.WriteImage(sitkImage,output_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--input_file', help= "source labelmap file", required=False)
    parser.add_argument('-o', "--output_file", required=False, help="target labelmap file")
    parser.add_argument('-m', '--mapping_file', help='id mapping file.',required=False)

    args = parser.parse_args()
    # input_file = args.input_file
    # output_file = args.output_file
    # mapping_file = args.mapping_file
    id_map = read_txt(args.mapping_file)
    chanage_nii_label(args.input_file,args.output_file,id_map)

if __name__ == '__main__':
    main()

    