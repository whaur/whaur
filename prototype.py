import os
import argparse
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

# Symbols for ascii art: ├ , ─ , └
def print_dict(dictionary, contents, indent=''):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print('%s%s' %(indent, key))
            print_dict(value, contents, indent+'  ')
        elif contents:
            print('%s%s = %s' %(indent, key, value))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true', default=False,
                        dest='include_files')
    args = parser.parse_args()
    nested = get_directory_structure(os.getcwd())
    print_dict(nested, args.include_files)

if __name__ == '__main__':
    main()
