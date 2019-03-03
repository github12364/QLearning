import math

class Map:
    def __init__(self, width, height, name, color):
        self.width = width
        self.height = height
        self.name = name
        self.color = color
        
class Car:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.angle = 0
        self.v = 0
        self.a = 1
        self.rv = math.pi / 180
        self.length = 100
        self.width = 50
        self.color = color
        self.name = "car"

    def turn(self, direction):
        if direction == "right":
            self.angle = (self.angle + self.rv) % (2 * math.pi)
        elif direction == "left":
            self.angle = (self.angle - self.rv) % (2 * math.pi)

    def accelerate(self):
        self.v += 1
        self.x += self.v * math.sin(self.angle)
        self.y += self.v * math.cos(self.angle)
            
    def decelerate(self):
        self.v -= 1
        self.x -= self.v * math.sin(self.angle)
        self.y -= self.v * math.cos(self.angle)
        
    def getVerticies(self):
        frontright = (self.x+math.cos(self.angle)*self.length/2-math.sin(self.angle)*self.width/2, 
                     self.y + math.sin(self.angle)*self.length/2+math.cos(self.angle)*self.width/2,)
        
        frontleft = (self.x+math.cos(self.angle)*self.length/2+math.sin(self.angle)*self.width/2, 
                      self.y + math.sin(self.angle)*self.length/2-math.cos(self.angle)*self.width/2,)
        
        backright = (self.x-math.cos(self.angle)*self.length/2-math.sin(self.angle)*self.width/2, 
                     self.y - math.sin(self.angle)*self.length/2+math.cos(self.angle)*self.width/2,)
        
        backleft = (self.x - math.cos(self.angle)*self.length/2+math.sin(self.angle)*self.width/2, 
                      self.y - math.sin(self.angle)*self.length/2-math.cos(self.angle)*self.width/2,)
        return (frontright, frontleft, backleft, backright)

class Obstructions:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name

class Cone(Obstructions):
    def __init__(self, x, y, radius, color):
        Obstructions.__init__(self, x, y, color, "cone")
        self.radius = radius

class Wall(Obstructions):
    def __init__(self, x, y, x2, y2, width, color):
        Obstructions.__init__(self, x, y, color, "wall")
        self.x2 = x2
        self.y2 = y2
        self.width = width
    
class Pedestrian(Obstructions): 
    def __init__(self, x, y, x2, y2, v, color):
        Obstructions.__init__(self, x, y, color, "pedestrian")
        self.x2 = x2
        self.y2 = y2
        self.v = v
        self.distance = math.sqrt(math.pow((self.x2 - self.x), 2) + math.pow((self.y2 - self.y), 2))
        self.move()

    def move(self):
        while self.x != self.x2 and self.y != self.y2:
            if self.x > self.x2 and self.y > self.y2:
                self.x -= self.v
