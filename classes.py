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

    def __init__(self):
        self.inProgress = False
        self.completed = False
        PictureObjectives.total.append(self)

    def checkOff(self):
        self.completed = True
        PictureObjectives.completed.append(self)

    def draw(self, app, canvas, x, y):
        goal = f"take pictures ({len(PictureObjectives.completed)} of {len(PictureObjectives.total)})"
        length = app.width/80
        canvas.create_rectangle(x, y, x + length, y + length, width = 2)
        canvas.create_text(x + length*2, y, text = goal, 
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
        x1, y1, x2, y2 = app.width//5, 0, app.width*4//5, app.height*3//4

        y2 *= 1.15

        if(self.level == 0):
            # draw basic rover with no upgrades
            bLeftX = tLeftX = x1 + x2/4
            bRightX = tRightX = x1 + x2*2/5
            bLeftY = bRightY = y2 * 9/10
            tRightY = tLeftY = y2*7.5/10

            fRightX = lRightX = lLeftX = fLeftX = bRightX + x2/20
            lRightY = lLeftY = tRightY - y2/50
            fRightY = fLeftY = tRightY - y2/8

            marginX = x2/50
            marginY = y2/50

            # draw leftmost wheel
            self.drawWheel(app, canvas, bLeftX, bLeftY - marginY, x2/35)

            # draw chassis
            canvas.create_rectangle(bLeftX, bLeftY, tRightX, tRightY, fill = "NavajoWhite2", width = 0)
            canvas.create_polygon(bRightX, bRightY, tRightX, tRightY, 
                                    fRightX, fRightY, lRightX, lRightY, fill = "NavajoWhite3")

            # draw head
            mid = (tRightX - tLeftX)/2 + x2/30
            canvas.create_rectangle(tLeftX + 1.1*mid, fRightY, tLeftX + 1.1*mid + x2/50, fRightY - y2/10, 
                                    fill = "dim gray", width = 0)
            canvas.create_rectangle(tLeftX + mid, fRightY, tLeftX + mid + x2/50, fRightY - y2/10, 
                                    fill = "ivory4", width = 0)
            canvas.create_polygon(tLeftX + mid - x2/30, fRightY - y2/10 - y2/20, 
                                    tLeftX + mid + x2/20, fRightY - y2/10 - y2/20,
                                    tLeftX + mid + x2/18, fRightY - y2/10 - y2/16,
                                    tLeftX + mid - x2/36, fRightY - y2/10 - y2/16, 
                                    fill = "gray", width = 0)
            canvas.create_polygon(tLeftX + mid + x2/20, fRightY - y2/10 - y2/20,
                                    tLeftX + mid + x2/18, fRightY - y2/10 - y2/16,
                                    tLeftX + mid + x2/18, fRightY - y2/9,
                                    tLeftX + mid + x2/20, fRightY - y2/10,
                                    fill = "dim gray", width = 0)
            canvas.create_rectangle(tLeftX + mid - x2/30, fRightY - y2/10, 
                                    tLeftX + mid + x2/20, fRightY - y2/10 - y2/20,
                                    fill = "cornsilk4", width = 0)

            # draw solar panels
            canvas.create_rectangle(tLeftX - marginX, tLeftY - marginY, tRightX + marginX, tRightY, 
                                    fill = "DeepSkyBlue4", width = 0)
            canvas.create_polygon(tLeftX - marginX, tLeftY - marginY, tRightX + marginX, tRightY - marginY,
                                    tRightX + marginX + x2/20, tRightY - marginY - y2/8,
                                    tLeftX - marginX + x2/15, tLeftY - marginY - y2/8, 
                                     fill = "SteelBlue4")
            canvas.create_polygon(tRightX + marginX, tRightY, tRightX + marginX, tRightY - marginY,
                                    tRightX + marginX + x2/20, tRightY - marginY - y2/8,
                                    tRightX + marginX + x2/20, tRightY - y2/8,
                                    fill = "DodgerBlue4")

            # draw wheels
            self.drawWheel(app, canvas, bRightX + 3*marginX, bRightY - 8*marginY, x2/45)
            self.drawWheel(app, canvas, bRightX + 2*marginX, bRightY - 5*marginY, x2/40)
            self.drawWheel(app, canvas, bRightX + marginX, bRightY - marginY, x2/35)


    def drawWheel(self, app, canvas, x, y, r):
        x1, y1, x2, y2 = app.width//5, 0, app.width*4//5, app.height*3//4
        thickness = x2/100
        canvas.create_oval(x - thickness + r/2, y + r, x - thickness - r/2, y - r, 
                            fill = "dim gray", width = 0)
        canvas.create_rectangle(x- thickness, y + r, x, y - r, fill = "dim gray", width = 0)
        canvas.create_oval(x + r/2, y + r, x - r/2, y - r, fill = "gray", width = 0)
        

    
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
        self.size = random.randint(20, 50)
        self.x = random.randint(x1 + int(self.size*1/5), x2 - int(self.size*1.5))
        self.y = random.randint(y2//3 + self.size, y2 - self.size)

class Crater(Obstacle):
    def draw(self, app, canvas):
        xr = self.size * 1.5
        yr = self.size
        canvas.create_oval(self.x - xr, self.y - yr, 
                            self.x + xr, self.y + yr,
                            fill = "firebrick4", width = 0)
