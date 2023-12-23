'''
10.8.3 消除缺失的编号
    编写一个程序， 在一个文件夹中找到所有带指定前缀的文件，如spam001.txt, spam002.txt等，
并定位缺失的编号（例如存在spam001.txt和spam003.txt，但不存在spam002.txt）。让该程序对后面
的所有文件重命名，消除缺失的编号。
'''

import sys, os, re, shutil
from pathlib import Path
from operator import itemgetter
import logging as log


log.basicConfig(level=log.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')


def findMatchingFiles(rootDir, filenamePrefix):
    ''' Matches the files in the rootDir to the given prefix and
        returns a list with the Path, integer literal, the integer literal 
        as int and the suffix of the filename.
        找到所有匹配的文件，这些文件具有相同的格式：前缀+编号，
        找到后将它们保存到“列表的列表”中
    '''
    pattern = re.compile(r'(' + filenamePrefix + r')(\d+)(.*)')
    gapFileList = []

    for filename in os.listdir(rootDir):
        mo = pattern.match(filename)
        if mo is not None:
            intLiteral = mo.group(2)
            fileSuffix = mo.group(3)
            gapFileList.append(      # 列表的列表
                [Path(rootDir).resolve() / filename, # 内部列表包含4项
                intLiteral, int(intLiteral), fileSuffix])

    return gapFileList


def getLongestIntLiteral(sortedFileList):
    ''' Returns the size of the longest integer literal e.g. 0002 --> 4
        TODO: Maybe there is a shorter pythonic version
        获取最长的整数字面量（字符串）的值
    ''' 

    lengthIntLiteral = 0
    for sortedFile in sortedFileList:
        if len(sortedFile[1]) > lengthIntLiteral:
            lengthIntLiteral = len(sortedFile[1])
    return lengthIntLiteral


# 参数gapAt是在附加题使用的
def renameFiles_A(sortedFileList, lengthIntLiteral, filenamePrefix):
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
    copyToDir = 'result-A'
    
    # Find out where the sequence begins
    # 确定第一个编号，它不一定是1
    start = sortedFileList[0][2]

    
    log.info(f'start: {start}')
    # 这个枚举了列表的每一项，并且使用start定义了第一次迭代的起点值
    # 比较高级的用法
    for i, gapFile in enumerate(sortedFileList, start=start): 
        ''' Check if the index is not the same as the number OR
            the length of the integer literal is not the length of the longest 
            integer literal in the list
        '''
        # 下面的if中，
        # 第1个条件是判断序号是否正确
        # 第2个条件是判断序号的格式是否正确
        log.info(f'curr i: {i}')
        if ( (i != gapFile[2]) or \
            (len(gapFile[1]) is not lengthIntLiteral) ):
            # i:0{lengthNumber} pads the new number to the length of the longest int literal
            # 如果格式不对，在i前面补足0
            src = gapFile[0]
            dest = Path(os.path.dirname(gapFile[0])) / \
                copyToDir / \
                f'{filenamePrefix}{i:0{lengthIntLiteral}}{gapFile[3]}'
            #log.info(f'renaming {src.name} to {dest.name}')
            log.info(f'TRANSFer & copy: {src} to {dest}')
            shutil.copy(src, dest)
        else:
            src = gapFile[0]
            dest = Path(os.path.dirname(gapFile[0])) / \
                copyToDir / \
                os.path.basename(gapFile[0])
            log.info(f'just copy: {src} to {dest}')
            shutil.copy(src, dest)

if __name__ == "__main__":
    if(len(sys.argv) == 3):
        rootDir = Path(sys.argv[1])
        filenamePrefix = sys.argv[2]

        gapFileList = findMatchingFiles(rootDir, filenamePrefix)
        log.info(f'founded: {gapFileList}')
        log.info(f'total: {len(gapFileList)}')
        
        # Sort the list of files by the number
        sortedFileList = sorted(gapFileList, key=itemgetter(int(2)))
        log.info(f'founded: {sortedFileList}')
        log.info(f'total: {len(sortedFileList)}')
        
        lengthIntLiteral = getLongestIntLiteral(sortedFileList)
        log.info(f'Literal len: {lengthIntLiteral}')
        
        renameFiles_A(sortedFileList, lengthIntLiteral, filenamePrefix)

    else:
        print('Usage: python my_fillingGaps.py . spam')



