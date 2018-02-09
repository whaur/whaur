import os
import argparse
from functools import reduce

def get_directory_structure(rootdir):
    dir_list = {}
    rootdir = rootdir.rstrip(os.path.sep)
    start = rootdir.rfind(os.path.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        filelist = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir_list)
        parent[folders[-1]] = filelist
    return dir_list

def get_length(dictionary, contents):
    if contents:
        cnt = len(dictionary)
    else:
        cnt = 0
        for key, value in dictionary.items():
            if isinstance(value, dict):
                cnt += 1
    return cnt

def get_leader(depth, last):
    if depth == 0:
        return ''
    if last:
        return '└── '
    return '├── '

def get_indent(depth, indent, last):
    if depth <= 1:
        return ''
    if last:
        return indent + ' '*4
    return indent + '|' + ' '*3

# Symbols for ascii art: ├ , ─ , └
def print_dict(dictionary, contents, depth=0, last_parent=False, indent=''):
    cnt = 1
    mcnt = get_length(dictionary, contents)
    indent = get_indent(depth, indent, last_parent)
    for key, value in sorted(dictionary.items()):
        leader = get_leader(depth, cnt==mcnt)
        if isinstance(value, dict):
            print('%s%s%s/' %(indent, leader, key))
            if depth < 1:
                shift = 0
            else:
                shift = 4
            print_dict(value, contents, depth+1, cnt==mcnt, indent)
            cnt += 1
        elif contents:
            print('%s%s%s' %(indent, leader, key))
            cnt += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true', default=False,
                        dest='include_files')
    args = parser.parse_args()
    nested = get_directory_structure(os.getcwd())
    print_dict(nested, args.include_files)

if __name__ == '__main__':
    main()
