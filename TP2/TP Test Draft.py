from cmu_112_graphics import *
import random, math

def appStarted(app):
    # Character Sprite Sheet Generation
    tempCharacterScaling = 1/10
    app.tempCharacter = app.loadImage("SpriteSheetTempRight.png") # original work
    app.tempCharacterScaled = app.scaleImage(app.tempCharacter, tempCharacterScaling)
    spriteMargin = 0
    sheetWidth = 480
    sheetHeight = 120
    app.spriteWidth = sheetWidth*tempCharacterScaling
    app.spriteHeight = sheetHeight*tempCharacterScaling
    app.tempCharCropRight = app.tempCharacterScaled.crop((spriteMargin,spriteMargin,\
            (app.spriteWidth)-spriteMargin,\
            (app.spriteHeight)-spriteMargin))
    app.tempCharacterFlipped = app.loadImage("SpriteSheetTempLeft.png") # original work (editied)
    app.tempCharacterFlippedScaled = app.scaleImage(app.tempCharacterFlipped, tempCharacterScaling)
    app.tempCharCropLeft = app.tempCharacterFlippedScaled.crop((spriteMargin,spriteMargin,\
            (app.spriteWidth)-spriteMargin,\
            (app.spriteHeight)-spriteMargin))
    app.sprites = []

    # Map generation:
    app.terrainWidth = app.width
    app.terrainHeight = app.height
    app.squareDim = 12
    app.cols = app.terrainWidth//app.squareDim
    app.rows = app.terrainHeight//app.squareDim
    app.randomBoard = [ [0] *app.cols for i in range(app.rows)]
    app.board = [ [0] *app.cols for i in range(app.rows)]
    app.neighbors = [ (0,1), (0,-1), (1,0), (1,1), (1,-1), (-1,0), (-1,1), (-1,-1)]

    # Character Sprite List
    for i in range(4):
        image = app.tempCharCropRight.crop(((app.spriteWidth/4)*i-1, 0, \
            (app.spriteWidth/4)*(i+1), app.spriteHeight))
        app.sprites.append(image)
        app.spritesFlipped = []
    for i in range(4):
        image = app.tempCharCropLeft.crop(((app.spriteWidth/4)*i-1, 0, \
            (app.spriteWidth/4)*(i+1), app.spriteHeight))
        app.spritesFlipped.append(image)
    app.spriteIndex = 0  

    #Player Generation:
    app.playerSpeed = 12
    app.playerPosX = 10*app.squareDim
    app.playerPosY = 10*app.squareDim

    #Projectile Generation:
    app.projPosX = app.playerPosX
    app.projPosY = app.playerPosY
    app.projChangeX = 0 
    app.projChangeY = 0
    app.projR = 5
    app.projSpeed = 12
    app.projAngle = 0  
    app.projCount = 0
    app.mouseX = 0
    app.mouseY = 0
    app.targetX = 0
    app.targetY = 0
    
    #Enemy Generation
    app.numEnemies = 10
    app.enemyX = 0
    app.enemyY = 0
    app.enemyR = app.squareDim/2
    app.enemyPosX = []
    app.enemyPosY = []

    randomDungeonFloor(app)
    generateEnemy(app)

def keyPressed(app,event):
    if (event.key == "Left"):
        movePlayer(app, -app.playerSpeed, 0)
    if (event.key == "Right"):
        movePlayer(app, app.playerSpeed, 0)
    if (event.key == "Up"):
        movePlayer(app, 0, -app.playerSpeed)
    if (event.key == "Down"):
        movePlayer(app, 0, app.playerSpeed)
    if (event.key == "a"):
        moveEnemy(app)
    else:
        pass

def randomDungeonFloor(app):
    for row in range(app.rows):
        for col in range(app.cols): 
            app.randomBoard[row][col] = random.randint(0,1)
    generateDungeonFloor(app,5)

def generateDungeonFloor(app,runs): 
    # I get inspiration from the "Cellular Automata" slides in the terrain generation additional TA lecture
    numRuns = 0
    while numRuns <= runs:
        for row in range(app.rows):
            for col in range(app.cols):
                spaceCount = 0
                wallCount = 0
                for move in app.neighbors:
                    dx,dy = move
                    newRow, newCol = row+dx,col+dy
                    if newRow < 0 or newRow >= app.rows or newCol < 0 or newCol >= app.cols:
                        continue
                    else:
                        if app.randomBoard[row][col] == 1 and app.randomBoard[newRow][newCol] == 1:
                            spaceCount += 1
                            if spaceCount >=4:
                                app.board[row][col] = 1
                        elif app.randomBoard[row][col] == 0 and app.randomBoard[newRow][newCol] == 1:
                            spaceCount +=1 
                            if spaceCount >=5:
                                app.board[row][col] = 1

        app.randomBoard = app.board
        # Border
        for col in range(app.cols):
            app.board[1][col] = 0
            app.board[app.rows-1][col] = 0
        for row in range(app.rows):
            app.board[row][1] = 0
            app.board[row][app.cols-1] = 0
        numRuns += 1 

        #Player Spawn Point
        spawnCenterX = app.playerPosX//app.squareDim
        spawnCenterY = app.playerPosY//app.squareDim
        for col in range(spawnCenterX-5,spawnCenterX+5):
            for row in range(spawnCenterY-5,spawnCenterY+5):
                app.board[row][col] = 1
        

