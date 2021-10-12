import h5py
import numpy as np

#===========================================================================
# Read HDF5 file.
f = h5py.File("LinearTransform_3.h5", "r")    # mode = {'w', 'r', 'a'}

# Print the keys of groups and datasets under '/'.
print(f.filename, ":")
print([key for key in f.keys()], "\n")

#===================================================
# Read dataset 'dset' under '/'.
d = f["TransformGroup"]

# Print the data of 'dset'.
print(d.name, ":")
print(d[:])

# Print the attributes of dataset 'dset'.
for key in d.attrs.keys():
	print(key, ":", d.attrs[key])
print("\n")

#===================================================
# Read group 'bar1'.
g = f["bar1"]

# Print the keys of groups and datasets under group 'bar1'.
print([key for key in g.keys()])

# Three methods to print the data of 'dset1'.
print(f["/bar1/dset1"][:])		# 1. absolute path

print(f["bar1"]["dset1"][:])  # 2. relative path: file[][]

print(g['dset1'][:])		# 3. relative path: group[]

# Delete a database.
# Notice: the mode should be 'a' when you read a file.
'''
del g["dset1"]
'''

# Save and exit the file
f.close()

if __name__ == "__main__":
    main()
