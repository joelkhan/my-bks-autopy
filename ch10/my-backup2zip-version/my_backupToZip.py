#! python3
# backupToZip.py
# Copies an entire folder and its contents into
# a zip file whose filename increments.

import zipfile, os

"""
  这个版本的backupToZip生成的结果zip文件中，包含了目标dir的相对路径
"""
def backupToZip(folder):
    # Backup the entire contents of "folder" into a zip file.

    print("1, " + folder)
    folder = os.path.abspath(folder) # make sure folder is absolute
    print("2, " + folder)
    print("base: " + os.path.basename(folder))
    print("dir: " + os.path.dirname(folder))
    dirname = os.path.dirname(folder)

    # Figure out the filename this code should used based on 
    # what files already exist.
    number = 1
    while True:
        # 取folder名作为文件名，这是合理的
        zipFilename = os.path.basename(folder) + '_' + str(number) + '.zip'
        # 这个检查会在程序运行的目录下进行
        if not os.path.exists(zipFilename):
            break
        number = number + 1

    # Create the zip file.
    print('Creating %s...' % (zipFilename))
    # 这个新创建的zipfile也会在程序运行的目录下
    # 注意，zipFilename是字符串，backupZip是ZipFile对象
    backupZip = zipfile.ZipFile(zipFilename, 'w')

    # Walk the entire folder tree and compress the files in each folder.
    for foldername, subfolders, filenames in os.walk(folder):
        # 这里walk的是一个绝对路径，
        # 导致foldername也是绝对路径
        # 进而导致了后续的write都是绝对路径
        #print('Adding files in %s...' % (foldername))
        # Add the current folder to the ZIP file.
        #backupZip.write(foldername)
        print("curr_dir: " + foldername[len(dirname)+1:])
        backupZip.write(foldername[len(dirname)+1:])

        # Add all the files in this folder to the ZIP file.
        for filename in filenames:
            if filename.startswith(os.path.basename(folder) + '_') and filename.endswith('.zip'):
                continue # don't backup the backup ZIP files
            #backupZip.write(os.path.join(foldername, filename))
            print("curr_dir, add...: " + os.path.join(foldername[len(dirname)+1:], filename))
            backupZip.write(os.path.join(foldername[len(dirname)+1:], filename))
    backupZip.close()
    print('Done.')

backupToZip(r'./delicious')


