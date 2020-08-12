import glob
import os
import time

print(os.getcwd())

print(os.path.expanduser('~'))

name = os.path.join('D:\PyCharm_projects\\up-stroke\dive_into_python3\chapter_3',
                   'examp.py')

print(os.path.split(os.getcwd()))

(dirname, filename) = os.path.split(name)

(shortname, extension) = os.path.splitext(filename)
print(shortname)
print(extension)

os.chdir('..')
print(glob.glob('*chapter*'))

metadata = os.stat('chapter_3')
print(metadata.st_mtime)
print(time.localtime(metadata.st_mtime))

print(os.path.realpath('os.py'))