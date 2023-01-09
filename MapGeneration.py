from cmu_112_graphics import *
import random, math

def appStarted(app):
    app.squareDim = 13
    app.rows = app.height//app.squareDim
    app.cols = app.width//app.squareDim
    app.randomBoard = [ [0] *app.cols for i in range(app.rows)]
    app.board = [ [0] *app.cols for i in range(app.rows)]
    app.neighbors = [ (0,1), (0,-1), (1,0), (1,1), (1,-1), (-1,0), (-1,1), (-1,-1)]
    randomDungeonFloor(app)

def drawDungeonFloor(app,canvas):
    for col in range(1,app.cols):
        for row in range(1,app.rows):
            if app.board[row][col] == 0:
                canvas.create_rectangle(col*app.squareDim+(app.squareDim/2),\
                    row*app.squareDim+(app.squareDim/2),\
                    col*app.squareDim-(app.squareDim/2),\
                    row*app.squareDim-(app.squareDim/2), fill="black", width = 0)
            elif app.board[row][col] == 1:
                canvas.create_rectangle(col*app.squareDim+(app.squareDim/2),\
                    row*app.squareDim+(app.squareDim/2),\
                    col*app.squareDim-(app.squareDim/2),\
                    row*app.squareDim-(app.squareDim/2), fill="white",  width = 0)

def randomDungeonFloor(app):
    for col in range(app.cols):
        for row in range(app.rows): 
            app.randomBoard[row][col] = random.randint(0,1)
    generateDungeonFloor(app,3)

def generateDungeonFloor(app,runs):
    numRuns = 0
    while numRuns <= runs:
        for col in range(app.cols):
            for row in range(app.rows):
                spaceCount = 0
                wallCount = 0
                for move in app.neighbors:
                    dx,dy = move
                    newRow, newCol = col+dx,row+dy
                    if newRow < 0 or newRow >= app.rows or newCol < 0 or newCol >= app.cols:
                        continue
                    else:
                        if app.randomBoard[row][col] == 1 and app.randomBoard[newRow][newCol] == 1:
                            spaceCount += 1
                            if spaceCount >=4:
                                app.board[row][col] = 1
                        elif app.randomBoard[row][col] == 0 and app.randomBoard[newRow][newCol] == 1:
                            spaceCount +=1 
                            if spaceCount >= 5:
                                app.board[row][col] = 1
        app.randomBoard = app.board
        for col in range(app.cols):
            app.board[1][col] = 0
            app.board[app.rows-1][col] = 0
        for row in range(app.rows):
            app.board[row][1] = 0
            app.board[row][app.cols-1] = 0
        numRuns += 1 

def redrawAll(app, canvas):
    drawDungeonFloor(app,canvas)

runApp(width = 800, height = 800)

