from cmu_112_graphics import *
import math

def mousePressed(app,event):
    app.mouseX = event.x
    app.mouseY = event.y

def drawSprite(app,canvas):
    spriteWidth = 20
    spriteHeight = 30
    r = spriteWidth/2
    theta = 0
    #canvas.create_rectangle(200+spriteWidth/2,200+spriteHeight/2,200-spriteWidth/2,200-spriteHeight/2,)
    canvas.create_rectangle(250+(r*(math.cos(theta)))+((spriteWidth/2)*math.cos(theta)), \
                            250+(r*(math.sin(theta)))+((spriteHeight/2)*math.cos(theta)),\
                            250+(r*(math.cos(theta)))-((spriteWidth/2)*math.cos(theta)), \
                            250+(r*(math.sin(theta)))-((spriteHeight/2)*math.cos(theta)))
    canvas.create_line(200,200,300,300)
    print(app.mouseX)
    print(app.mouseY)
    #canvas.create_line(app.width/2,app.height/2,app.mouseX,app.mouseY)
    

def redrawAll(app,canvas):
    drawSprite(app,canvas)

runApp(width=400,height=400)

