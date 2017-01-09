# Repo for Section of the test

This repo is for the first section of the test. It took me longer because I wanted to do it as profesional as I could. That means I added many validations to the input parameters, such as:

* Path validation
* Folder names without illegal characters
* Format of parameter `<name1>,<size1>,<name2>,<size2>...` (size, composition, etc.)
* Zero or negative size folders or files
* Available disk space

They are 3 Python scripts, one per section:

1. Data Generation (3 parameters)
  * `python data_generate.py <PATH> <FILE_SIZE> <FOLDER_NAME1>,<FOLDER_SIZE1>,<FOLDER_NAME2>,<FOLDER_SIZE>...`
2. Data Update (2 parameters)
  * `python data_update.py <PATH> <FOLDER_NAME1>,<FOLDER_SIZE1>,<FOLDER_NAME2>,<FOLDER_SIZE>...`
3. Data Backup (2 parameters)
  * `python data_backup.py <PATH_SOURCE> <PATH_DESTINATION>`

## Notes:
* For any script, you can call help with `-h` or `--help`, like this:
  * `python <PYTHHON_SCRIPT> -h`
* All parameters are mandatory. You can excecute the scripts with Python 2.7+ or Python 3.5+.
* These scripts where tested on Ubuntu Xenial 16.04
* Theoretically, they must run on Windows too (I repeat, theoretically)





