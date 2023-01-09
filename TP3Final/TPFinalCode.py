from cmu_112_graphics import *
import random, math

def appStarted(app):
    # Character Sprite Sheet Generation
    # Sprite Animation inspired by TA optional Lecture on Images
    app.gameStarted = False
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
    app.squareDim = 12
    app.scoreboardMargin = app.squareDim * 3
    app.terrainWidth = app.width
    app.terrainHeight = app.height - app.scoreboardMargin
    app.cols = app.terrainWidth//app.squareDim
    app.rows = app.terrainHeight//app.squareDim
    app.randomBoard = [ [0] *app.cols for i in range(app.rows)]
    app.tempBoard = [ [0] *app.cols for i in range(app.rows)]
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
    app.projListX = []
    app.projListY = []
    app.targetListX = []
    app.targetListY = []
    app.projAngleList = []
    app.projChangeListX = []
    app.projChangeListY = []
    app.projR = 5
    app.projSpeed = 12
    app.projCount = 0
    app.projDistance = 0
    app.maxProjDist = 10
    
    #Enemy Generation
    app.mouseX = 0
    app.mouseY = 0
    app.numEnemies = 2
    app.enemyX = 0
    app.enemyY = 0
    app.enemyR = app.squareDim/2
    app.enemyCol = []
    app.enemyRow = []
    app.enemySpeed = 1
    app.enemyMovementTrigger = 0

    # Scoreboard
    app.roundNumber = 1
    app.lives = 3

    app.gameOver = False
    randomDungeonFloor(app)
    generateEnemy(app)

def drawStartScreen(app,canvas):
    canvas.create_rectangle(app.squareDim/2, app.squareDim/2, app.width-(app.squareDim/2), app.height-(app.squareDim/2), fill = "dark grey", width = 5)
    Margin1 = 50
    enemyR = 10
    projR = enemyR/2
    outerEnemyBox = enemyR * 5
    canvas.create_rectangle((app.squareDim/2)+Margin1, (app.squareDim/2)+Margin1, (app.width-(app.squareDim/2))-Margin1, ((2*app.height/3)-(app.squareDim/2))-Margin1, fill = "grey", width = 5)
    canvas.create_text(app.width/2, (app.height/3), text = "Enter the 112Dungeon", font = f'Arial {int(app.width/20)} bold')
    canvas.create_text(app.width/2, (app.height/3)+50, text = "A 112 rendition of -- Enter the Gungeon", font = f'Arial {int(app.width/100)} bold')

    canvas.create_rectangle(app.width/5+outerEnemyBox,3*app.height/4+outerEnemyBox,app.width/5-outerEnemyBox,3*app.height/4-outerEnemyBox, fill = "white", width = 3)
    canvas.create_rectangle(app.width/5+enemyR,3*app.height/4+enemyR,app.width/5-enemyR,3*app.height/4-enemyR, fill = "green")
    canvas.create_text(app.width/5,2*app.height/3-25, text = "Avoid These Dungeon Crawlers")

    canvas.create_rectangle(app.width/2+outerEnemyBox,3*app.height/4+outerEnemyBox,app.width/2-outerEnemyBox,3*app.height/4-outerEnemyBox, fill = "white", width = 3)
    canvas.create_image(app.width/2,3*app.height/4,image=ImageTk.PhotoImage(app.sprites[0]))
    canvas.create_text(app.width/2,2*app.height/3-25, text = "Move around using WASD or Arrow Keys")

    canvas.create_rectangle(4*app.width/5+outerEnemyBox,3*app.height/4+outerEnemyBox,4*app.width/5-outerEnemyBox,3*app.height/4-outerEnemyBox, fill = "white", width = 3)
    canvas.create_oval(4*app.width/5+projR,3*app.height/4+projR,4*app.width/5-projR,3*app.height/4-projR, fill = "white")
    canvas.create_text(4*app.width/5,2*app.height/3-25, text = "Click Mouse Button To Shoot Dungeon Crawlers")

    canvas.create_rectangle(app.width/2-100,app.height-20,app.width/2+100,app.height-60, fill = "dark green", width = 2)
    canvas.create_text(app.width/2,app.height-40, text = "Hit G to Start Game!!!", font = f'Arial {int(app.width/75)} bold')



