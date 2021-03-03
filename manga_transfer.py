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

MANGA_PATH = '/mnt/nasHDD/manga/'
AMT_PATH = str(pathlib.Path(__file__).parent.absolute())

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

    with open(AMT_PATH + '/auth.json', 'w') as f:
        f.write(json.dumps(credentials, indent=4))

def get_credentials():
    f = open(AMT_PATH + '/auth.json', 'r')
    credentials = json.load(f)

    f.close()
    return credentials

def is_fractioned(path):
    chapters = os.listdir(path)

    for chap in chapters:
        if "-" in chap:
            return True

    return False

def get_mangas():
    return [name for name in os.listdir(MANGA_PATH)
            if os.path.isdir(os.path.join(MANGA_PATH, name))]

def print_mangas():
    os.system("ls " + MANGA_PATH)

def main():
    global MANGA_PATH, AMT_PATH

    if len(sys.argv) == 2:
        if sys.argv[1] == 'register':
            register()
        if sys.argv[1] == 'list':
            print_mangas()

    elif len(sys.argv) >= 3:
        path = MANGA_PATH + sys.argv[1] + '/'
        start_idx = int(sys.argv[2])

        fractioned = is_fractioned(path)
        chapters = os.listdir(path)

        if len(sys.argv) == 3:
            end_idx = int(sys.argv[2])
        else:
            end_idx   = int(sys.argv[3])

        credentials = get_credentials()
        with pysftp.Connection(**credentials, cnopts=cnopts) as sftp:
            cprint('Connection established ... ', 'white', attrs=['bold'])
            # cd to folder in device
            sftp.cwd('Pictures/manga/')

            # put each chapter
            for i in range(start_idx, end_idx+1):
                chapter_dir = f'chapter_{str(i).zfill(4)}-'
                if start_idx >= 1000:
                    chapter_dir = f'chapter_{str(i).zfill(5)}-'

                for chap in [x for x in chapters if chapter_dir in x]:
                    localpath = path + chap
                    remotepath = chap
                    cprint(f'* {chap} transfering ... *', 'blue', attrs=['bold'])
                    sftp.mkdir(remotepath)
                    sftp.put_r(localpath=localpath, remotepath=remotepath)

                    clr_line()
                    cprint(f'~ {chap} done! ~', 'green', attrs=['bold'])

    else:
        print(__doc__)

if __name__ == '__main__':
    main()
