
#%%
import yaml

def write_yaml_file(data:dict,filename:str =""):
    with open("./data/test.yaml","w",encoding="utf-8") as f:
        yaml.dump(config,f,sort_keys=True)

def read_config_file(input:str):
        with open(input,"r") as f:
            config = yaml.safe_load(f.read())
            #method = config['segmentataion']
            return config

config = read_config_file("./data/config.yaml")
print(type(config))

if config.get('landmark'):
    print('sb')
print(read_config_file("./data/config.yaml"))

config['nnunet']['history'] = '2022-8-30'
config['nnunet']['history'] ='2022-8-31'
write_yaml_file(config)
c = read_config_file("./data/model.yaml")

print(c['best_metric'])

#%%


import os

filename = "c:/a/b/c.txt"
print(os.path.basename(filename))




#%%
class A:
    def __init__(self,num:int = 0):
        self.n = num
        print("call init",self.n)
    def __call__(self):
        print("call call")
    def print_n(self):
        print("n=",self.n)


class B(A):
    def __init__(self,n)->None:
        super().__init__(n)
        print("call B init")
    def __call__(self)->None:
        print("call call B")

    def set_num(self,num):
        self.n = num


x =B(6)
x.set_num(9)
x.print_n()

#%%
a =1.000000009
b =1.00

print(a > b)
# %%
