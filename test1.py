import torch

# file =[{"ima":"ssss","label":"sdffsafsafs"}]
# print(len(file))

# print(type(writer))
# x = torch.randn(2,3)
# print(x)

# y = (x > 0.5).float()
# print(y)

w = torch.randn(1,98,98)
x = torch.randn(1,100,98)
# y = torch.cat([w,x])
n = torch.stack([w,x])
# print(y.shape)
print(n.shape)

#%%
import os
model_file = '/home/bian/project/data/nnUNet_trained_models/nnUNet/3d_lowres/Task135_KiTS2021/nnUNetTrainerV2__nnUNetPlansv2.1/fold_0/model_final_checkpoint.model'  
folder, f  = os.path.split(model_file)
print(f)
# %%
import torch
import torch.autograd.variable as Variable
t1 = torch.tensor([1])
t1 = t1.cuda()
print(t1)
a=Variable(torch.Tensor([1]),requires_grad=True).cuda()
a
# %%
ret = {'name': "bian"}
ret['input'] = torch.tensor([0.0,1.0,0.8])
ret['gt'] = torch.tensor([1.1,1.2,1.3])
ret[0]
# %%
import shutil
import os
import time
os.makedirs("./myTestidr",exist_ok=True)
time. sleep(5)
#shutil.rmtree("./myTestidr")
os.removedirs("./myTestidr")
# %%

def Add(a,b):
    return a+b
def Sub(a,b):
    return a-b


method={
    "add":Add,
    "sub":Sub
}


print(method["add"](1,2))
# %%


class A:

    def __init__(self) -> None:
        
        self.num = self.get_num()
        print(self.num)

    def get_num(self)->int:
        return 5

class B(A):
    def __init__(self) -> None:
        super().__init__()
    def get_num(self)->int:
        return 10

btest = B()
# %%
a = True

print(type(a))

# %%
import torch
import torch.nn as nn
conv1 = nn.Conv1d(in_channels=256, out_channels=100, kernel_size=2)
input = torch.randn(32, 35, 256)
input = input.permute(0, 2, 1)
output = conv1(input)
print(output.shape)
# %%
class CNN(nn.Module):
    def __init__(self):
        nn.Model.__init__(self)
 
        self.conv1 = nn.Conv2d(1, 6, 5)  # 输入通道数为1，输出通道数为6
        self.conv2 = nn.Conv2d(6, 16, 5)  # 输入通道数为6，输出通道数为16
        self.fc1 = nn.Linear(5 * 5 * 16, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # 输入x -> conv1 -> relu -> 2x2窗口的最大池化
        x = self.conv1(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        # 输入x -> conv2 -> relu -> 2x2窗口的最大池化
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        # view函数将张量x变形成一维向量形式，总特征数不变，为全连接层做准备
        x = x.view(x.size()[0], -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
#%%

import time
# 获取当前时间
current_time = int(time.time())
print(current_time) # 1631186249
# 转换为localtime
localtime = time.localtime(current_time)
# 利用strftime()函数重新格式化时间
dt = time.strftime('%Y-%m-%d-%H-%M-%S', localtime)
print(dt) # 返回当前时间：2021:09:09 19:17:29

# %%
import shutil
os.makedirs()
