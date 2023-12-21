'''
Chapter 10 Organizing Files

Filling in the Gaps

Write a program that finds all files with a given prefix, such as spam001.txt,
spam002.txt, and so on, in a single folder and locates any gaps in the 
numbering (such as if there is a spam001.txt and spam003.txt but no spam002.txt).
Have the program rename all the later files to close this gap.

10.8.3 消除缺失的编号
    编写一个程序， 在一个文件夹中找到所有带指定前缀的文件，如spam001.txt, spam002.txt等，
并定位缺失的编号（例如存在spam001.txt和spam003.txt，但不存在spam002.txt）。让该程序对后面
的所有文件重命名，消除缺失的编号。
    作为附加的挑战（见insertGaps），编写另一个程序，在一些连续编号的文件中空出一些编号，
以便加入新的文件。

'''

# fillingGaps.py - Renames all files with the given prefix in a dir, 
# so there are no gaps in the numbering sequence. It checks where the 
# sequence start and pads all files to the same length of leading zeros 
# Usage: python fillingGaps.py rootDir filenamePrefix

import sys, os, re, shutil
from pathlib import Path
from operator import itemgetter
import logging

logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')


def findMatchingFiles(rootDir, filenamePrefix):
    ''' Matches the files in the rootDir to the given prefix and
        returns a list with the Path, integer literal, the integer literal 
        as int and the suffix of the filename.
        找到所有匹配的文件，保存到列表的列表中
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
def renameFiles(sortedFileList, lengthIntLiteral, filenamePrefix, gapAt=0):
    ''' Loops through every file in the list. If the number in
        the file name is not the next in the sequence or hasn't the right 
        amount of leading zeros renames it. 
        这里的逻辑不是移动（那样想就复杂了），而是简单的重命名，解释如下：
        （1）移动是指，如果有001和004，那么需要把004重命名为002
        （2）重命名是指，已知存在001，那么紧跟其后的项就应该是002，
        无论它本身的编号是多少，这个逻辑成立的前提是该列表必须已排序。
    '''

    # Find out where the sequence begins
    # 确定第一个编号，它不一定是1
    start = sortedFileList[0][2]

    # 这个gapAt感觉有些问题
    # 如果文件列表的编号就是100开始的，
    # 前4个文件分别是 100, 101, 102, 106, 怎么办？
    if(gapAt is not 0):
        sortedFileList = sortedFileList[gapAt-sortedFileList[0][2]:]
        start=gapAt-1+start

    # 这个start应该是定义了迭代的起点
    for i, gapFile in enumerate(sortedFileList, start=start): 
            ''' Check if the index is not the same as the number OR
                the length of the integer literal is not the length of the longest 
                integer literal in the list
            '''
            # 下面的if中，
            # 第1个条件是判断序号是否正确
            # 第2个条件是判断序号的格式是否正确
            if (i is not gapFile[2] or len(gapFile[1]) is not lengthIntLiteral):
                # i:0{lengthNumber} pads the new number to the length of the longest int literal
                # 如果格式不对，在i前面补足0
                src = gapFile[0]
                dest = Path(os.path.dirname(gapFile[0])) / f'{filenamePrefix}{i:0{lengthIntLiteral}}{gapFile[3]}'
                logging.info(f'renaming {src.name} to {dest.name}')
                shutil.move(src, dest)

if __name__ == "__main__":
    if(len(sys.argv) == 3):
        rootDir = Path(sys.argv[1])
        filenamePrefix = sys.argv[2]

        gapFileList = findMatchingFiles(rootDir, filenamePrefix)

        # Sort the list of files by the number
        sortedFileList = sorted(gapFileList, key=itemgetter(int(2)))
        lengthIntLiteral = getLongestIntLiteral(sortedFileList)
        renameFiles(sortedFileList, lengthIntLiteral, filenamePrefix)

    else:
        print('Usage: python fillingGaps.py rootDir filenamePrefix')