def drawGameOver(app,canvas):
    #canvas.create_rectangle(app.squareDim/2, app.squareDim/2, app.width-(app.squareDim/2), app.height-(app.squareDim/2), fill = "grey", width = 5)
    canvas.create_text(app.width/2,app.height/2,text = "GAME OVER", fill = "red", font = f'Arial {int(app.width/10)} bold')
    canvas.create_text(app.width/2,2*app.height/3,text = "Press R to Restart", fill = "red", font = f'Arial {int(app.width/20)} bold')

def mouseMoved(app,event):
    app.mouseX = event.x
    app.mouseY = event.y

def keyPressed(app,event):
    if (event.key == "Left") or (event.key == "a"):
        movePlayer(app, -app.playerSpeed, 0)
    if (event.key == "Right") or (event.key == "d"):
        movePlayer(app, app.playerSpeed, 0)
    if (event.key == "Up") or (event.key == "w"):
        movePlayer(app, 0, -app.playerSpeed)
    if (event.key == "Down") or (event.key == "s"):
        movePlayer(app, 0, app.playerSpeed)
    if (event.key == "r"):
        if app.gameOver == True:
            app.gameStarted = False
        else:
            resetGame(app)
    if (event.key == "g"):
        app.gameStarted = True
        app.gameOver == False
        resetGame(app)
    else:
        pass

def resetGame(app):
    app.enemyRow = []
    app.enemyCol = []
    app.lives = 3
    app.roundNumber = 1
    app.numEnemies = 2
    app.gameOver = False
    newLevel(app)

def newLevel(app):
    if app.gameOver == False:
        randomDungeonFloor(app)
        generateEnemy(app)
    else: pass

def newRound(app):
    startingEnemyCount = 2
    app.numEnemies += (startingEnemyCount + (app.roundNumber*2))
    app.roundNumber += 1        
    newLevel(app)
    
def randomDungeonFloor(app):
    for row in range(app.rows):
        for col in range(app.cols): 
            app.randomBoard[row][col] = random.randint(0,1)
    generateDungeonFloor(app,5)

def generateDungeonFloor(app,runs): 
    # I got inspiration from the "Cellular Automata" slides in the terrain generation additional TA lecture
    numRuns = 0
    app.tempBoard = [ [0] *app.cols for i in range(app.rows)]
    while numRuns <= runs:
        for row in range(app.rows):
            for col in range(app.cols):
                spaceCount = 0
                wallCount = 0
                for move in app.neighbors:
                    dx,dy = move
                    newRow, newCol = row+dy,col+dx
                    if newRow < 0 or newRow >= app.rows or newCol < 0 or newCol >= app.cols:
                        continue
                    else:
                        if app.randomBoard[row][col] == 1 and app.randomBoard[newRow][newCol] == 1:
                            spaceCount += 1
                            if spaceCount >=4:
                                app.tempBoard[row][col] = 1
                        elif app.randomBoard[row][col] == 0 and app.randomBoard[newRow][newCol] == 1:
                            spaceCount +=1 
                            if spaceCount >=5:
                                app.tempBoard[row][col] = 1
        app.randomBoard = app.tempBoard
        # Player Spawn Point
        spawnCenterX = app.playerPosX//app.squareDim
        spawnCenterY = app.playerPosY//app.squareDim
        for col in range(spawnCenterX-5,spawnCenterX+5):
            for row in range(spawnCenterY-5,spawnCenterY+5):
                app.tempBoard[row][col] = 1
        # Border
        for col in range(app.cols):
            app.tempBoard[1][col] = 2
            app.tempBoard[app.rows-1][col] = 2
        for row in range(app.rows):
            app.tempBoard[row][1] = 2
            app.tempBoard[row][app.cols-1] = 2
        numRuns += 1 
    app.board = app.tempBoard

