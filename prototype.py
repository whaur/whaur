import os
from functools import reduce

def get_directory_structure(rootdir):
    dir_list = {}
    rootdir = rootdir.rstrip(os.path.sep)
    start = rootdir.rfind(os.path.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir_list)
        parent[folders[-1]] = subdir
    return dir_list

def print_dict(dictionary, ident = '', braces=1):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print('%s%s%s%s' %(ident,braces*'[',key,braces*']'))
            print_dict(value, ident+'  ', braces+1)
        else:
            print(ident+'%s = %s' %(key, value))

def main():
    nested = get_directory_structure(os.getcwd())
    print_dict(nested)

if __name__ == '__main__':
    main()
