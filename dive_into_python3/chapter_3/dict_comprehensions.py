import os
import glob

metadata = [(f, os.stat(f)) for f in glob.glob('*.py')]
# print(metadata[0])

metadata_dict = {f: os.stat(f) for f in glob.glob('*.py')}
print(type(metadata_dict))

print(list(metadata_dict.keys()))
print(metadata_dict['os.py'].st_size)

a_dict = {'a': 1, 'b': 2, 'c': 3}
print({value:key for key, value in a_dict.items()})

