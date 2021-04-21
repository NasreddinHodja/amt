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
import json
from rich.console import Console
from rich.progress import Progress

def clr_line():
  print ("\033[A                                            \033[A")

def register():
  global credentials
  credentials = {}
  console.print('[red bold]Please register your credentials[/red bold]')
  console.print('[blue bold] * host: [/blue bold]')
  credentials['host'] = input()
  console.print('[blue bold] * port: [/blue bold]')
  credentials['port'] = int(input())
  console.print('[blue bold] * username: [/blue bold]')
  credentials['username'] = input()
  console.print('[blue bold] * password: [/blue bold]')
  credentials['password'] = input()
  console.print('[blue bold] * local manga directory: [/blue bold]')
  credentials['manga_path'] = input()
  if credentials['manga_path'][-1] != "/":
    credentials['manga_path'] += "/"


  with open(AMT_PATH + '/auth.json', 'w') as f:
    f.write(json.dumps(credentials, indent=4))

def get_credentials():
  global MANGA_PATH, credentials
  f = open(AMT_PATH + '/auth.json', 'r')
  credentials = json.load(f)

  f.close()
  MANGA_PATH = credentials.pop("manga_path")

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

def init():
  global MANGA_PATH, AMT_PATH, cnopts, console, credentials

  # disable public key requirement
  cnopts = pysftp.CnOpts()
  cnopts.hostkeys = None

  AMT_PATH = str(pathlib.Path(__file__).parent.absolute())

  console = Console()
  get_credentials()

def main():
  init()

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

    with pysftp.Connection(**credentials, cnopts=cnopts) as sftp:
      console.print('[green bold]Connection established ...')
      # cd to folder in device
      sftp.cwd('Pictures/manga/')

      # put each chapter
      with Progress(console=console, expand=True, transient=True) as progress:
        task = progress.add_task("[bold white]transfering...", total=(end_idx+1-start_idx))
        for i in range(start_idx, end_idx+1):
          chapter_dir = f'chapter_{str(i).zfill(4)}-'
          if start_idx >= 1000:
            chapter_dir = f'chapter_{str(i).zfill(5)}-'

          for chap in [x for x in chapters if chapter_dir in x]:
            localpath = path + chap
            remotepath = chap
            # console.print(f'[blue bold]* {chap} transfering ... *[/blue bold]')
            sftp.mkdir(remotepath)
            sftp.put_r(localpath=localpath, remotepath=remotepath)

            # clr_line()
            # console.print(f'[green bold]~ {chap} done! ~[/green bold]')

          # console.print(f"[blue bold]* {chapter_dir[:-1]} done!")
          progress.advance(task)
  else:
    print(__doc__)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
