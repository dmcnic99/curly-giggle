import turtle
import pandas as pd
from collections import Counter


def drawGrid(grid):
    for row in range(0, 10):
        if (row % 3) == 0:
            myPen.pensize(3)
        else:
            myPen.pensize(1)
        myPen.penup()
        myPen.goto(topLeft_x, topLeft_y - row * intDim)
        myPen.pendown()
        myPen.goto(topLeft_x + 9 * intDim, topLeft_y - row * intDim)
    for col in range(0, 10):
        if (col % 3) == 0:
            myPen.pensize(3)
        else:
            myPen.pensize(1)
        myPen.penup()
        myPen.goto(topLeft_x + col *intDim, topLeft_y)
        myPen.pendown()
        myPen.goto(topLeft_x + col * intDim, topLeft_y - 9 * intDim)
    return


def text(number, x, y, size, color = 'black'):
    FONT = ['Calibri', size, 'normal']
    myPen.penup()
    myPen.goto(x, y)
    myPen.pencolor(color)
    myPen.write(number, align = 'left', font = FONT)
    return


def printValue(color, value, x, y):
    # This is used when numbers are found and added to the grid
    # Highlight the cell
    # pencolor is black and fill color is yellow
    # Place the number
    text(x = topLeft_x + x * intDim + 9,
         y = topLeft_y - y * intDim - intDim + 8,
         number = value, size = 18, color = color)
    # Create a normal background
    # pencolor is black and fill color is white
    # Place the number
    text(x = topLeft_x + x * intDim + 9,
         y = topLeft_y - y * intDim - intDim + 8,
         number = value, size = 18, color = color)
    return


def updateText(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] != '0':
                # printValue(grid[row][col], topLeft_x + col * intDim + 9,
                #            topLeft_y - y * intDim - intDim * 8, 18)
                text(grid[row][col], topLeft_x + col * intDim + 9, 
                     topLeft_y - row * intDim - intDim + 8, 18)
    return


def initializeGrid():
    turtle.title('Python Sudoku Solver')
    # get puzzle
    try:
        # Ubuntu
        df = pd.read_excel('/home/dmcnic/Dropbox/Puzzles/Dell2021-01.xlsx')
    except:
        # MacBook
        df = pd.read_excel('/Users/david/Dropbox/Puzzles/Dell2021-01.xlsx')
    # print(df['Puzzle'][0])
    grid = []
    for startPos in range(0, 81, 9):
        grid.append([char for char in df['Puzzle'][0][startPos:startPos + 9]])
    text('Dell Magazine 01/2021 # 001', -150, 175, 18)
    # grid = [char for char in df['Puzzle'][0]]
    # print(grid)
    return grid


def clearText():
    turtle.penup()
    turtle.goto(-150, -200)
    turtle.pencolor('white')
    turtle.pendown()
    turtle.fillcolor('white')
    turtle.begin_fill()
    turtle.goto(150, -200)
    turtle.goto(150, -250)
    turtle.goto(-150, -250)
    turtle.goto(-150, -200)
    turtle.end_fill()
    return


def phaseZero(grid, showStatus = False):
    zeroCount = len([ele for eachRow in grid for ele in eachRow if ele == '0'])
    clearText()
    if showStatus:
        text('There are ' + str(zeroCount) + ' empty cells', -150, -250, 18)
    return zeroCount


def squares(grid):
    # This converts the grid by rows to a grid by squares
    newGrid = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            newGrid.append([grid[i + 0][j + 0], grid[i + 0][j + 1], grid[i + 0][j + 2],
                           grid[i + 1][j + 0], grid[i + 1][j + 1], grid[i + 1][j + 2],
                           grid[i + 2][j + 0], grid[i + 2][j + 1], grid[i + 2][j + 2]])
    return newGrid


def checkGrid(grid, iterType):
    for ndx, eachIter in enumerate(grid):
        iterCount = Counter(eachIter)
        del iterCount['0']
        if iterCount.most_common(1)[0][1] > 1:
            return 'Fault in ' + iterType + ' ' + (ndx + 1)
    return


