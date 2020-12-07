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

    # rover control button locations
    x1, y1, x2, y2 = app.width//5, app.height*3//4, app.width*4//5, app.height
    app.buttons = dict()
    cx, cy = x1 + (x2 - x1)/3, y1 + (y2 - y1)/2
    size = y2/30
    app.buttons["camera"] = (cx, cy, size)

    resetAll(app)

def resetAll(app):
    # counter that increments every 10 ms
    app.time = 0

    # dawn, midday, dusk, night
    # 0,    1,      2,    3
    app.timeOfDay = 0

    latitude = random.randint(-100, 100)
    longitude = random.randint(-100, 100)
    app.destination = (latitude, longitude)

    # create rover
    app.rover = Rover(0, 0)

    # initialize objectives
    app.objectives = []
    app.objectives.append(Objective("deploy from lander"))
    app.objectives.append(PictureObjectives())
    app.objectives.append(PictureObjectives())
    app.objectives.append(PictureObjectives())

    app.objectives.append(Objective("collect samples (1 of 5)"))
    app.objectives.append(Objective("reach destination"))
    app.objectives[-1].checkOff()

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
    cx, cy, size = app.buttons["camera"]
    if(((cx - size*2) < x < (cx + size*2)) and 
        ((cy - size) < y < (cy + size))):
        takePicture(app)

def keyPressed(app, event):
    # rover mobility keys
    # obstacles become larger as they come closer
    if(event.key == "Up" or event.key == "w"):
        moveBackground(app, (0, 1), 0.1)
        app.rover.latitude += 0.5
    elif(event.key == "Down" or event.key == "s"):
        moveBackground(app, (0, -1), -0.1)
        app.rover.latitude -= 0.5
    elif(event.key == "Left" or event.key == "a"):
        moveBackground(app, (1, 0), 0)
        app.rover.longitude -= 0.5
    elif(event.key == "Right" or event.key == "d"):
        moveBackground(app, (-1, 0), 0)
        app.rover.longitude += 0.5

    # check for collisions
    for obstacle in app.obstacles:
        if((app.rover.lx > obstacle.x - obstacle.xr) or
            (app.rover.rx < obstacle.x + obstacle.xr) or
            (app.rover.ty < obstacle.y - obstacle.yr) or
            (app.rover.by > obstacle.y + obstacle.yr)):
            app.rover.percentWorn += 10

    # check if destination is reached
    if((app.rover.latitude, app.rover.longitude) == app.destination):
        app.objectives[-1].checkOff()

    # other controls
    if(event.key == "Space"):
        pass
    elif(event.key == "c"):     # camera
        takePicture(app)
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

def positionOfSun(app):
    # physics with the orbits and rotations of mars and the sun
    # to determine where the sun is in the sky

    pass

def earthToMarsTime(app):
    timeScale = 100     # time passed in the game relative to real life
    scaledTime = app.time * timeScale
    seconds = scaledTime//1000
    minutes = seconds//60
    minute = seconds%60
    hours = minutes//60
    hour = int(hours%24.6)
    sol = int(hours//24.6)
    return sol, hour, minute

def takePicture(app):
    for objective in app.objectives:
        if(isinstance(objective, PictureObjectives) and objective.completed == False):
            objective.checkOff()
            break

def drawCameraFeedSection(app, canvas):
    x1, y1, x2, y2 = app.width//5, 0, app.width*4//5, app.height*3//4

    # draw mars
    canvas.create_rectangle(x1, y1 + y2//3, x2, y2, fill = "tomato4")

    # draw obstacles
    for obstacle in app.obstacles:
        obstacle.draw(app, canvas)

    # draw rover
    app.rover.draw(app, canvas)

    # draw sky
    canvas.create_rectangle(x1, y1, x2, y2//3, fill = "black")

    # draw stars
    for star in app.stars:
        star.draw(canvas)

    # draw demos and phobos

def drawMissionSection(app, canvas):
    x1, y1, x2, y2 = 0, 0, app.width//5, app.height
    canvas.create_rectangle(x1, y1, x2, y2, fill = "slate gray")

    # draw map
    mx1, my1, mx2, my2 = x2//8, y2//20, x2*7//8, y2*3//10
    canvas.create_rectangle(mx1, my1, mx2, my2, fill = "tomato4")
    # rover location
    r = (mx2 - mx1)/20
    la = app.rover.latitude
    lo = app.rover.longitude
    canvas.create_oval(mx1 + lo + (mx2-mx1)/2 - r, my1 - la + (mx2-mx1)/2 - r, 
                        mx1 + lo + (mx2-mx1)/2 + r, my1 - la + (mx2-mx1)/2 + r, 
                        fill = "DeepSkyBlue4", width = 0)
    # destination
    dx = 0.9*(mx2 - mx1)*app.destination[1]//200 + mx1 + (mx2 - mx1)//2    # based on longitude
    dy = 0.9*(my2 - my1)*app.destination[0]//200 + my1 + (my2 - my1)//2    # based on latitude  
    canvas.create_oval(dx + r, dy + r, dx - r, dy - r, fill = "blue", width = 0)

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

    # draw time
    s, h, m = earthToMarsTime(app)
    canvas.create_text(x1 + (x2-x1)//8, y2*7/8, 
                        text = f"Sol {s}, {h}:{m}", fill = 'black', 
                        font = app.paragraphFont, anchor = "nw")

def drawRoverControlSection(app, canvas):
    x1, y1, x2, y2 = app.width//5, app.height*3//4, app.width*4//5, app.height
    canvas.create_rectangle(x1, y1, x2, y2, fill = "gray")

    # camera button
    cx, cy, size = app.buttons["camera"]
    canvas.create_rectangle(cx + size*2, cy + size, cx - size*2, cy - size, fill = "blue", width = 0)
    canvas.create_text(cx, cy, text = "camera", fill = "white", font = app.paragraphFont)

    # sample button
    #app.buttons["sample"] = x, y


# from 112 course notes
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

# contentsToWrite = "This is a test!\nIt is only a test!"
# writeFile("foo.txt", contentsToWrite)

# contentsRead = readFile("foo.txt")

def redrawAll(app, canvas):
    #draw background
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "dim gray")
    drawCameraFeedSection(app, canvas)
    drawMissionSection(app, canvas)
    drawRoverInfoSection(app, canvas)
    drawRoverControlSection(app, canvas)

runApp(width=1100, height=600)