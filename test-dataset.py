import h5py
f=h5py.File("myh5py.hdf5","w")
#deset1是数据集的name，（20,）代表数据集的shape，i代表的是数据集的元素类型
d1=f.create_dataset("dset1", (20,), 'i')
for key in f.keys():
    print(key)
    print(f[key].name)
    print(f[key].shape)
    print(f[key][()])

# 输出：
# dset1
# /dset1
# (20,)
# [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]