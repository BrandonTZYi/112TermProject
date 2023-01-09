from cmu_112_graphics import *
import random, math

def appStarted(app):
    tempCharacterScaling = 1/15
    app.tempCharacter = app.loadImage("SpriteSheetTempRight.png") # original work
    app.tempCharacterScaled = app.scaleImage(app.tempCharacter, tempCharacterScaling)
    spriteMargin = 2
    sheetWidth = 2003
    sheetHeight = 801
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
    for i in range(4):
        image = app.tempCharCropRight.crop(((app.spriteWidth/4)*i-1, 0, (app.spriteWidth/4)*(i+1), app.spriteHeight))
        app.sprites.append(image)
    
    app.spritesFlipped = []
    for i in range(4):
        image = app.tempCharCropLeft.crop(((app.spriteWidth/4)*i-1, 0, (app.spriteWidth/4)*(i+1), app.spriteHeight))
        app.spritesFlipped.append(image)

    app.tileSet = app.loadImage("basicTileSet.jpg") # comes from https://www.youtube.com/watch?v=fCpalUPlhMs&ab_channel=HeartBeast
    app.tileSetScaled = app.scaleImage(app.tileSet, 1/5)
    # Cut up tiles from youtube video:
    app.tile1 = app.loadImage('FloorTiles\Tile1.jpg') 
    app.tile2 = app.loadImage('FloorTiles\Tile2.jpg')
    app.tile3 = app.loadImage('FloorTiles\Tile3.jpg')
    app.tile4 = app.loadImage('FloorTiles\Tile4.jpg')
    app.tile5 = app.loadImage('FloorTiles\Tile5.jpg')

    # After looping through and randomly assigning tiles into place (see commented code below)
    # I snipped a picture of one of the floors for simplicity
    app.floor = app.loadImage('FloorTiles\Basic Floor.png')
    app.floorScaled = app.scaleImage(app.floor, 1/3)
    app.terrainWidth = 1000
    app.terrainHeight = 800
    app.playerSpeed = 10
    app.OffSetX = 0
    app.OffSetY = 0
    tileIdealSize = 25
    tileSize = 120
    tileConversion = tileIdealSize/tileSize
    app.tileList = [app.scaleImage(app.tile1, tileConversion),\
                    app.scaleImage(app.tile2, tileConversion),\
                    app.scaleImage(app.tile3, tileConversion),
                    app.scaleImage(app.tile4, tileConversion),\
                    app.scaleImage(app.tile5, tileConversion)]
    app.rows = app.terrainHeight//25
    app.cols = app.terrainWidth//25
    app.board = [ [0] *app.cols for i in range(app.rows)]
    app.mouseX = 0
    app.mouseY = 0
    app.targetX = 0
    app.targetY = 0
    app.projCount = 0
    app.playerPosX = app.width/2
    app.playerPosY = app.height/2
    app.projPosX = app.playerPosX
    app.projPosY = app.playerPosY
    app.projChangeX = 0 
    app.projChangeY = 0
    app.projR = 5
    app.projSpeed = 20
    app.projAngle = 0
    #generateDungeonFloor(app)    

def keyPressed(app,event):
    if (event.key == "Left"):
        movePlayer(app, -app.playerSpeed, 0)
    if (event.key == "Right"):
        movePlayer(app, app.playerSpeed, 0)
    if (event.key == "Up"):
        movePlayer(app, 0, -app.playerSpeed)
    if (event.key == "Down"):
        movePlayer(app, 0, app.playerSpeed)
    else:
        pass

def movePlayer(app,dx,dy):
    app.playerPosX += dx
    app.playerPosY += dy
    app.projPosX, app.projPosY = app.playerPosX, app.playerPosY

def drawDungeonFloor(app,canvas):
    canvas.create_image((app.width/2),(app.height/2),\
                    image=ImageTk.PhotoImage(app.floorScaled))
    # for col in range(1,app.cols):
    #     for row in range(1,app.rows):
    #         canvas.create_image(col*25+offSetX,row*25+offSetY,\
    #                 image=ImageTk.PhotoImage(app.tileList[app.board[row][col]]))

# def generateDungeonFloor(app):
#     for col in range(app.cols):
#         for row in range(app.rows): 
#             tileIndex = random.randint(0,len(app.tileList)-1)
#             app.board[row][col] = tileIndex
#     return app.board

def drawCharacter(app,canvas):
    if app.mouseX > app.width/2:
        canvas.create_image(app.playerPosX,app.playerPosY,\
                        image=ImageTk.PhotoImage(app.sprites[0]))
    else:
        canvas.create_image(app.playerPosX,app.playerPosY,\
                        image=ImageTk.PhotoImage(app.spritesFlipped[0]))

def mouseMoved(app,event):
    app.mouseX = event.x
    app.mouseY = event.y
    
def mousePressed(app,event):
    app.projPosX = app.playerPosX
    app.projPosY = app.playerPosY
    app.projCount += 1
    app.targetX = event.x
    app.targetY = event.y
    totalX = app.targetX - app.playerPosX
    totalY = app.targetY - app.playerPosY
    app.projAngle = math.atan(totalY/totalX)
    app.projChangeX = app.projSpeed * math.cos(app.projAngle)
    app.projChangeY = app.projSpeed * math.sin(app.projAngle)

def timerFired(app):
    if app.projPosX <= app.terrainWidth and app.projPosX > 0 and \
        app.projPosY < app.terrainHeight and app.projPosY > 0:
        if app.targetX > app.width/2:
            app.projPosX += app.projChangeX
            app.projPosY += app.projChangeY
        else:
            app.projPosX -= app.projChangeX
            app.projPosY -= app.projChangeY

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

runApp(width = 1000, height = 800)


