"""
* Android Manga Transfer *

Usage:
    amt <manga> <start> <end>

Args:
    manga: manga dir
    start: start chapter
    end: end chapter
"""

import sys
import os
import pathlib

import pysftp
from termcolor import cprint
import json

# disable public key requirement
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

# credentials = {
#     'host'    : '192.168.1.100',
#     'port'    : 1234,
#     'username': 'nasredd1n',
#     'password': 'oceanboie'
# }

path = '/mnt/nasHDD/manga/'
amt_path = str(pathlib.Path(__file__).parent.absolute())

def clr_line():
    print ("\033[A                                            \033[A")

def register():
    credentials = {}
    cprint('Please register your credentials.', 'red', attrs=['bold'])
    cprint(' * host: ', 'blue', end='', attrs=['bold'])
    credentials['host'] = input()
    cprint(' * port: ', 'blue', end='', attrs=['bold'])
    credentials['port'] = int(input())
    cprint(' * username: ', 'blue', end='', attrs=['bold'])
    credentials['username'] = input()
    cprint(' * password: ', 'blue', end='', attrs=['bold'])
    credentials['password'] = input()

    with open(amt_path + '/auth.json', 'w') as f:
        f.write(json.dumps(credentials, indent=4))

def fill_zeros(n, size):
    res = str(n)
    while len(res) < size:
        res = '0' + res
    return res

def get_mangas():
    manga_dir = '/mnt/nasHDD/manga'
    return [name for name in os.listdir(manga_dir)
            if os.path.isdir(os.path.join(manga_dir, name))]

def print_mangas():
    mangas = get_mangas()
    options = []

    while len(mangas) > 0:
        col = []
        for i in range(5):
            col += [mangas.pop(0)]
            if len(mangas) == 0:
                break
        options += [col]

    col_width = max(len(word) for row in options for word in row) + 2  # padding
    for row in options:
        cprint(''.join(word.ljust(col_width) for word in row), 'blue', attrs=['bold'])

def main():
    global path, amt_path
    if len(sys.argv) == 2:
        if sys.argv[1] == 'register':
            register()
        if sys.argv[1] == 'list':
            print_mangas()

    elif len(sys.argv) >= 3:
        path = path + sys.argv[1] + '/'
        start_idx = int(sys.argv[2])

        if len(sys.argv) == 3:
            end_idx = int(sys.argv[2])
        else:
            end_idx   = int(sys.argv[3])

        with open(amt_path + '/auth.json', 'r') as f:
            credentials = json.load(f)
            with pysftp.Connection(**credentials, cnopts=cnopts) as sftp:
                cprint('Connection established ... ', 'white', attrs=['bold'])
                # cd to folder in device
                sftp.cwd('Pictures/manga/')

                # put each chapter
                for i in range(start_idx, end_idx+1):
                    chapter_dir = f'chapter_{fill_zeros(i, 4)}'
                    localpath = path + chapter_dir
                    remotepath = chapter_dir

                    cprint(f'* {chapter_dir} transfering ... *', 'blue', attrs=['bold'])
                    sftp.mkdir(remotepath)
                    sftp.put_r(localpath=localpath, remotepath=remotepath)

                    clr_line()
                    cprint(f'~ {chapter_dir} done! ~', 'green', attrs=['bold'])

    else:
        print(__doc__)

if __name__ == '__main__':
    main()
