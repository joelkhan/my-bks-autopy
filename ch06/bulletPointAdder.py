#! python3
# Adds Wikipedia bullet points to the start
# of each line of text on the clipboard.
# 说明：
# pyperclip 正确安装并使用这个包需要一些系统依赖，暂时不关注了
# 
import pyperclip
text = pyperclip.paste()

#Separate lines and add stars.
lines = text.split('\n')
for i in range(len(lines)): # loop through all indexes for "lines" list
    lines[i] = '* ' + lines[i] # add star to each string in "lines" list
text = '\n'.join(lines)
pyperclip.copy(text)
