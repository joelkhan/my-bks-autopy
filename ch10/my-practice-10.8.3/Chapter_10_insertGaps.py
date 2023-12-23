'''
Chapter 10 Organizing Files

Insert Gaps

As an added challenge, write another program that can insert gaps
into numbered files so that a new file can be added.

10.8.3 的附加挑战
编写另一个程序，在一些连续编号的文件中空出一些编号，以便加入新的文件。

'''

# insertGaps.py - Inserts a gap in sequence of numbered files with the 
# given prefix. It uses mostly the functions of fillingGaps. The renamed 
# files are moved temporarily into a temp dir.  
# Usage: python insertGaps.py rootDir filenamePrefix gapAt

import os, shutil, sys
from operator import itemgetter
from pathlib import Path
import fillingGaps as fg    # 导入了fillingGaps

if __name__ == "__main__":

    if(len(sys.argv) == 4):

        rootDirPath =  Path(sys.argv[1]).absolute()
        filenamePrefix = sys.argv[2]
        gapAt = int(sys.argv[3])

        fileList = fg.findMatchingFiles(rootDirPath, filenamePrefix)
        sortedFileList = sorted(fileList, key=itemgetter(int(2)))
        lengthIntLiteral = fg.getLongestIntLiteral(sortedFileList)

        # 构建一个临时目录
        tempDirPath = Path(os.path.join(rootDirPath, 'temp'))
        if(os.path.exists(tempDirPath)):
            tempDirPath.rmdir()
        tempDirPath.mkdir()

        # Move the renamed files into a temp-dir, so that they are not 
        # overwritten by themselves.
        # xxx4.txt --> xxx5.txt --> xx6.txt 
        fg.renameFiles(sortedFileList, lengthIntLiteral, 
            os.path.join('temp/' + filenamePrefix), gapAt=gapAt)
        
        # Move the files back to the original dir
        for fn in os.listdir(tempDirPath):
            shutil.move(os.path.join(tempDirPath, fn), rootDirPath)

        tempDirPath.rmdir()

    else:
        print('Usage: python insertGaps.py rootDir filenamePrefix gapAt')


