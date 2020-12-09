from cmu_112_graphics import *
import math
import random
from classes import *

def appStarted(app):

    app.rover = Rover(0, 0)
    app.splash = True
    app.angle = 0
    app.popupMessage = None
    app.numObjectives = 0
    app.daytime = False

    app.sampling = False
    app.sampleAttached = False
    app.samplingX = app.width*7/8
    app.samplingY = 1


    # define fonts
    app.titleFont = 'Arial 36 bold'
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

    sx, sy = x1 + (x2 - x1)*2/3, y1 + (y2 - y1)/2
    app.buttons["sample"] = (sx, sy, size)

    # initialize objectives
    app.objectives = []
    #app.objectives.append(Objective("deploy from lander"))
    for i in range(3):
        app.objectives.append(PictureObjectives(app.numObjectives))
        app.numObjectives += 1
    for i in range(2):
        app.objectives.append(SampleObjectives(app.numObjectives))
        app.numObjectives += 1
    app.objectives.append(Objective("reach destination", app.numObjectives))

    # create obstacles
    app.obstacles = []
    app.obstacles.append(Crater(app, 10))
    app.obstacles.append(Crater(app, 10))
    app.obstacles.append(Crater(app, 10))
    app.obstacles.append(Crater(app, 10))

def resetAll(app):
    # counter that increments every 10 ms
    app.time = 0

    app.angle = 0

    app.latitude = random.randint(-100, 100)
    app.longitude = random.randint(-100, 100)

    # create rover
    app.rover = Rover(0, 0)

    # clear progress file
    with open("progress.txt", "wt") as f:
        f.write("")


def retrieveProgress(app):
    content = readFile("progress.txt")

    lines = content.split("\n")
    data = []
    lines.pop()         # extra empty line at the end for some reason
    for line in lines:
        i = line.find(':')
        d = line[i+2:]
        if('.' in d):
            data.append(float(d))
        elif(d.isalpha()):
            data.append(bool(d))
        else:
            data.append(int(d))

    
    app.rover = Rover(data[0], data[1])
    app.rover.percentCharged = data[2]
    app.rover.percentWorn = data[3]
    app.rover.temperature = data[4]

    app.time = data[5]

    # picture objectives
    for i in range(data[6]):
        app.obstacles[i].completed = True

    # sample objectives
    for i in range(data[7]):
        app.obstacles[2 + i].completed = True

    app.obstacles[-1].completed = data[8]
    app.latitude = data[9]
    app.longitude = data[10]

    app.angle = data[11]

    # retrieve coordinates of mission checkpoints
    i = 12
    while(i < len(data)):
        index = (i - 12)//2
        app.objectives[index].checkpointLat = data[i]
        app.objectives[index].checkpointLong = data[i+1]
        i += 2

def saveProgress(app):
    # save relevant data to progress file
    output = ""
    output += f"latitude: {app.rover.latitude}\n"
    output += f"longitude: {app.rover.longitude}\n"
    output += f"charge: {app.rover.percentCharged}\n"
    output += f"damage: {app.rover.percentWorn}\n"
    output += f"temperature: {app.rover.temperature}\n"
    output += f"time: {app.time}\n"

    picturesTaken = 0
    for i in range(0, 3):
        if(app.objectives[i].completed):
            picturesTaken += 1
    output += f"pictures: {picturesTaken}\n"

    samplesTaken = 0
    for i in range(3, 5):
        if(app.objectives[i].completed):
            samplesTaken += 1
    output += f"samples: {samplesTaken}\n"

    output += f"destinationObjective: {app.objectives[-1].completed}\n"
    output += f"destinationLatitude: {app.latitude}\n"
    output += f"destinationLongitude: {app.longitude}\n"

    output += f"angle: {app.angle}\n"

    for objective in app.objectives[:-1]:
        output += f"checkpointLat: {objective.checkpointLat}\n"
        output += f"checkpointLong: {objective.checkpointLong}\n"

    writeFile("progress.txt", output)

def timerFired(app):
    if(not app.splash):
        app.time += 1

        if(90 < app.angle < 270):
            app.daytime = True
            app.rover.charge()
        else:
            app.daytime = False    

        # rotate Mars
        # 360 degrees per 24.6 hours
        # 360 degrees per 1476 minutes
        # 360 degrees per 88560 seconds
        # 360 degrees per 88560 scaled timerFireds
        # rotate 0.0041 degrees every timerFired 
        app.angle += 0.0041

        # completely turned away from the sun at 0/360 and completely facing the sun at 180
        app.angle %= 360
        if(app.angle < 180):
            app.rover.chargingRate = (app.angle/180)*0.05
        else:
            app.rover.chargingRate = ((180-app.angle)/180)*0.05

        # update progress file
        saveProgress(app)

        # check if there is a popup that needs to go away
        if(app.popupMessage != None and app.time > app.popupStart + 15):
            app.popupMessage = None

