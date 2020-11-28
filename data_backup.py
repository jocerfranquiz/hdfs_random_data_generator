import filecmp
import os
import random
import shutil
import string
import sys


def path_validator(p):
  if os.path.isdir(p):
    # return the normalized path including safe case sensitivity
    return os.path.normpath(os.path.normcase(p))
  else:
    raise argparse.ArgumentTypeError('Path location incorrect')

def main(args):

  source = args.source[0]
  origin = os.path.basename(source)
  source += os.sep

  destiny = args.destiny[0]

  for root, folders, files in os.walk(source):
    if os.path.isabs(destiny):
      backup_path = os.path.join(destiny, origin, root.replace(source,''))
    else:
      backup_path = os.path.join(root, destiny)
    # Create new directories
    if not os.path.exists(backup_path):
      os.makedirs(backup_path)

    folders = [d for d in folders if d != backup_path]
    for f in files:
      file_path = os.path.join(root, f)
      dest_path = os.path.join(backup_path, f)
      for index in range(100):
        current_backup = '{0}.{1:02d}'.format(dest_path, index)
        absolute_path = os.path.abspath(file_path)

        if index > 0:
          prev_backup = '{0}.{1:02d}'.format(dest_path, index-1)
          if not os.path.exists(prev_backup):
            break
          absolute_path = os.path.abspath(prev_backup)

          try:
            if os.path.isfile(absolute_path) and filecmp.cmp(absolute_path, file_path, shallow = False):
              continue
          except OSError:
            pass

        try:
          if not os.path.exists(current_backup):
            sys.stdout.write('{0} ---> {1}\n'.format(file_path, current_backup))
            shutil.copy(file_path, current_backup)
        except Exception as e:
          sys.stdout.write(e)

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(description = 'Backup dataset with versioning upto 100')
  parser.add_argument('source',
    metavar='PATH',
    type=path_validator,
    nargs=1,
    default=os.getcwd(),
    help='Path to location of Master Dataset. Default is the current working path')

  parser.add_argument('destiny',
    metavar='PATH',
    type=path_validator,
    nargs=1,
    default=os.getcwd(),
    help='Path to location of Master Dataset. Default is the current working path')

  main(parser.parse_args())


# TODO add an ignore files parameter
# TODO validate disk space
# TODO Rotate versions