def drawDungeonFloor(app,canvas):
    for col in range(1,app.cols):
        for row in range(1,app.rows):
            if app.board[row][col] == 0:
                canvas.create_rectangle(col*app.squareDim+(app.squareDim/2),\
                    row*app.squareDim+(app.squareDim/2) + app.scoreboardMargin,\
                    col*app.squareDim-(app.squareDim/2),\
                    row*app.squareDim-(app.squareDim/2) + app.scoreboardMargin, fill="grey", width = 0)
            elif app.board[row][col] == 1:
                canvas.create_rectangle(col*app.squareDim+(app.squareDim/2),\
                    row*app.squareDim+(app.squareDim/2) + app.scoreboardMargin,\
                    col*app.squareDim-(app.squareDim/2),\
                    row*app.squareDim-(app.squareDim/2) + app.scoreboardMargin, fill="white", width = 0)
            elif app.board[row][col] == 2:
                canvas.create_rectangle(col*app.squareDim+(app.squareDim/2),\
                    row*app.squareDim+(app.squareDim/2) + app.scoreboardMargin,\
                    col*app.squareDim-(app.squareDim/2),\
                    row*app.squareDim-(app.squareDim/2) + app.scoreboardMargin, fill="black", width = 0)

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
    elif app.playerPosY < 2*app.squareDim or app.playerPosY > app.terrainHeight+app.squareDim:
        app.playerPosY -= dy
    currRow = (app.playerPosY//app.squareDim) - (app.scoreboardMargin//app.squareDim)
    currCol = (app.playerPosX//app.squareDim)
    if app.board[currRow][currCol] == 0:
        app.playerPosX -= dx
        app.playerPosY -= dy
    
def mousePressed(app,event):
    app.targetListX.append(event.x)
    app.targetListY.append(event.y)
    generateProj(app)

def timerFired(app):
    if app.gameStarted == True:
        if app.gameOver == False:
            if app.projCount > 0:
                shootProjectile(app)
            else:
                pass
            app.enemyMovementTrigger += 1
            collideWithPlayer(app)
            if app.enemyMovementTrigger % 5 == 0:
                moveEnemy(app)
                pass 
            else: pass
        else: pass
    else:pass

def collideWithPlayer(app):
    for i in range(app.numEnemies):
        if app.enemyCol[i] == app.playerPosX//app.squareDim and\
             app.enemyRow[i]+(app.scoreboardMargin//app.squareDim) == app.playerPosY//app.squareDim:
            if app.lives > 0:
                app.lives -= 1
            elif app.lives == 0:
                print("dead")
                app.gameOver = True                

def generateProj(app):
    app.projListX.append(app.playerPosX)
    app.projListY.append(app.playerPosY)
    totalX = app.targetListX[app.projCount] - app.projListX[app.projCount]
    totalY = app.targetListY[app.projCount] - app.projListY[app.projCount]
    if totalX == 0:
        app.projAngleList.append(math.radians(90))
    else:
        app.projAngleList.append(math.atan(totalY/totalX))
    app.projChangeListX.append(app.projSpeed * math.cos(app.projAngleList[app.projCount]))
    app.projChangeListY.append(app.projSpeed * math.sin(app.projAngleList[app.projCount]))
    shootProjectile(app)
    app.projCount += 1

def shootProjectile(app):
    count = 0
    while count != app.projCount:
        projRow = app.projListY[count]//app.squareDim
        projCol = app.projListX[count]//app.squareDim
        if projRow < 5 or \
            app.projListY[count] > app.terrainHeight or \
            projCol < 2 or\
            app.projListX[count] > app.terrainWidth-(2*app.squareDim):
            removeProj(app,count)
            count-=1
        elif app.board[int(projRow)-2][int(projCol)] == 0:
            removeProj(app,count)
            app.board[int(projRow)-2][int(projCol)] = 1
            count-=1
        if (int(projRow-2)) in app.enemyRow and int(projCol) in app.enemyCol:
                removeProj(app,count)
                app.enemyRow.pop(app.enemyRow.index(int(projRow-2)))
                app.enemyCol.pop(app.enemyCol.index(int(projCol)))
                app.numEnemies -= 1
                if app.numEnemies == 0: 
                    newRound(app)
                count-=1
        count+=1
    for i in range(app.projCount):
        if app.targetListX[i] > app.playerPosX:
            app.projListX[i] += app.projChangeListX[i]
            app.projListY[i] += app.projChangeListY[i]
        else:
            app.projListX[i] -= app.projChangeListX[i]
            app.projListY[i] -= app.projChangeListY[i]

def removeProj(app,i):
    app.projListX.pop(i)
    app.projListY.pop(i)
    app.targetListX.pop(i)
    app.targetListY.pop(i)
    app.projAngleList.pop(i)
    app.projChangeListX.pop(i)
    app.projChangeListY.pop(i)
    app.projCount -= 1

def drawProjectile(app,canvas,i):
    canvas.create_oval(app.projListX[i]+app.projR,app.projListY[i]+app.projR,\
                    app.projListX[i]-app.projR,app.projListY[i]-app.projR, fill="white")

def drawScoreboard(app,canvas):
    canvas.create_text(app.width/2,app.scoreboardMargin/2, text=f"Crawlers Remaining: {str(app.numEnemies)}", \
                        font = 'Arial 16 bold', fill='Black')
    canvas.create_text(app.scoreboardMargin * 3,app.scoreboardMargin/2, text=f"DungeonLevel: {app.roundNumber}", \
                        font = 'Arial 16 bold', fill='Black')
    canvas.create_text(app.width-app.scoreboardMargin*3,app.scoreboardMargin/2, text=f"Lives: {app.lives}", \
                        font = 'Arial 16 bold', fill='Black')

def generateEnemy(app):
    enemyCount = app.numEnemies
    while enemyCount > 0:
        enemyCol = random.randint(3, app.cols-2)
        enemyRow = random.randint(5, app.rows-4)
        if app.board[enemyRow][enemyCol] == 1 and \
            (enemyCol not in app.enemyCol or enemyRow not in app.enemyRow) or\
                (enemyCol == app.playerPosX and enemyRow == app.playerPosY):
            app.enemyCol.append(enemyCol)
            app.enemyRow.append(enemyRow)
            enemyCount -= 1 
        else:
            continue

def drawEnemy(app,canvas):
    for i in range(len(app.enemyCol)):
        enemyX = app.enemyCol[i] * app.squareDim
        enemyY = app.enemyRow[i] * app.squareDim + app.scoreboardMargin
        canvas.create_rectangle(enemyX+app.enemyR,enemyY+app.enemyR,\
                enemyX-app.enemyR,enemyY-app.enemyR,fill = "green")

def moveEnemy(app):
    for i in range(len(app.enemyRow)):
        if app.playerPosX > app.enemyCol[i]*app.squareDim:
            app.enemyCol[i] += 1
            if isLegal(app, i) == False:
                app.enemyCol[i] -= 1
        elif app.playerPosX < app.enemyCol[i]*app.squareDim:
            app.enemyCol[i] -= 1
            if isLegal(app, i) == False:
                app.enemyCol[i] += 1

        if app.playerPosY > (app.enemyRow[i]+3)*app.squareDim:
            app.enemyRow[i] += 1
            if isLegal(app, i) == False:
                app.enemyRow[i] -= 1
        elif app.playerPosY < (app.enemyRow[i]+3)*app.squareDim:
            app.enemyRow[i] -= 1
            if isLegal(app, i) == False:
                app.enemyRow[i] += 1
            
def isLegal(app, i):
    if app.board[app.enemyRow[i]][app.enemyCol[i]] == 0:
        return False 
    return True

def redrawAll(app, canvas):
    if app.gameStarted == True:
        drawDungeonFloor(app,canvas)
        drawCharacter(app,canvas)
        for i in range(len(app.projListX)):
            drawProjectile(app,canvas,i)
        drawEnemy(app,canvas)
        drawScoreboard(app,canvas) 
        if app.gameOver == True:
            drawGameOver(app,canvas)
    elif app.gameStarted == False:
        drawStartScreen(app,canvas)

runApp(width = 1000, height = 600)