
from cmu_112_graphics import *
import math
import random

class Star(object):

    def __init__(self, app):
        x1, y1, x2, y2 = app.width//5, 0, app.width*4//5, app.height*3//4
        self.x = random.randint(x1, x2)
        self.y = random.randint(y1, y2//3)
        self.r = random.random()*2
        self.color = "white"

    def draw(self, canvas):
        canvas.create_oval(self.x + self.r, self.y + self.r, 
                            self.x - self.r, self.y - self.r, fill = self.color)

def appStarted(app):
    app.stars = []
    for i in range(100):
        app.stars.append(Star(app))

def timerFired(app):
    pass

def mousePressed(app, event):
    pass

def keyPressed(app, event):
    #if(event.key == "Up")
    pass

def drawCameraFeedSection(app, canvas):
    x1, y1, x2, y2 = app.width//5, 0, app.width*4//5, app.height*3//4
    canvas.create_rectangle(x1, y1, x2, y2, fill = "black")

    # draw moon
    canvas.create_rectangle(x1, y1 + y2//3, x2, y2, fill = "light gray")

    # draw stars
    for star in app.stars:
        star.draw(canvas)

def drawMissionSection(app, canvas):
    x1, y1, x2, y2 = 0, 0, app.width//5, app.height
    canvas.create_rectangle(x1, y1, x2, y2, fill = "gray")

    # draw map
    canvas.create_rectangle(x2//8, y2//20, x2*7//8, y2*3//10, fill = "black")

def drawRoverInfoSection(app, canvas):
    x1, y1, x2, y2 = app.width*4//5, 0, app.width, app.height
    canvas.create_rectangle(x1, y1, x2, y2, fill = "gray")

    # draw rover
    canvas.create_rectangle(x1 + (x2-x1)//8, y2//20, x1 + (x2-x1)*7//8, y2*3//10, fill = "black")

def drawRoverControlSection(app, canvas):
    pass

def redrawAll(app, canvas):
    #draw background
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "gray")
    drawCameraFeedSection(app, canvas)
    drawMissionSection(app, canvas)
    drawRoverInfoSection(app, canvas)
    # draw the text
    canvas.create_text(app.width/2, 20,
                       text='Mission Control')

runApp(width=1100, height=600)