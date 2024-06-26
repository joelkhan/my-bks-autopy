# conway.py
#
# print("this conway game")
# 
# Conway's Game of Life
#

import random, time, copy
import os

#
# 函数定义
#
def show_conway_chart(h, w, cells):
    os.system('clear')
    for y in range(h):
        for x in range(w):
            print(cells[x][y], end='') # Print the # or space.
        print() # Print a newline at the end of the row.

#
# conway的主程序
# 
# 调整了time.sleep(0.1)，加快程序运行，即模拟细胞快速更新
# 感觉conway游戏最终是趋向于一个稳定的状态？？
#
WIDTH = 60
HEIGHT = 20

# Create a list of list for the cells:
# 初始化nextCells
nextCells = []
for x in range(WIDTH):
    column = [] # Create a new column.
    for y in range(HEIGHT):
        if (x, y) in ((1, 0), (2, 1), (0, 2), (1, 2), (2, 2)):
            column.append('#') # Add a living cell.
        else:
            column.append(' ') # Add a dead cell.
    nextCells.append(column) # nextCells is a list of column lists.

# 主循环
#cntr = 0
while True: # Main program loop.
    print('\n\n\n\n\n') # Separate each step with newlines.
    # 复制nextCells为currentCells
    currentCells = copy.deepcopy(nextCells)
    
    # 输出currentCells
    # Print currentCells on the screen:
    #cntr += 1
    #print("tims: " + str(cntr))
    show_conway_chart(HEIGHT, WIDTH, currentCells)

    # Calculate the next step's cells based on current step's cells:
    # 根据currentCells计算nextCells
    for x in range(WIDTH):
        for y in range(HEIGHT):
            # Get neighboring coordinates:
            # '% WIDTH' ensures leftCoord is always between 0 and WIDTH - 1
            leftCoord = (x - 1) % WIDTH
            rightCoord = (x + 1) % WIDTH
            aboveCoord = (y - 1) % HEIGHT
            belowCoord = (y + 1) % HEIGHT
            # Count number of living neighbors:
            numNeighbors = 0
            if currentCells[leftCoord][aboveCoord] == '#':
                numNeighbors += 1 # Top-left neighbor is alive.
            if currentCells[x][aboveCoord] == '#':
                numNeighbors += 1 # Top neighbor is alive.
            if currentCells[rightCoord][aboveCoord] == '#':
                numNeighbors += 1 # Top-right neighbor is alive.
            if currentCells[leftCoord][y] == '#':
                numNeighbors += 1 # Left neighbor is alive.
            if currentCells[rightCoord][y] == '#':
                numNeighbors += 1 # Right neighbor is alive.
            if currentCells[leftCoord][belowCoord] == '#':
                numNeighbors += 1 # Bottom-left neighbor is alive.
            if currentCells[x][belowCoord] == '#':
                numNeighbors += 1 # Bottom neighbor is alive.
            if currentCells[rightCoord][belowCoord] == '#':
                numNeighbors += 1 # Bottom-right neighbor is alive.
            
            # Set cell based on Conway's Game of Life rules:
            if currentCells[x][y] == '#' and (numNeighbors == 2 or numNeighbors == 3):
                # Living cells with 2 or 3 neighbors stay alive:
                nextCells[x][y] = '#'
            elif currentCells[x][y] == ' ' and numNeighbors == 3:
                # Dead cells with 3 neighbors become alive:
                nextCells[x][y] = '#'
            else:
                # Everything else dies or stays dead:
                nextCells[x][y] = ' '
    # 暂停1秒
    time.sleep(0.1) # Add a 1-second pause to reduce flickering.

