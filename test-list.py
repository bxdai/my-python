lst =[ {'image': '/workspace/data/chest_19.nii.gz',  'label': 0},
{'image': '/workspace/data/chest_31.nii.gz',  'label': 1}]

i = 0
for l in lst:
    print(f"i:{i}\n{l}")
    print(f"{l['image']}")
    
    i+=1
