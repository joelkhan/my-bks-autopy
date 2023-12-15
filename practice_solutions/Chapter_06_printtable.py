'''
Chapter 6 Manipulating Strings

Write a function named printTable() that takes a list of lists of strings
and displays it in a well-organized table with each column right-justified.
Assume that all the inner lists will contain the same number of strings.

'''

tableData = [
    ['apples', 'oranges', 'cherries', 'banana'],
    ['Alice', 'Bob', 'Carol', '#David'],
    ['dogs', 'cats', 'moose', 'goose']]
#
# 本程序作者的行、列的概念和我正好相反
# 他的行在我看来是列，他的列在我看来是行
# 运行程序，结合输出的结果看代码，还是可以看明白的
# 否则，只看代码，容易晕
# 
def printTable(tData):
    colWidth = [0] * len(tData)
    print(colWidth)
    for col in range(len(tData)):
        for row in range(len(tData[0])):
            entryLength = len(tData[col][row])
            if(entryLength > colWidth[col]):
                colWidth[col] = entryLength
    print(colWidth)
    for row in range(len(tData[0])):
        for col in range(len(tData)):
            print(tData[col][row].rjust(colWidth[col]) + ' ', end='')
        print()

printTable(tableData)


