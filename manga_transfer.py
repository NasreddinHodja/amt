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
from pathlib import Path

import pysftp
import json
from rich.console import Console
from rich.progress import Progress
from getpass import getpass

def clr_line():
  print ('\033[A                                            \033[A')

def register():
  global credentials
  credentials = {}
  console.print('[red bold]Please register your credentials[/red bold]')

  console.print('[blue bold] * host: [/blue bold]', end='')
  credentials['host'] = input()

  console.print('[blue bold] * port: [/blue bold]', end='')
  credentials['port'] = int(input())

  console.print('[blue bold] * username: [/blue bold]', end='')
  credentials['username'] = input()

  console.print('[blue bold] * password: [/blue bold]', end='')
  credentials['password'] = getpass(prompt='')

  console.print('[blue bold] * local manga directory: [/blue bold]', end='')
  credentials['source_path'] = str(Path(input()))

  console.print('[blue bold] * remote manga directory: [/blue bold]', end='')
  credentials['destination_path'] = str(Path(input()))

  with open(Path(AMT_PATH, 'auth.json'), 'w') as f:
    f.write(json.dumps(credentials, indent=4))

def get_credentials():
  global SOURCE_PATH, DESTINATION_PATH, credentials
  f = open(Path(AMT_PATH, 'auth.json'), 'r')
  credentials = json.load(f)

  f.close()
  SOURCE_PATH = Path(credentials.pop('source_path'))
  DESTINATION_PATH = Path(credentials.pop('destination_path'))

def print_mangas():
  os.system('ls ' + str(SOURCE_PATH))

def get_mangas():
  return os.listdir(SOURCE_PATH)

def max_chap(manga_path):
  return max([int(str(manga.split("-")[0])[8:]) for manga in os.listdir(manga_path)])

def init():
  global AMT_PATH, cnopts, console, credentials

  # disable public key requirement
  cnopts = pysftp.CnOpts()
  cnopts.hostkeys = None

  AMT_PATH = Path(__file__).parent.absolute()

  console = Console()
  if 'register' not in sys.argv:
    get_credentials()

def send_manga(manga_path, start_idx, end_idx):
  chapters = os.listdir(manga_path)
  with pysftp.Connection(**credentials, cnopts=cnopts) as sftp:
    console.print('[green bold]Connection established ...')
    sftp.cwd(str(DESTINATION_PATH))

    # put each chapter
    with Progress(console=console, expand=True, transient=True) as progress:
      task = progress.add_task('[bold white]transfering...', total=(end_idx+1-start_idx))
      for i in range(start_idx, end_idx+1):
        chapter_dir = f'chapter_{str(i).zfill(4)}-'

        for chap in [x for x in chapters if chapter_dir in x]:
          localpath = Path(manga_path, chap)
          remotepath = chap
          sftp.mkdir(remotepath)
          sftp.put_r(localpath=localpath, remotepath=remotepath)

        progress.advance(task)

def main():
  init()

  if len(sys.argv) == 2 and sys.argv[1] == 'register':
    register()
  elif len(sys.argv) == 2 and sys.argv[1] == 'list':
    print_mangas()
  elif sys.argv[1] in get_mangas():
    manga_path = Path(SOURCE_PATH, sys.argv[1])
    start_idx = 0
    end_idx = 0

    if len(sys.argv) == 2:
      end_idx = max_chap(manga_path)
    elif len(sys.argv) == 3:
      start_idx = int(sys.argv[2])
      end_idx = start_idx
    elif len(sys.argv) == 4:
      start_idx = int(sys.argv[2])
      end_idx = int(sys.argv[3])
    else:
      exit(1)

    send_manga(manga_path, start_idx, end_idx)

  else:
    print(__doc__)

if __name__ == '__main__':
  try:
    main()
    clr_line()
  except KeyboardInterrupt:
    pass