# reset star locations if window size changes
def sizeChanged(app):
    for i in range(100):
        app.stars[i] = Star(app)

def mousePressed(app, event):
    x, y = event.x, event.y

    # camera button
    cx, cy, size = app.buttons["camera"]
    if(((cx - size*2) < x < (cx + size*2)) and 
        ((cy - size) < y < (cy + size))):
        takePicture(app)

    # sample button
    cx, cy, size = app.buttons["sample"]
    if(((cx - size*2) < x < (cx + size*2)) and 
        ((cy - size) < y < (cy + size))):
        takeSample(app)

    # track mouse click for sampling game
    if(app.sampling):
        app.samplingX = x

def keyPressed(app, event):

    # splash page controls
    if(app.splash):
        if(event.key == 'r'):
            app.splash = False
            resetAll(app)
        if(event.key == 'Space'):
            app.splash = False
            retrieveProgress(app)

    # sampling mini game controls
    elif(app.sampling):
        if(event.key == 'Down'):
            app.samplingY += 10
        elif(event.key == 'Up'):
            app.samplingY -= 10
            if(app.samplingY < 0):
                takeSample(app)
                app.sampleAttached = False
                app.sampling = False
        elif(event.key == 'Space'):
            app.sampleAttached = True

    else:
        # rover mobility keys
        # obstacles become larger as they come closer
        if(event.key == "Up" or event.key == "w") and app.rover.latitude < 100:
            moveBackground(app, (0, 1), 0.1)
            app.rover.latitude += 0.5
        elif(event.key == "Down" or event.key == "s") and app.rover.latitude > -100:
            moveBackground(app, (0, -1), -0.1)
            app.rover.latitude -= 0.5
        elif(event.key == "Left" or event.key == "a") and app.rover.longitude > - 100:
            moveBackground(app, (1, 0), 0)
            app.rover.longitude -= 0.5
        elif(event.key == "Right" or event.key == "d") and app.rover.longitude < 100:
            moveBackground(app, (-1, 0), 0)
            app.rover.longitude += 0.5

        checkMove(app)

        # other controls
        if(event.key == "c"):     # camera
            takePicture(app)
        elif(event.key == "v"):     # sampler
            app.sampling = True
        elif(event.key == 'r'):
            resetAll(app)

        # increment rover stats
        app.rover.spendCharge()
        app.rover.wear()

def checkMove(app):
    # check for collisions
    for obstacle in app.obstacles:
        if((app.rover.lx > obstacle.x - obstacle.xr) or
            (app.rover.rx < obstacle.x + obstacle.xr) or
            (app.rover.ty < obstacle.y - obstacle.yr) or
            (app.rover.by > obstacle.y + obstacle.yr)):
            app.rover.wear()

    # check if rover is going out of mission bounds
    if((not -100 < app.rover.latitude < 100) or
        (not -100 < app.rover.longitude < 100)):
        sendWarning(app, "Out of mission bounds")

    # check if destination is reached
    if((app.rover.latitude, app.rover.longitude) == (app.latitude, app.longitude)):
        app.objectives[-1].checkOff()


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
    angleOfRotation = 25.2
    earthHoursPerRotation = 24.6

    

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
        if(isinstance(objective, PictureObjectives) and 
        (objective.completed == False) and
        (app.rover.latitude, app.rover.longitude) == objective.getCheckpoint()):
            objective.checkOff()
            break

def takeSample(app):
    for objective in app.objectives:
        if(isinstance(objective, SampleObjectives) and 
            objective.completed == False and
            (app.rover.latitude, app.rover.longitude) == objective.getCheckpoint()):
            objective.checkOff()
            break
    previous = readFile("samples.txt")
    current = previous + f"{earthToMarsTime(app)}, sample taken\n"
    writeFile("samples.txt", current)

def sendWarning(app, message):
    # warn player if charge is low, damage is high, or temp is critical
    app.popupMessage = message
    app.popupStart = app.time

def drawPopUp(app, canvas):
    canvas.create_rectangle(app.width*1/3, app.height*1/10, app.width*2/3, app.height*2/10, fill = "light gray", width = 0)
    canvas.create_text(app.width/2, app.height*3/20, text = app.popupMessage, font = app.headerFont)

def drawSplashScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "tomato4")
    canvas.create_text(app.width/1.99, app.height/5.1, text = "Mission Control", font = app.titleFont)  # text shadow
    canvas.create_text(app.width/2, app.height/5, text = "Mission Control", fill = "SteelBlue4", font = app.titleFont)
    canvas.create_text(app.width/2, app.height*1.5/5, text = "Press 'r' to start a new mission", font = app.headerFont)
    canvas.create_text(app.width/2, app.height*6/7, text = "Press SPACE to continue the current mission", font = app.headerFont)
    app.rover.draw(app, canvas)

def drawCameraFeedSection(app, canvas):
    x1, y1, x2, y2 = app.width//5, 0, app.width*4//5, app.height*3//4

    # draw mars
    canvas.create_rectangle(x1, y1 + y2//3, x2, y2, fill = "tomato4")

    # draw obstacles
    for obstacle in app.obstacles:
        obstacle.draw(app, canvas)

    # draw rover
    app.rover.draw(app, canvas)

    if(app.daytime):
        # draw sky
        gradient = int((app.angle/360)*150)
        color = rgbString(gradient, gradient, 100)
        canvas.create_rectangle(x1, y1, x2, y2//3, fill = color)
        # draw sun's position based on angle of Mars
        sunR = app.height//20
        sunX = ((app.angle-90)/180)*(x2 - x1)
        canvas.create_oval(sunX + sunR, y2//5 + sunR, sunX - sunR, y2//5 - sunR, 
                            fill = "light goldenrod", width = 0)
    else:
        # draw sky
        canvas.create_rectangle(x1, y1, x2, y2//3, fill = "black")
        # draw stars
        for star in app.stars:
            star.draw(canvas)
        # draw demos and phobos based on angle of Mars
        moonsR = app.height//20
        moonsX = ((abs(app.angle-90))/180)*(x2 - x1)
        # deimos
        canvas.create_oval(moonsX + moonsR, y2//5 + moonsR, moonsX - moonsR, y2//5 - moonsR, 
                            fill = "AntiqueWhite2", width = 0)
        # phobos
        canvas.create_oval(moonsX + moonsR + 3*moonsR, y2//5 + moonsR, moonsX - moonsR + 3*moonsR, y2//5 - moonsR, 
                            fill = "seashell4", width = 0)

def drawMissionSection(app, canvas):
    x1, y1, x2, y2 = 0, 0, app.width//5, app.height
    canvas.create_rectangle(x1, y1, x2, y2, fill = "slate gray")

    # draw map
    mx1, my1, mx2, my2 = x2//8, y2//20, x2*7//8, y2*3//10
    canvas.create_rectangle(mx1, my1, mx2, my2, fill = "tomato4")
    # rover location
    r = (mx2 - mx1)/25
    la = 0.7*app.rover.latitude
    lo = 0.8*app.rover.longitude
    canvas.create_oval(mx1 + lo + (mx2-mx1)/2 - r, my1 - la + (mx2-mx1)/2 - r, 
                        mx1 + lo + (mx2-mx1)/2 + r, my1 - la + (mx2-mx1)/2 + r, 
                        fill = "DeepSkyBlue4", width = 0)
    # destination
    dx = 0.9*(mx2 - mx1)*app.latitude//200 + mx1 + (mx2 - mx1)//2    # based on longitude
    dy = 0.9*(my2 - my1)*app.longitude//200 + my1 + (my2 - my1)//2    # based on latitude  
    canvas.create_oval(dx + r, dy + r, dx - r, dy - r, fill = "blue", width = 0)
    canvas.create_text(dx, dy, text = "5", fill = "white", font = app.paragraphFont)

    # checkpointa
    for i in range(len(app.objectives)-1):
        app.objectives[i].drawOnMap(app, canvas, i)

    # draw objectives
    canvas.create_text(x2//2, y2//3, text = "Objectives", fill = 'black', font = app.headerFont)
    for i in range(len(app.objectives)):
        goal = app.objectives[i]
        x = x2//8
        y = y2//3 + 30*(i+1)
        goal.draw(app, canvas, x, y)

    # write mission location Mawrth Vallis
    canvas.create_text(x2/2, y2*8/9, text = "location: Mawrth Vallis", font = app.paragraphFont)

def drawRoverInfoSection(app, canvas):
    x1, y1, x2, y2 = app.width*4//5, 0, app.width, app.height
    canvas.create_rectangle(x1, y1, x2, y2, fill = "slate gray")

    # draw rover
    canvas.create_rectangle(x1 + (x2-x1)//8, y2//20, x1 + (x2-x1)*7//8, y2*3//10, fill = "black")

    # draw stats
    margin = 30
    canvas.create_text(x1 + (x2-x1)//2, y2//3, text = "Rover Stats", fill = 'black', font = app.headerFont)
    canvas.create_text(x1 + (x2-x1)//8, y2//3 + margin, 
                        text = f"Battery Charge: {int(app.rover.percentCharged)}%", fill = 'black', 
                        font = app.paragraphFont, anchor = "nw")
    canvas.create_text(x1 + (x2-x1)//8, y2//3 + 2*margin, 
                        text = f"Temperature: {app.rover.temperature} C", fill = 'black', 
                        font = app.paragraphFont, anchor = "nw")
    canvas.create_text(x1 + (x2-x1)//8, y2//3 + 3*margin, 
                        text = f"Wear and Tear: {int(app.rover.percentWorn)}%", fill = 'black', 
                        font = app.paragraphFont, anchor = "nw")

    if(app.sampling):
        drawSampleGame(app, canvas)

    # draw time
    s, h, m = earthToMarsTime(app)
    canvas.create_text(x1 + (x2-x1)//8, y2*7/8, 
                        text = f"Sol {s}, {h}:{m}", fill = 'black', 
                        font = app.paragraphFont, anchor = "nw")

def drawSampleGame(app, canvas):

    x1, y1, x2, y2 = app.width*4//5, 0, app.width, app.height

    canvas.create_rectangle(x1 + (x2-x1)//8, y2//20, x1 + (x2-x1)*7//8, y2*3//10, fill = "tomato4")
    canvas.create_rectangle(x1 + (x2-x1)//8, y2//20, x1 + (x2-x1)*7//8, y2*3//15, fill = "black")

    x = app.samplingX

    if(x < x1 + (x2-x1)//8):
        x = x1 + (x2-x1)//8
    elif(x > x1 + (x2-x1)*7//8):
        x = x1 + (x2-x1)*7//8

    # draw sampling arm
    sampleSize = app.width/40
    bottomY = y2/10 + app.samplingY
    canvas.create_rectangle(x - sampleSize, y2/15, x, bottomY, 
                            fill = "NavajoWhite4", width = 0)   # vertical piece
    size = x - (x1 + (x2-x1)//8)
    canvas.create_rectangle(x - size, y2/15, x, y2/10, 
                            fill = "NavajoWhite3", width = 0)   # horizontal piece

    # draw soil sample
    sx = x1 + (x2-x1)//2
    if(app.sampleAttached):
        canvas.create_rectangle(sx - sampleSize, bottomY - sampleSize, sx, bottomY, fill = "tomato3", width = 0)
    else:
        canvas.create_rectangle(sx - sampleSize, y2*3//15, sx, y2*3//15 + sampleSize, fill = "tomato3", width = 0)

def drawRoverControlSection(app, canvas):
    x1, y1, x2, y2 = app.width//5, app.height*3//4, app.width*4//5, app.height
    canvas.create_rectangle(x1, y1, x2, y2, fill = "gray")

    # camera button
    cx, cy, size = app.buttons["camera"]
    canvas.create_rectangle(cx + size*2, cy + size, cx - size*2, cy - size, fill = "blue", width = 0)
    canvas.create_text(cx, cy, text = "camera", fill = "white", font = app.paragraphFont)

    # sample button
    sx, sy, size = app.buttons["sample"]
    canvas.create_rectangle(sx + size*2, sy + size, sx - size*2, sy - size, fill = "blue", width = 0)
    canvas.create_text(sx, sy, text = "sampler", fill = "white", font = app.paragraphFont)


# from 112 course notes: https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

# from collab 4
def rgbString(red, green, blue):
    return f'#{red:02x}{green:02x}{blue:02x}'

def redrawAll(app, canvas):
    if(app.splash):
        drawSplashScreen(app, canvas)
    else:
        canvas.create_rectangle(0, 0, app.width, app.height, fill = "dim gray")
        drawCameraFeedSection(app, canvas)
        drawMissionSection(app, canvas)
        drawRoverInfoSection(app, canvas)
        drawRoverControlSection(app, canvas)
        if(app.popupMessage != None):
            drawPopUp(app, canvas)

runApp(width=1100, height=600)