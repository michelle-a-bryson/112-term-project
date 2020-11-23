from cmu_112_graphics import *
import math
import random

# draws stars in the camera feed
class Star(object):

    def __init__(self, app):
        x1, y1, x2, y2 = app.width//5, 0, app.width*4//5, app.height*3//4
        self.x = random.randint(x1, x2)
        self.y = random.randint(y1, y2//3)
        self.r = random.random()*1.8
        self.color = "white"

    def draw(self, canvas):
        canvas.create_oval(self.x + self.r, self.y + self.r, 
                            self.x - self.r, self.y - self.r, fill = self.color)

# keeps track of mission objectives
class Objective(object):

    def __init__(self, goal):
        self.goal = goal
        self.completed = False

    def checkOff(self):
        self.completed = True

    def draw(self, app, canvas, x, y):
        length = app.width/80
        canvas.create_rectangle(x, y, x + length, y + length, width = 2)
        canvas.create_text(x + length*2, y, text = self.goal, 
                            font = app.paragraphFont, fill = "black", anchor = "nw")
        if(self.completed):
            # draw checkmark
            pass

class Rover(object):

    def __init__(self, latitude, longitude):
        self.location = (latitude, longitude)
        self.level = 0
        self.speed = 2              # meters per second
        self.percentCharged = 100
        self.temperature = 25       # degrees Celsius
        self.percentWorn = 0
        self.chargingRate = 5

    def draw(self, app, canvas):
        if(self.level == 0):
            # draw basic rover with no upgrade
            pass

    def move(self):
        latitude += self.speed
        longitude += self.speed

    def charge(self):
        self.percentCharged += self.chargingRate

    def upgradeSpeed(self):
        self.speed += 1

    def upgradeChargingEfficiency(self):
        self.chargingRate *= 1.5

def appStarted(app):
    # define fonts
    app.titleFont = 'Arial 16 bold'
    app.headerFont = 'Arial 12 bold'
    app.paragraphFont = 'Arial 11'

    # initialize star objects
    app.stars = []
    for i in range(100):
        app.stars.append(Star(app))

    # initialize objectives
    app.objectives = []
    app.objectives.append(Objective("deploy from lander"))
    app.objectives.append(Objective("travel to mission site"))
    app.objectives.append(Objective("take pictures (3 of 10)"))
    app.objectives.append(Objective("collect samples (1 of 5)"))

    # create rover
    app.rover = Rover(0, 0)

def timerFired(app):
    pass

# reset star locations if window size changes
def sizeChanged(app):
    for i in range(100):
        app.stars[i] = Star(app)

def mousePressed(app, event):
    x, y = event.x, event.y

def keyPressed(app, event):
    # rover mobility keys
    if(event.key == "Up" or event.key == "w"):
        pass
    elif(event.key == "Down" or event.key == "s"):
        pass
    elif(event.key == "Left" or event.key == "a"):
        pass
    elif(event.key == "Right" or event.key == "d"):
        pass
    # other controls
    elif(event.key == "Space"):
        pass

def drawCameraFeedSection(app, canvas):
    x1, y1, x2, y2 = app.width//5, 0, app.width*4//5, app.height*3//4
    canvas.create_rectangle(x1, y1, x2, y2, fill = "black")

    # draw stars
    for star in app.stars:
        star.draw(canvas)

    # draw mars
    canvas.create_rectangle(x1, y1 + y2//3, x2, y2, fill = "tomato4")

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
    pass

def redrawAll(app, canvas):
    #draw background
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "dim gray")
    drawCameraFeedSection(app, canvas)
    drawMissionSection(app, canvas)
    drawRoverInfoSection(app, canvas)

runApp(width=1100, height=600)