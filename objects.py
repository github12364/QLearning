import math

class Map:
    def __init__(self, length, height):
        self.length = length
        self.height = height
        
class Car:
    def __init__(self, x, y, a, ra):
        self.x = x
        self.y = y
        self.angle = 0
        self.v = 0
        self.a = 1
        self.rv = math.pi / 180

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

class Obstructions:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.type = name
    
        
