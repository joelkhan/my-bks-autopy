#! python3
# backupToZip.py
# Copies an entire folder and its contents into
# a zip file whose filename increments.

import zipfile, os

def backupToZip(folder):
    # 我这里给函数传递了一个绝对路径
    # 这导致了在最后的zip中也包含的是一个绝对路径
    # Backup the entire contents of "folder" into a zip file.

    print("1, " + folder)
    folder = os.path.abspath(folder) # make sure folder is absolute
    print("2, " + folder)

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
        print('Adding files in %s...' % (foldername))
        # Add the current folder to the ZIP file.
        backupZip.write(foldername)

        # Add all the files in this folder to the ZIP file.
        for filename in filenames:
            if filename.startswith(os.path.basename(folder) + '_') and filename.endswith('.zip'):
                continue # don't backup the backup ZIP files
            backupZip.write(os.path.join(foldername, filename))
    backupZip.close()
    print('Done.')


#backupToZip('C:\\delicious')

#Path(r'/home/joel/src/my-bks/my-bks-autopy/ch10/delicious')
backupToZip(r'/home/joel/src/my-bks/my-bks-autopy/ch10/delicious')


