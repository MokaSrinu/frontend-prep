import os
import stat
print(os.getcwd())  # Returns the present working directory
print(os.getcwdb()) # returns the present working directory as a byte object


os.chdir('/Users/srinu/Documents/frontend-prep/backend/python') # use to change directory
print(os.getcwd())
print(os.listdir()) # lists all files and sub-directories inside a directory

os.mkdir('test_folder') # used to make a new directory

os.rename('test_folder', 'New_folder') # used to rename a directory

os.chmod('New_folder', stat.S_IRWXU) # used to change permissions of a file

os.remove('Test.txt') # used to remove a file

os.rmdir('Test.txt') # used to remove a directory
