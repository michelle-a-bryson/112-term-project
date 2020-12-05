from cmu_112_graphics import *
import math
import random
from classes import *

def appStarted(app):
    # define fonts
    app.titleFont = 'Arial 16 bold'
    app.headerFont = 'Arial 12 bold'
    app.paragraphFont = 'Arial 11'

    # initialize star objects
    app.stars = []
    for i in range(100):
        app.stars.append(Star(app))

    resetAll(app)

def resetAll(app):
    # counter that increments every 10 ms
    app.time = 0

    # initialize objectives
    app.objectives = []
    app.objectives.append(Objective("deploy from lander"))
    app.objectives.append(PictureObjectives())
    app.objectives.append(PictureObjectives())

    app.objectives.append(PictureObjectives())

    app.objectives.append(Objective("take pictures (3 of 10)"))
    app.objectives.append(Objective("collect samples (1 of 5)"))

    # create rover
    app.rover = Rover(0, 0)

    # create obstacles
    app.obstacles = []
    app.obstacles.append(Crater(app, 10))
    app.obstacles.append(Crater(app, 10))
    app.obstacles.append(Crater(app, 10))
    app.obstacles.append(Crater(app, 10))
    app.obstacles.append(Crater(app, 10))

def timerFired(app):
    app.time += 1

    # increment rover stats
    if(app.time%100 == 0):
        app.rover.spendCharge()
    if(app.time%500 == 0):
        app.rover.wear()


# reset star locations if window size changes
def sizeChanged(app):
    for i in range(100):
        app.stars[i] = Star(app)

def mousePressed(app, event):
    x, y = event.x, event.y

def keyPressed(app, event):
    # rover mobility keys
    # obstacles become larger as they come closer
    if(event.key == "Up" or event.key == "w"):
        moveBackground(app, (0, -1), -0.1)
    elif(event.key == "Down" or event.key == "s"):
        moveBackground(app, (0, 1), 0.1)
    elif(event.key == "Left" or event.key == "a"):
        moveBackground(app, (-1, 0), 0)
    elif(event.key == "Right" or event.key == "d"):
        moveBackground(app, (1, 0), 0)
    # other controls
    elif(event.key == "Space"):
        pass
    elif(event.key == 'r'):
        resetAll(app)

def moveBackground(app, dir, dSize):
    dx, dy = dir
    x1, y1, x2, y2 = app.width//5, 0, app.width*4//5, app.height*3//4

    for obstacle in app.obstacles:

        obstacle.x += dx
        obstacle.y += dy
        obstacle.size += dSize
        # for perspective, move right or left
        if((dy == 1 and obstacle.x > app.width/2) or
            (dy == -1 and obstacle.x < app.width/2)):
            obstacle.x += 1
        elif(dy != 0):
            obstacle.x -= 1

        if((obstacle.x < x1 - obstacle.size*1.5) or
            (obstacle.x > x2 + obstacle.size*1.5) or
            (obstacle.y < y1 - obstacle.size) or
            (obstacle.y > y2 + obstacle.size)):
            app.obstacles.pop()
            # add new obstacle
            app.obstacles.append(Crater(app, 10))
            app.obstacles[-1].y = y2//3 + app.obstacles[-1].size
            app.obstacles[-1].size /= 3
        

def drawCameraFeedSection(app, canvas):
    x1, y1, x2, y2 = app.width//5, 0, app.width*4//5, app.height*3//4
    canvas.create_rectangle(x1, y1, x2, y2, fill = "black")

    # draw stars
    for star in app.stars:
        star.draw(canvas)

    # draw mars
    canvas.create_rectangle(x1, y1 + y2//3, x2, y2, fill = "tomato4")

    # draw obstacles
    for obstacle in app.obstacles:
        obstacle.draw(app, canvas)

    # draw rover
    app.rover.draw(app, canvas)

def drawMissionSection(app, canvas):
    x1, y1, x2, y2 = 0, 0, app.width//5, app.height
    canvas.create_rectangle(x1, y1, x2, y2, fill = "slate gray")

    # draw map
    canvas.create_rectangle(x2//8, y2//20, x2*7//8, y2*3//10, fill = "black")

    # draw objectives
    canvas.create_text(x2//2, y2//3, text = "Objectives", fill = 'black', font = app.headerFont)
    for i in range(len(app.objectives)):
        goal = app.objectives[i]
        x = x2//8
        y = y2//3 + 30*(i+1)
        goal.draw(app, canvas, x, y)

def drawRoverInfoSection(app, canvas):
    x1, y1, x2, y2 = app.width*4//5, 0, app.width, app.height
    canvas.create_rectangle(x1, y1, x2, y2, fill = "slate gray")

    # draw rover
    canvas.create_rectangle(x1 + (x2-x1)//8, y2//20, x1 + (x2-x1)*7//8, y2*3//10, fill = "black")

    # draw stats
    margin = 30
    canvas.create_text(x1 + (x2-x1)//2, y2//3, text = "Rover Stats", fill = 'black', font = app.headerFont)
    canvas.create_text(x1 + (x2-x1)//8, y2//3 + margin, 
                        text = f"Battery Charge: {app.rover.percentCharged}%", fill = 'black', 
                        font = app.paragraphFont, anchor = "nw")
    canvas.create_text(x1 + (x2-x1)//8, y2//3 + 2*margin, 
                        text = f"Temperature: {app.rover.temperature} C", fill = 'black', 
                        font = app.paragraphFont, anchor = "nw")
    canvas.create_text(x1 + (x2-x1)//8, y2//3 + 3*margin, 
                        text = f"Wear and Tear: {app.rover.percentWorn}%", fill = 'black', 
                        font = app.paragraphFont, anchor = "nw")

def drawRoverControlSection(app, canvas):
    x1, y1, x2, y2 = app.width//5, app.height*3//4, app.width*4//5, app.height
    canvas.create_rectangle(x1, y1, x2, y2, fill = "gray")

def redrawAll(app, canvas):
    #draw background
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "dim gray")
    drawCameraFeedSection(app, canvas)
    drawMissionSection(app, canvas)
    drawRoverInfoSection(app, canvas)
    drawRoverControlSection(app, canvas)

runApp(width=1100, height=600)