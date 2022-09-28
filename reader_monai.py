from monai.data import ITKReader, PILReader
from monai.transforms import (Compose, EnsureChannelFirstd, EnsureTyped,
                              LoadImage, LoadImaged, Resized, SqueezeDim,AddChannel,)

filename = '/home/bian/nas/markrootTest/task503_feature_points/raw/IM_0077_20220825124433710_0000.nii.gz'
filename1 = '/home/bian/nas/markrootTest/task503_feature_points/raw/IM_0003_20220824142442515_0000.nii.gz'
filename3 = '/home/bian/nas/markrootTest/task503_feature_points/preprocessed/case_991_0000.nii.gz'
filename4 = '/home/bian/nas/markrootTest/task503_feature_points/preprocessed/case_991_0000.IMA'
filename5 = '/home/bian/project/fidetect2d/data/imagesTr/IM_0003_0000.nii.gz'
filename6 = '/home/bian/nas/markrootTest/task503_feature_points/raw/IM_0003_0000.nii.gz'

data, meta = LoadImage()(filename6)
print(f"image data shape:{data.shape}")
#print(f"meta data:{meta}")
adata = AddChannel()(data)
print(f"image data shape:{adata.shape}")
#sDim_data =  SqueezeDim(dim=-1)(data)
#print(f"image data shape:{sDim_data.shape}")