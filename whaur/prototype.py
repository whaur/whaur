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

def get_length(dictionary, show_files, show_hidden):
    cnt = 0
    if show_files and show_hidden:
        cnt = len(dictionary)
    else:
        for key, value in dictionary.items():
            if key[0] != '.' and show_files:
                cnt += 1
            elif isinstance(value, dict):
                if key[0] != '.' or show_hidden:
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
def print_dict(dictionary, show_files, show_hidden, depth=0, last=False,
               indent=''):
    cnt = 1
    mcnt = get_length(dictionary, show_files, show_hidden)
    indent = get_indent(depth, indent, last)
    for key, value in sorted(dictionary.items()):
        leader = get_leader(depth, cnt==mcnt)
        if key[0] == '.' and not show_hidden:
            continue
        elif isinstance(value, dict):
            print('%s%s%s/' %(indent, leader, key))
            print_dict(value, show_files, show_hidden, depth+1, cnt==mcnt,
                       indent)
            cnt += 1
        elif show_files:
            print('%s%s%s' %(indent, leader, key))
            cnt += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store_true', default=False,
                        dest='show_files')
    parser.add_argument('-a', action='store_true', default=False,
                        dest='show_hidden')
    args = parser.parse_args()
    nested = get_directory_structure(os.getcwd())
    print_dict(nested, args.show_files, args.show_hidden)

if __name__ == '__main__':
    main()
