import SimpleITK as sitk
import numpy as np
import itk.itkImagePython
from batchgenerators.utilities.file_and_folder_operations import subfiles
from tqdm import tqdm
import os



def resample_label_and_volume(label_file:str,volume_file:str,output:str):
    label_file = label_file.replace("\\","/")
    volume_file =volume_file.replace("\\","/")
    output = output.replace("\\","/")
    save_label_file = os.path.join(output,label_file.split('/')[-2],label_file.split('/')[-1])
    save_volume_file = os.path.join(output,volume_file.split('/')[-2],volume_file.split('/')[-1])

    if os.path.exists(save_label_file):
        return

    print(save_label_file)
    print(save_volume_file)

    label_image = sitk.ReadImage(label_file)
    volume_image = sitk.ReadImage(volume_file)
    input_size = label_image.GetSize()
     # img_len = input_size[0]*input_size[1]*input_size[2] - 1
    print(type(label_image))
    Dimension = label_image.GetDimension()

    data_np = sitk.GetArrayFromImage(label_image)
    print(data_np.shape)
    g = np.where(data_np >= 1)
    assert data_np.shape[0] == input_size[2],"size error!" 
    Z,Y,X = g


    x_min = int(np.array(X).min(axis=0))-5
    x_max = int(np.array(X).max(axis=0)) + 5


    y_min = int(np.array(Y).min(axis=0)) - 5
    y_max = int(np.array(Y).max(axis=0)) + 5

    z_min = int(np.array(Z).min(axis=0))- 5
    z_max = int(np.array(Z).max(axis=0))+ 5

    # x_min = int(np.array(X).min(axis=0))
    # x_max = int(np.array(X).max(axis=0))


    # y_min = int(np.array(Y).min(axis=0))
    # y_max = int(np.array(Y).max(axis=0)) 

    # z_min = int(np.array(Z).min(axis=0))
    # z_max = int(np.array(Z).max(axis=0))

    x_min = int(max(x_min,0))
    x_max = int(min(x_max,input_size[0] -1))
    y_min = int(max(y_min,0))
    y_max = int(min(y_max,input_size[1] -1))
    z_min = int(max(z_min,0))
    z_max = int(min(z_max,input_size[2] -1))

    x_len = int(x_max -x_min)
    y_len = int(y_max -y_min)
    z_len = int(z_max -z_min)

    output_size = [x_len,y_len,z_len]

    #output_origin = input_image.TransformIndexToPhysicalPoint([int(x_min-10),int(y_min-10),int(z_min-10)])
    output_origin = label_image.TransformIndexToPhysicalPoint([int(x_min),int(y_min),int(z_min)])
    #output_origin_2 = label_image.TransformContinuousIndexToPhysicalPoint([int(x_min),int(y_min),int(z_min)])
    print(f"x:{x_min},{x_max}")
    print(f"y:{y_min},{y_max}")
    print(f"z:{z_min},{z_max}")

    resample_label = resample_image(label_image,output_origin,output_size,is_label=True)
    sitk.WriteImage(resample_label, save_label_file)
    resample_volume = resample_image(volume_image,output_origin,output_size,is_label=False)
    sitk.WriteImage(resample_volume, save_volume_file)

def resample_image(itk_image,out_origin, out_len,out_spacing=[1.0, 1.0, 1.0],is_label=False):
    original_spacing = itk_image.GetSpacing()
    original_size = itk_image.GetSize()
    out_size = [
        int(np.round(out_len[0] * (original_spacing[0] / out_spacing[0]))),
        int(np.round(out_len[1] * (original_spacing[1] / out_spacing[1]))),
        int(np.round(out_len[2] * (original_spacing[2] / out_spacing[2])))
    ]
    # 上述也可以直接用下面这句简写
    #out_size = [int(round(osz*ospc/nspc)) for osz,ospc,nspc in zip(original_size, original_spacing, out_spacing)]

    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(out_spacing)
    resample.SetSize(out_size)
    resample.SetOutputDirection(itk_image.GetDirection())
    resample.SetOutputOrigin(out_origin)
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(itk_image.GetPixelIDValue())

    if is_label: # 如果是mask图像，就选择sitkNearestNeighbor这种插值
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else: # 如果是普通图像，就采用sitkBSpline插值法
        resample.SetInterpolator(sitk.sitkBSpline)
        #resample.SetInterpolator(sitk.sitkLinear)

    return resample.Execute(itk_image)

def main():
    root_dir = "//192.168.100.4/label/standard/Task501_CTSpine1K/reviewed"
    #target_dir = "//192.168.100.4/label/standard/Task501_CTSpine1K_mini_test/reviewed"
    target_dir = "//192.168.100.4/label/standard/Task501_CTSpine1K_mini_test2/reviewed"
    label_dir = os.path.join(root_dir,"labelsTr")
    image_dir = os.path.join(root_dir,"imagesTr")
    file_list = subfiles(label_dir,join=False,suffix=".nii.gz")
    for i,it in enumerate(tqdm(file_list, desc='Processing')):
        label_file = os.path.join(label_dir,it)
        volume_file = os.path.join(image_dir,it[:-7]+"_0000.nii.gz")
        print(label_file)
        print(volume_file)
        
        resample_label_and_volume(label_file,volume_file,target_dir)

if __name__ == "__main__":
    main()