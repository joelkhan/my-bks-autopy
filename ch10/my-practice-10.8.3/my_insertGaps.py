'''
Chapter 10 Organizing Files

Insert Gaps

As an added challenge, write another program that can insert gaps
into numbered files so that a new file can be added.

10.8.3 的附加挑战
编写另一个程序，在一些连续编号的文件中空出一些编号，以便加入新的文件。
本程序将“result-A”中的文件拷贝到“result-B”，并在gapAt位置形成1个“空位”。
'''

# insertGaps.py - Inserts a gap in sequence of numbered files with the 
# given prefix. It uses mostly the functions of fillingGaps. The renamed 
# files are moved temporarily into a temp dir.  
# Usage: python insertGaps.py rootDir filenamePrefix gapAt

import os, shutil, sys
from operator import itemgetter
from pathlib import Path
import my_fillingGaps as fg    # 导入了my_fillingGaps
import logging as log

log.basicConfig(level=log.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')


def renameFiles_B(sortedFileList, lengthIntLiteral, filenamePrefix, gapAt, 
                    fromDir, toDir, tempDir):
    ''' Loops through every file in the list. If the number in
        the file name is not the next in the sequence or hasn't the right 
        amount of leading zeros renames it. 
        这里的逻辑不是移动（那样想就复杂了），而是简单的重命名，解释如下：
        （1）移动是指，如果有001和004，那么需要把004重命名为002
        （2）重命名是指，已知存在001，那么紧跟其后的项就应该是002，
        无论它本身的编号是多少，这个逻辑成立的前提是该列表必须已排序。
        
        注意：
        这个函数固定将整理后的文件复制到result-A目录
    '''
    #copyToDir = 'result-A'
    
    # Find out where the sequence begins
    # 确定第一个编号，它不一定是1
    start = sortedFileList[0][2]

    log.info(f'start: {start}')
    # 这个枚举了列表的每一项，并且使用start定义了第一次迭代的起点值
    # 比较高级的用法
    offset = 0
    for i, gapFile in enumerate(sortedFileList, start=start): 
        ''' Check if the index is not the same as the number OR
            the length of the integer literal is not the length of the longest 
            integer literal in the list
        '''
        # 下面的if中，
        # 第1个条件是判断序号是否正确
        # 第2个条件是判断序号的格式是否正确
        log.info(f'curr i: {i}')
        if ( i == gapAt ):
            offset += 1
            #continue
        
        sn = i + offset
        src = gapFile[0]
        dest = Path(os.path.dirname(gapFile[0])) / \
            tempDir / \
            f'{filenamePrefix}{sn:0{lengthIntLiteral}}{gapFile[3]}'
        log.info(f'copy to temp-dir: {src} to {dest}')
        shutil.copy(src, dest)


if __name__ == "__main__":

    if(len(sys.argv) == 4):

        fromDir = 'result-A'
        toDir = 'result-B'
        tempDir = 'temp'
        
        rootDirPath = (Path(sys.argv[1]) / fromDir).absolute()
        filenamePrefix = sys.argv[2]
        gapAt = int(sys.argv[3])
        #log.info(f'args: {rootDirPath}, {filenamePrefix}, {gapAt}')

        fileList = fg.findMatchingFiles(rootDirPath, filenamePrefix)
        #log.info(f'{fileList}')
        sortedFileList = sorted(fileList, key=itemgetter(int(2)))
        log.info(f'sorted: {sortedFileList}')
        lengthIntLiteral = fg.getLongestIntLiteral(sortedFileList)
        log.info(f'{lengthIntLiteral}')
        
        # 构建一个临时目录
        tempDirPath = Path(os.path.join(rootDirPath, tempDir))
        if(os.path.exists(tempDirPath)):
            tempDirPath.rmdir()
        tempDirPath.mkdir()
        
        # Move the renamed files into a temp-dir, so that they are not 
        # overwritten by themselves.
        # xxx4.txt --> xxx5.txt --> xx6.txt 
        #fg.renameFiles(sortedFileList, lengthIntLiteral, 
        #    os.path.join('temp/' + filenamePrefix), gapAt=gapAt)
        renameFiles_B(sortedFileList, lengthIntLiteral, filenamePrefix, gapAt, 
            fromDir, toDir, tempDir)
        
        log.info(f'tempDirPath: {tempDirPath}')
        toDirPath = (Path(sys.argv[1]) / toDir).absolute()
        log.info(f'toDirPath: {toDirPath}')
        # Move the files back to the original dir
        for fn in os.listdir(tempDirPath):
            log.info(f'move all files to dir result-B: \
                {os.path.join(tempDirPath, fn)} to {toDirPath}')
            shutil.move(os.path.join(tempDirPath, fn), toDirPath)

        log.info(f'finally, let me remove temp-dir: {tempDirPath}')
        tempDirPath.rmdir()
        #sys.exit()

    else:
        print('Usage: python my_insertGaps.py . spam gapAt')


