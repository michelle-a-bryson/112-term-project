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
        self.inProgress = False
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

class PictureObjectives(Objective):

    total = []
    completed = []
    goal = f"take pictures ({len(completed)} of {len(total)})"

    def __init__(self):
        self.inProgress = False
        self.completed = False
        PictureObjectives.total.append(self)
        print("fuck")

    def checkOff(self):
        self.completed = True
        PictureObjectives.completed.append(self)

    def draw(self, app, canvas, x, y):
        length = app.width/80
        canvas.create_rectangle(x, y, x + length, y + length, width = 2)
        canvas.create_text(x + length*2, y, text = PictureObjectives.goal, 
                            font = app.paragraphFont, fill = "black", anchor = "nw")
        if(self.completed):
            # draw checkmark
            pass

class SampleObjectives(Objective):

    total = []
    completed = []
    goal = f"take samples ({len(completed)} of {len(total)})"

    def __init__(self):
        self.inProgress = False
        self.completed = False
        SampleObjectives.total.append(self)

    def checkOff(self):
        self.completed = True
        SampleObjectives.completed.append(self)

    def draw(self, app, canvas, x, y):
        length = app.width/80
        canvas.create_rectangle(x, y, x + length, y + length, width = 2)
        canvas.create_text(x + length*2, y, text = SampleObjectives.goal, 
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

    def spendCharge(self):
        if(self.percentCharged > 0):
            self.percentCharged -= 1

    def wear(self):
        if(self.percentWorn < 100):
            self.percentWorn += 1

    def damage(self, obstacle):
        pass

    def charge(self):
        self.percentCharged += self.chargingRate

    def upgradeSpeed(self):
        self.speed += 1

    def upgradeChargingEfficiency(self):
        self.chargingRate *= 1.5

class Obstacle(object):

    def __init__(self, app, damage):
        x1, y1, x2, y2 = app.width//5, 0, app.width*4//5, app.height*3//4
        self.damage = damage
        self.size = random.randint(30, 80)
        self.x = random.randint(x1 + int(self.size*1/5), x2 - int(self.size*1.5))
        self.y = random.randint(y2//3 + self.size, y2 - self.size)

class Crater(Obstacle):
    def draw(self, app, canvas):
        xr = self.size * 1.5
        yr = self.size
        canvas.create_oval(self.x - xr, self.y - yr, 
                            self.x + xr, self.y + yr,
                            fill = "firebrick4", width = 0)