def drawDungeonFloor(app,canvas):
    for col in range(1,app.cols):
        for row in range(1,app.rows):
            if app.board[row][col] == 0:
                canvas.create_rectangle(col*app.squareDim+(app.squareDim/2),\
                    row*app.squareDim+(app.squareDim/2),\
                    col*app.squareDim-(app.squareDim/2),\
                    row*app.squareDim-(app.squareDim/2), fill="black", width = 1)
            elif app.board[row][col] == 1:
                canvas.create_rectangle(col*app.squareDim+(app.squareDim/2),\
                    row*app.squareDim+(app.squareDim/2),\
                    col*app.squareDim-(app.squareDim/2),\
                    row*app.squareDim-(app.squareDim/2), fill="white", width = 1)

def drawCharacter(app,canvas):
    if app.mouseX > app.playerPosX:
        canvas.create_image(app.playerPosX,app.playerPosY,\
                        image=ImageTk.PhotoImage(app.sprites[app.spriteIndex]))
    else:
        canvas.create_image(app.playerPosX,app.playerPosY,\
                        image=ImageTk.PhotoImage(app.spritesFlipped[app.spriteIndex]))

def movePlayer(app,dx,dy):
    app.playerPosX += dx
    app.playerPosY += dy
    if app.playerPosX < 2*app.squareDim or app.playerPosX > app.terrainWidth-2*app.squareDim:
        app.playerPosX -= dx
    elif app.playerPosY < 2*app.squareDim or app.playerPosY > app.terrainHeight-2*app.squareDim:
        app.playerPosY -= dy
    currRow = app.playerPosX//app.squareDim
    currCol = app.playerPosY//app.squareDim
    if app.board[currCol][currRow] == 0:
        app.playerPosX -= dx
        app.playerPosY -= dy

def mouseMoved(app,event):
    app.mouseX = event.x
    app.mouseY = event.y
    
def mousePressed(app,event):
    app.projPosX = app.playerPosX
    app.projPosY = app.playerPosY
    app.projCount += 1
    app.targetX = event.x
    app.targetY = event.y
    totalX = app.targetX - app.projPosX
    totalY = app.targetY - app.projPosY
    app.projAngle = math.atan(totalY/totalX)
    app.projChangeX = app.projSpeed * math.cos(app.projAngle)
    app.projChangeY = app.projSpeed * math.sin(app.projAngle)

def timerFired(app):
    if app.projPosX <= app.terrainWidth and app.projPosX > 0 and \
        app.projPosY < app.terrainHeight and app.projPosY > 0 and \
            app.board[int(app.projPosX)//app.squareDim][int(app.projPosY)//app.squareDim]:
        if app.targetX > app.playerPosX:
            app.projPosX += app.projChangeX
            app.projPosY += app.projChangeY
        else:
            app.projPosX -= app.projChangeX
            app.projPosY -= app.projChangeY
    else:
        app.projPosX = app.playerPosX
        app.projPosY = app.playerPosY
        app.projChangeX
        app.projChangeY

def generateEnemy(app):
    while app.numEnemies > 0:
        enemyCol = random.randint(2, app.cols-2)
        enemyRow = random.randint(2, app.rows-2)
        if app.board[enemyRow][enemyCol] == 1 and \
            (enemyCol not in app.enemyPosX or enemyRow not in app.enemyPosY):
            app.enemyPosX.append(enemyCol)
            app.enemyPosY.append(enemyRow)
            app.numEnemies -= 1 
        else:
            continue
        
def moveEnemy(app):
    for i in range(len(app.enemyPosX)):
        if app.playerPosX - app.enemyPosX[i] > app.playerPosY - app.enemyPosY[i]:
            if app.playerPosX > app.enemyPosX[i]:
                app.enemyPosX[i] += 1
            else:
                app.enemyPosX[i] -= 1
        else:
            if app.playerPosY > app.enemyPosY[i]:
                app.enemyPosY[i] += 1
            else:
                app.enemyPosY[i] -= 1
    
def drawEnemy(app,canvas):
    for i in range(len(app.enemyPosX)):
        enemyY = app.enemyPosX[i] * app.squareDim
        enemyX = app.enemyPosY[i] * app.squareDim
        canvas.create_rectangle(enemyX+app.enemyR,enemyY+app.enemyR,\
                enemyX-app.enemyR,enemyY-app.enemyR,fill = "green")

def drawProjectile(app,canvas):
    canvas.create_oval(app.projPosX+app.projR,app.projPosY+app.projR,\
                app.projPosX-app.projR,app.projPosY-app.projR, fill="white")

def redrawAll(app, canvas):
    drawDungeonFloor(app,canvas)
    drawCharacter(app,canvas)
    if app.projCount == 0:
        pass
    else:
        drawProjectile(app,canvas)
    drawEnemy(app,canvas)

runApp(width = 1000, height = 800)


