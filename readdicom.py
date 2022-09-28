#%%
from typing import List
import numpy as np
import SimpleITK as sitk
img = sitk.ReadImage(fileName= "./data/I001")
print(type(img)) # <class 'SimpleITK.SimpleITK.Image'>

# %%
data_np = sitk.GetArrayFromImage(img)
data_np = data_np.astype(np.float32)
print(data_np.shape)  # (1, 1067, 978) = (Slice index, Rows, Columns)
print(type(data_np),data_np.shape,data_np.dtype)
# %%
import matplotlib.pyplot as plt
data_np = data_np.squeeze()
print(data_np.shape) 
plt.imshow(data_np,cmap='gray')
plt.show
#%%
a = 5
print(f"{a}")
print("{}".format(a,))
print("%0.3d"%a)
print("{:0.3d}".format(a))

#%%
import torch
from torch import nn, tensor
class_num = 7
alpha = torch.ones(class_num, 1) / class_num
alpha
#%%
one_hot_codes = torch.eye(class_num)

#%%
import torch
from torch import nn, tensor
a = torch.tensor([[1,2,3],[2,2,2]],dtype=float)
print(a.shape)
b = torch.randn((5,))
print(b.data)
b =b.long()
print(b.data)
x = torch.eye(15)/2
print(x.data)
print(x.shape)
print(b.shape)
bx = x[b.data]
print(bx.shape)
print(bx)
#%%
import numpy as np
import SimpleITK as sitk
img = sitk.ReadImage(fileName= "./data/CT_112_0000_label.nii.gz")
print(type(img)) # <class 'SimpleITK.SimpleITK.Image'>
data_np = sitk.GetArrayFromImage(img)

b = np.where(data_np == 3,8,data_np)

# NumPy 阵列转为 SimpleITK 影像
sitkImage = sitk.GetImageFromArray(b,
  isVector=img.GetNumberOfComponentsPerPixel()>1)
sitkImage.SetOrigin(tuple(img.GetOrigin()))
sitkImage.SetSpacing(tuple(img.GetSpacing()))
sitkImage.SetDirection(img.GetDirection())
sitk.WriteImage(sitkImage,"./data/CT_112_0000_label_2.nii.gz")
#%%
from typing import List
import os
import SimpleITK as sitk
import numpy as np

def subfiles(folder: str, join: bool = True, prefix: str = None, suffix: str = None, sort: bool = True) -> List[str]:
    if join:
        l = os.path.join
    else:
        l = lambda x, y: y
    res = [l(folder, i) for i in os.listdir(folder) if os.path.isfile(os.path.join(folder, i))
           and (prefix is None or i.startswith(prefix))
           and (suffix is None or i.endswith(suffix))]
    if sort:
        res.sort()
    return res

nii_gz_files = subfiles("C:/Users/Bxd/Desktop/1",".nii.gz")

for name in nii_gz_files:
  print(name,"\n")
  # 读取图像
  ct_img = sitk.ReadImage(fileName= name)
  ct_array = sitk.GetArrayFromImage(ct_img)
  origin = ct_img.GetOrigin()
  direction = ct_img.GetDirection()
  space = ct_img.GetSpacing()
  print(type(direction))
  M1 = np.array(direction,dtype=float)
  M2 = np.array([-1,0,0,0,-1,0,0,0,1])

  M3 = np.multiply(M2, M1)
  direction = tuple(M3.tolist())
  print(direction)
  # 保存图像
  saved_img = sitk.GetImageFromArray(ct_array)
  saved_img.SetOrigin(origin)
  saved_img.SetSpacing(space)
  saved_img.SetDirection(direction)

  sitk.WriteImage(saved_img, name)





#%%
# 读取图像
# ct = sitk.ReadImage(filename)
# ct_array = sitk.GetArrayFromImage(ct)
# print(ct_array.shape)  # [z,y,x]



# # 保存图像
# savedImg = sitk.GetImageFromArray(ct_array)
# savedImg.SetOrigin(origin)
# savedImg.SetDirection(direction)
# savedImg.SetSpacing(space)
# sitk.WriteImage(savedImg, saved_name)

#