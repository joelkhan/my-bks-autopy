#! python3
# renameDates.py - Renames filenames with American MM-DD-YYYY date format
# to European DD-MM-YYYY.

import shutil, os, re

# Create a regex that matches files with the American date format.
datePattern = re.compile(r"""^(.*?) # all text before the date
    ((0|1)?\d)- # one or two digits for the month
    ((0|1|2|3)?\d)- # one or two digits for the day
    ((19|20)\d\d) # four digits for the year (must start with 19 or 20)
    (.*?)$ # all text after the date
    """, re.VERBOSE)

# Loop over the files in the working directory.
for amerFilename in os.listdir('./dates-files/'):
    mo = datePattern.search(amerFilename)

    # Skip files without a date.
    if mo == None:
        continue

    # Get the different parts of the filename.
    beforePart = mo.group(1)
    monthPart  = mo.group(2)
    dayPart    = mo.group(4)
    yearPart   = mo.group(6)
    afterPart  = mo.group(8)

    print("using re.search...")
    #print(mo)
    print("0: " + mo.group(0)) # search的0默认是整体匹配的结果
    print("1: " + mo.group(1)) # 从1开始是左括号
    print("2: " + mo.group(2))
    print("3: " + mo.group(3))
    print("4: " + mo.group(4))
    print("5: " + mo.group(5))
    print("6: " + mo.group(6))
    print("7: " + mo.group(7))
    print("8: " + mo.group(8))
    
    print("using re.findall...")
    # 如果你不给整体加小括号，那么findall的0是第1个分组！
    print(datePattern.findall(amerFilename))
    
    break # 这是个验证程序，所以在找到第一个可以验证正则的文件名后，随即退出


