import h5py
import numpy as np

# f = h5py.File("mytestfile.hdf5",'w')
# dset = f.create_dataset("mydataset", (100,), dtype='i')

# f.close()

with h5py.File("mytestfile.hdf5", "w") as f:
    dset =  f.create_dataset("mydataset", (100,), dtype='i')
    print(f"dset name:{dset.name}")
    print(f"f.name:{f.name}")

print("-"*10)

f = h5py.File('mydataset.hdf5', 'a')
grp = f.create_group("subgroup")
dset2 = grp.create_dataset("another_dataset", (50,), dtype='f')
print(f"dset2.name;{dset2.name}")

dset3 = f.create_dataset('subgroup2/dataset_three', (10,), dtype='i')
print(f"dset3.name:{dset3.name}")

dataset_three = f['subgroup2/dataset_three']

print(f.values())

for name in f:
    print(name)

print("-"*10)

for key in f.keys():
    print(key)

# for it in f.items():
#     it.count()
#     print(it.index(0))

for itr in iter(f):
    print(itr)

print("mydataset" in f)
print("somethingelse" in f)

print("subgroup/another_dataset" in f)