def checkZero(grid):
    # This function checks to see if '0' has a value of one
    for ndx, eachIter in enumerate(grid):
        iterCount = Counter(eachIter)
        if iterCount['0'] == 1:
            return ndx
    return


def checkForFault(grid):
    # Check for fault looks for duplicated numbers
    # Start with rows
    checkResult = checkGrid(grid, 'row')
    if checkResult is not None:
        return checkResult
    # Next is columns
    # https://stackoverflow.com/questions/6473679/transpose-list-of-lists
    checkResult = checkGrid(list(map(list, zip(*grid))), 'column')
    if checkResult is not None:
        return checkResult
    # Finally, squares
    checkResult = checkGrid(squares(grid), 'square')
    if checkResult is not None:
        return checkResult
    return


def phaseOne(grid):
    # check for iters of length eight
    # This can be accomplished by using Counter and seeing if '0' has a value of 1 (one)
    # Start with rows
    countZero = checkZero(grid)
    if countZero is not None:
        # countZero contains the row number with one blank
        testList = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for eachItem in grid[countZero]:
            del testList[eachItem]
        # The remaining value in testList is the missing value
        # Find the location of the missing value
        missingColumn = grid[countZero].index(testList[0])
        # Print the missing value
        printValue(x = missingColumn, y = countZero,
                   value = testList[0], penColor = 'blue')
        # Use a list comprehension to modify the targeted row
        newList = [testList[0] if x == '0' else x for x in grid[countZero]]
        # Create a new grid with the new row
        newGrid = []
        for ndx, eachRow in grid:
            if ndx == countZero:
                newGrid.append(newList)
            else:
                newGrid.append(grid[ndx])
        return newGrid


def phaseTwo(grid):
    # Check for a value in two of three triplets
    # then look for that value to fill one cell in the third triplet
    for i in range(0, 9, 3):   # identifier of the first triplet
        for testValue in range(1, 9):   # value to find 
            targetIter = 0
            if (testValue in grid[i]) and (testValue in grid[i + 1]) and (testValue not in grid[i + 2]):
                targetIter = 3
            if (testValue in grid[i]) and (testValue not in grid[i + 1]) and (testValue in grid[i + 2]):
                targetIter = 2
            if (testValue not in grid[i]) and (testValue in grid[i + 1]) and (testValue in grid[i + 2]):
                targetIter = 1
            # if targetIter != 0:   # We have a potential situation that fits the first criteria
                # Find the square that is missing targetValue
                # With the missing row and the missing square, see if two values are filled
                # If so, then the second criteria is met and we have found a location for the targetValue

    return


def sudokuSolver(grid):
    # This will be the main function that will continuously loop
    # We just finished writing the grid. Call phaseZero() and get the open cell count.
    zeroCount = phaseZero(grid, showStatus = True)
    beginningCount = zeroCount
    endingCount = 81
    while (zeroCount > 0) and (beginningCount != endingCount):
        checkResult = checkForFault(grid)
        if checkResult is not None:
            clearText()
            text(checkResult, -150, -250, 18)
            turtle.exitonclick()
        # Phase one -- check for iters of length eight
        phaseOne(grid)
        zeroCount = phaseZero(grid, showStatus = False)
        # if zeroCount != beginningCount:
            # Phase two -- look for a number twice in a triplet
            # phaseTwo(grid)
        # End of the while loop
        endingCount = phaseZero(grid, showStatus = False)
    return


myPen = turtle.Turtle()
# myPen.speed(0)
myPen.color('#000000')
# myPen.hideturtle()
topLeft_x = -150
topLeft_y = 150
intDim = 35

grid = initializeGrid()
drawGrid(grid)
updateText(grid)
text('Sudoku puzzle ready', -150, -250, 18)
sudokuSolver(grid)
myPen.hideturtle()
turtle.exitonclick()