import os
import random
import string
import sys

def path_validator(p):
  if os.path.isdir(p):
    # return the normalized path including safe case sensitivity
    return os.path.normpath(os.path.normcase(p))
  else:
    raise argparse.ArgumentTypeError('Path location incorrect')

def name_size_validator(s):
  """ This function validates the folder_name/folder_sizes argument to de format
  <name1>,<size1>,<name2>,<size2>..."""

  # Warning: this depends on OS's ASCII table definition
  LEGAL_CHARS = ('-_.() ' +
                  string.ascii_uppercase +
                  string.ascii_lowercase +
                  string.digits)

  l = s.split(',')

  # The length of l should be even and names must be different
  raw_folder_names = l[::2]
  raw_folder_sizes = l[1::2]

  if len(set(raw_folder_names)) != len(raw_folder_sizes):
    raise argparse.ArgumentTypeError('There is one missing or repeated folder-name/folder-size')

  # Taking away illegal chars
  folder_names = []
  for name in raw_folder_names:
    new_name = ''.join(c for c in name if c in LEGAL_CHARS)
    if len(new_name) == 0:
      raise argparse.ArgumentTypeError("Folder's name contains only illegal characters")
    else:
      folder_names.append(new_name)

  # Validate sizes as integer type
  folder_sizes = []
  for size in raw_folder_sizes:
    try:
      folder_sizes.append(int(size))
    except Exception as e:
      sys.stdout.write(e)
      raise argparse.ArgumentTypeError("Folder's SIZE is not an integer")

  return dict(zip(folder_names, folder_sizes))

def rand_string():
  """This function generates a random string with random length"""
  # Test does not says the max length of the alphanumeric string
  # or upper case or lower case.
  # I took liberties on both cases: 128 max length, upper and lower cases
  length = random.randint(1, 128)
  # SystemRandom() is more cryptographically secure because depends on the OS
  return (''.join( random.SystemRandom().choice(
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits) for _ in range(length)) + '\n')

def file_filler(path, folder_name, folder_size, file_size):
  # Creates file into the sub-folder
  num_file = folder_size // file_size
  last_file = folder_size % file_size

  for n in range(1,num_file + 1):
    file_path = os.path.join(path, folder_name, 'file' + str(n))
    if os.path.isfile(file_path) and os.path.getsize(file_path)//1048576 == file_size:
      continue
    elif os.path.isfile(file_path) and os.path.getsize(file_path)//1048576 < file_size:
      acum_file = os.path.getsize(file_path)
    elif not os.path.isfile(file_path):
      acum_file = 0
    try:
      file_handle = open(file_path, 'a')
      while acum_file < file_size*1048576:
        line = rand_string()
        line_size = len(line)
        try:
          file_handle.write(line)
          acum_file += line_size
        except Exception as e:
          sys.stdout.write(str(e)+'\n')
      file_handle.close()
    except Exception as e:
      sys.stdout.write(str(e)+'\n')
  if last_file:
    try:
      file_handle = open(os.path.join(path, folder_name, 'file' + str(num_file + 1)), 'w')
      acum_file = 0
      while acum_file < last_file*1048576:
        line = rand_string()
        line_size = len(line)
        try:
          file_handle.write(line)
          acum_file += line_size
        except Exception as e:
          sys.stdout.write(str(e)+'\n')
      file_handle.close()
    except Exception as e:
      sys.stdout.write(str(e)+'\n')
  return

def folder_creator(path, folder_names):
  """ Create sub-folders per each folder-name passed to de program """

  for name in folder_names:
    try:
      os.mkdir(os.path.join(path,name))
    except Exception as e:
      sys.stdout.write(e)
      sys.stdout.write('Folder ' + name + ' already exist' +'\n')
      pass
  return

def main(args):
  # Verify folder sizes > 0
  if min(args.folders[0].values()) <= 0:
    sys.stdout.write('Some sub-folder size is zero or less. Quitting now...')
    sys.exit('\n')

  # verify the disk space available
  fs_stats = os.statvfs(args.path[0])
  free_space = fs_stats.f_bavail * fs_stats.f_frsize
  projected_space = sum( list( args.folders[0].values() ) )*1048576
  ratio = (free_space - projected_space)*1.0/free_space if free_space!=0 else -1

  if ratio < 0.1 and ratio >= 0.0:
    sys.stdout.write('After execution 90% of available disk space will be used. Quitting now...')
    sys.exit('\n')
  elif ratio < 0:
    sys.stdout.write('Not enough space available on disk. Quitting now...')
    sys.exit('\n')

  # Create sub-folders
  folder_creator(args.path[0],list(args.folders[0].keys()))

  # Create files
  file_data = {}
  for root, dirs, files in os.walk(args.path[0]):
    if len(files)>0:
      for name in files:
        file_data[os.path.basename(root)] = {}
      for name in files:
        file_data[os.path.basename(root)][name] = os.path.getsize(os.path.join(root, name))

  old_folders = list(file_data.keys())
  file_size = max(list(file_data[old_folders[0]].values()))//1048576

  for name in args.folders[0]:
    if name in old_folders:
      folder_size = args.folders[0][name] + sum(file_data[name].values())//1048576
    else:
      folder_size = args.folders[0][name]
    file_filler(args.path[0], name, folder_size, file_size)
  return

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(description = 'Add more folders and files to dataset')
  parser.add_argument('path',
    metavar='PATH',
    type=path_validator,
    nargs=1,
    default=os.getcwd(),
    help='Path to location of Master Dataset. Default is the current working path')

  parser.add_argument('folders',
    metavar='SUB-FOLDERS',
    type=name_size_validator,
    nargs=1,
    help='Sub-folders in the Master Dataset in the format <name1>,<size1>,<name2>,<size2>... where <name> represents a folder name and <size> represent a size in megabytes')

  main(parser.parse_args())
