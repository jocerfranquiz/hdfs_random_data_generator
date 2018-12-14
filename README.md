# Random Generator of files and folders

They are 3 Python scripts:

1. Data Generation (3 parameters)
  * `python data_generate.py <PATH> <FILE_SIZE> <FOLDER_NAME_1>,<FOLDER_SIZE_1>,<FOLDER_NAME_2>,<FOLDER_SIZE_2>...`
2. Data Update (2 parameters)
  * `python data_update.py <PATH> <FOLDER_NAME_1>,<FOLDER_SIZE_1>,<FOLDER_NAME_2>,<FOLDER_SIZE_2>...`
3. Data Backup (2 parameters)
  * `python data_backup.py <PATH_SOURCE> <PATH_DESTINATION>`
  
I added many validations to the input parameters, such as:
* Path validation
* Folder names without illegal characters
* Format of parameter `<name_1>,<size_1>,<name_2>,<size_2>...` (size, composition, etc.)
* Zero or negative size folders or files
* Available disk space

## Notes:
* For any script, you can call help with `-h` or `--help`, like this:
  * `python <PYTHHON_SCRIPT> -h`
* All parameters are mandatory. You can excecute the scripts with Python 2.7+ or Python 3.5+.
* These scripts where tested on Ubuntu Xenial 16.04
* Theoretically, they must run on Windows too (I repeat, theoretically)





