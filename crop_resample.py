from cProfile import label
import os
import sys
import itk
import SimpleITK as sitk
# import itk.itkImagePython
# import itk.itkImageFunctionBasePython
import numpy as np
import itk.itkImagePython
from batchgenerators.utilities.file_and_folder_operations import subfiles
from tqdm import tqdm



def resample_label_and_volume(label_file:str,volume_file:str,output:str):
    
    label_file = label_file.replace("\\","/")
    volume_file =volume_file.replace("\\","/")
    output = output.replace("\\","/")
    save_label_file = os.path.join(output,label_file.split('/')[-2],label_file.split('/')[-1])
    save_volume_file = os.path.join(output,volume_file.split('/')[-2],volume_file.split('/')[-1])

    print(save_label_file)
    print(save_volume_file)
    
    input_image = itk.imread(label_file)
    input_size = itk.size(input_image)
    input_spacing = itk.spacing(input_image)
    input_origin = itk.origin(input_image)


    # x_min = 10000
    # x_max = -10000
    # y_min = 10000
    # y_max = -10000
    # z_min = 10000
    # z_max = -10000
    
    # pixelIndex = itk.Index[3]()


    # for i in range(input_size[0]):
    #     for j in range(input_size[1]):
    #         for k in range(input_size[2]):
    #             pixelIndex[0] = i
    #             pixelIndex[1] = j
    #             pixelIndex[2] = k
    #             v = input_image.GetPixel(pixelIndex)
    #             if v > 0:
    #                 if i < x_min:
    #                     x_min = i
    #                 if i > x_max:
    #                     x_max = i
    #                 if j < y_min:
    #                     y_min = j
    #                 if j > y_max:
    #                     y_max = j
    #                 if k < z_min:
    #                     z_min = k
    #                 if k > z_max:
    #                     z_max = k


    # img_len = input_size[0]*input_size[1]*input_size[2] - 1
    print(type(input_image))
    Dimension = input_image.GetImageDimension()

    data_np = itk.GetArrayFromImage(input_image)
    print(data_np.shape)
    g = np.where(data_np >= 1)
    assert data_np.shape[0] == input_size[2],"size error!" 
    Z,Y,X = g

    x_min = np.array(X).min(axis=0)
    x_max = np.array(X).max(axis=0)


    y_min = np.array(Y).min(axis=0)
    y_max = np.array(Y).max(axis=0)

    z_min = np.array(Z).min(axis=0)
    z_max = np.array(Z).max(axis=0)


    x_len = int(x_max -x_min)
    y_len = int(y_max -y_min)
    z_len = int(z_max -z_min)




    # x_min = int(max(x_min-5,0))
    # x_max = int(min(x_max + 5,input_size[0]-1))

    # y_min = int(max(y_min-5,0))
    # y_max = int(min(y_max + 5,input_size[1]-1))

    # z_min = int(max(z_min-5,0))
    # z_max = int(min(z_max + 5,input_size[2]-1))


    # x_len = int(x_max -x_min)
    # y_len = int(y_max -y_min)
    # z_len = int(z_max -z_min)

    output_size = [x_len,y_len,z_len]
    #output_spacing = input_spacing
    #output_spacing = [1.0,1.0,1.0]#input_spacing
    output_spacing = input_spacing
    #output_origin = input_image.TransformIndexToPhysicalPoint([int(x_min-10),int(y_min-10),int(z_min-10)])
    output_origin = input_image.TransformIndexToPhysicalPoint([int(x_min),int(y_min),int(z_min)])
    print(f"x:{x_min},{x_max}")
    print(f"y:{y_min},{y_max}")
    print(f"z:{z_min},{z_max}")
    #output_origin = input_origin
    #output_origin = (0.0,0.0,0.0)

    interpolator_nearestNeighbor= itk.NearestNeighborInterpolateImageFunction.New(input_image)
    
    resampled_label = itk.resample_image_filter(
        input_image,
        #transform=scale_transform,
        interpolator=interpolator_nearestNeighbor,
        size=output_size,
        output_spacing=output_spacing,
        output_origin=output_origin,
    )
    itk.imwrite(resampled_label, save_label_file)

    # input_volume = itk.imread(volume_file)
    # #interpolator_linear = itk.LinearInterpolateImageFunction.New(input_volume)
    # interpolator_linear = itk.LinearInterpolateImageFunction[itk.Image[itk.SS,3], itk.D].New(input_volume)
    # resampled_volume = itk.resample_image_filter(
    #     input_volume,
    #     #transform=scale_transform,
    #     interpolator=interpolator_linear,
    #     size=output_size,
    #     output_spacing=output_spacing,
    #     output_origin=output_origin,
    # )
    
    # itk.imwrite(resampled_volume, save_volume_file)


def main():
    root_dir = "//192.168.100.4/label/standard/Task501_CTSpine1K/reviewed"
    target_dir = "//192.168.100.4/label/standard/Task501_CTSpine1K_mini_test/reviewed"
    label_dir = os.path.join(root_dir,"labelsTr")
    image_dir = os.path.join(root_dir,"imagesTr")
    file_list = subfiles(label_dir,join=False,suffix=".nii.gz")
    for i,it in enumerate(tqdm(file_list, desc='Processing')):
        label_file = os.path.join(label_dir,it)
        volume_file = os.path.join(image_dir,it[:-7]+"_0000.nii.gz")
        print(label_file)
        print(volume_file)
        if i == 2:
            
    
    #label_file = "D:/liver_169.nii.gz"
    label_file = "D:/1.3.6.1.4.1.9328.50.4.0003.nii.gz"
    volume_file = "D:/liver_169.nii.gz"
    target_dir = "D:/output"
    #resample_label_and_volume(label_file,volume_file,target_dir)  

    
    input_image = sitk.ReadImage(label_file)
    input_size = input_image.GetSize()
     # img_len = input_size[0]*input_size[1]*input_size[2] - 1
    print(type(input_image))
    Dimension = input_image.GetDimension()

    data_np = sitk.GetArrayFromImage(input_image)
    print(data_np.shape)
    g = np.where(data_np >= 1)
    assert data_np.shape[0] == input_size[2],"size error!" 
    Z,Y,X = g

    x_min = np.array(X).min(axis=0)
    x_max = np.array(X).max(axis=0)


    y_min = np.array(Y).min(axis=0)
    y_max = np.array(Y).max(axis=0)

    z_min = np.array(Z).min(axis=0)
    z_max = np.array(Z).max(axis=0)


    x_len = int(x_max -x_min)
    y_len = int(y_max -y_min)
    z_len = int(z_max -z_min)


    output_size = [x_len,y_len,z_len]

    #output_origin = input_image.TransformIndexToPhysicalPoint([int(x_min-10),int(y_min-10),int(z_min-10)])
    output_origin = input_image.TransformIndexToPhysicalPoint([int(x_min),int(y_min),int(z_min)])
    print(f"x:{x_min},{x_max}")
    print(f"y:{y_min},{y_max}")
    print(f"z:{z_min},{z_max}")

    label_file = label_file.replace("\\","/")

    target_dir = target_dir.replace("\\","/")
    save_label_file = os.path.join(target_dir,label_file.split('/')[-2],label_file.split('/')[-1])
    
    resample_label = resample_image(input_image,output_origin,output_size,is_label=True)
    sitk.WriteImage(resample_label, save_label_file)





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

    return resample.Execute(itk_image)



if __name__ == "__main__":
    main()