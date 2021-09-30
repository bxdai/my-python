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