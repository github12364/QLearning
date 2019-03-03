# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:13:25 2019

@author: Henry
"""
import math
import physics
import copy
import qlearn

import objects as objs

temp = None
add_end = False

def addObject(pygame, background, x):
    if x.name == "car":
        verticies = x.getVerticies()
        pygame.draw.circle(background, (255,0,0), tuple(map(lambda x: int(x+0.5), verticies[0])), 3)
        pygame.draw.circle(background, (0,255,0),tuple(map(lambda x: int(x+0.5), verticies[1])), 3)
        pygame.draw.circle(background, (0,0,255), tuple(map(lambda x: int(x+0.5), verticies[2])), 3)
        pygame.draw.circle(background, (0,0,0), tuple(map(lambda x: int(x+0.5), verticies[3])), 3)
        pygame.draw.polygon(background, (255,0,255), tuple(map(lambda x: tuple(map(lambda y: int(y+0.5), x)), verticies)))
    if x.name == "cone" or x.name == "goal":
        pygame.draw.circle(background, x.color,(int(x.x+0.5),int(x.y+0.5)), int(x.radius+0.5))
    if x.name == "wall":
        pygame.draw.line(background, x.color, (int(x.x+0.5),int(x.y+0.5)),(int(x.x2+0.5),int(x.y2+0.5)), int(x.width+0.5))
    return True

def getPixelBackground(objects, window):
    pixelArray = [[0 for x in range(window.width)] for x in range(window.height)]
    for x in objects:
        if x.name == "car":
            continue
        if x.name == "goal":
            pixels = circlePixelArray(int(x.x+0.5),int(x.y+0.5),x.radius)
            for p in pixels:
                pixelArray[p[1]][p[0]] = 250
                continue
        if x.name == "cone":
            pixels = circlePixelArray(int(x.x+0.5),int(x.y+0.5),x.radius)
        if x.name == "wall":
            pixels = linePixelArray(int(x.x+0.5),int(x.y+0.5),int(x.x2+0.5),int(x.y2+0.5))
        for x in pixels:
            pixelArray[x[1]][x[0]] = 150
    return pixelArray
        
def circlePixelArray(x,y,r):
    radiusSquared = r*r
    pixels = []
    for xc in range(x-r, x+r+1):
        for yc in range(y-r, y+r+1):
            if (x-xc)*(x-xc)+(y-yc)*(y-yc) <= radiusSquared:
                pixels.append((int(x),int(y),))
    return pixels

def getPixelArray(pixelBackground, car):
    for x in range(int(car.x-car.length), int(car.x+car.length)):
        for y in range(int(car.y - car.length), int(car.y+car.length)):
            if pixelBackground[y][x] == 200:
                pixelBackground[y][x] == 0
    verticies = car.getVerticies()
    pixels = []
    pixels += linePixelArray(*list(map(lambda x: int(x+0.5),(verticies[0]+verticies[1]))))
    pixels += linePixelArray(*list(map(lambda x: int(x+0.5),(verticies[1]+verticies[2]))))
    pixels += linePixelArray(*list(map(lambda x: int(x+0.5),(verticies[2]+verticies[3]))))
    pixels += linePixelArray(*list(map(lambda x: int(x+0.5),(verticies[3]+verticies[0]))))
    for x in pixels:
        pixelBackground[x[1]][x[0]] = 200
    return pixelBackground

def linePixelArray(x0, y0, x1, y1):
    pixels = []
    deltax = x1 - x0
    deltay = y1 - y0
    if deltax == 0:
        return [(x0, y) for y in range(y0,y1+1)]
    deltaerr = abs(deltay / deltax)
    error = 0.0 
    y = y0
    for x in range(x0, x1):
        pixels.append((int(x),int(y),))
        error = error + deltaerr
        if error >= 0.5:
            y = y + deltay / abs(deltay) * 1
            error = error - 1.0
    return pixels

def render(pygame, screen, background, objects, window):
    background.fill(window.color)
    for x in objects:
        addObject(pygame, background, x)
    screen.blit(background, (0, 0))
    pygame.display.update()
            
    
def update(objects, FPS, choices, window):
    car = objects[0]
    if car.x < car.length*2 or car.y < car.length*2 or car.x > window.width - car.length*2 or car.y > window.height - car.length*2:
        return False
    for x in objects:
        if x.name == "car":
            car.update(choices, FPS)
            continue
        if x.name == "goal":
            collision = physics.carCircle(car, x)
            if collision: 
                x.color = (255,255,255)
                return "win"
            continue
            
        if x.name == "cone":
            collision = physics.carCircle(car, x)
        if x.name == "wall":
            collision = physics.carLine(car, (x.x,x.y,x.x2,x.y2))
        if collision:
            x.color = (0,0,0)
            return False
        else:
            x.color = (255, 0, 0)
    return True
        
def addCone(objects, x, y):
    objects.append(objs.Cone(x, y, 20, (255,0,0)),)

def addWall(objects, x, y, x2, y2):
    objects.append(objs.Wall(x, y, x2, y2, 5, (255,0,0)),)

def addGoal(objects, x, y):
    objects.append(objs.Goal(x, y, 20, (0,255,0)),)

def checkEvents(pygame, objects, choices):
    global temp
    global add_end
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            return "quit"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if add_end:
                addGoal(*((objects,) + pygame.mouse.get_pos()))
            elif event.button == 3:
                addCone(*((objects,) + pygame.mouse.get_pos()))
            else:
                temp = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if temp:
                addWall(*((objects,) + temp + pygame.mouse.get_pos()) )
                temp = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"
            if event.key == pygame.K_LEFT:
                choices[1]=-1
            if event.key == pygame.K_RIGHT:
                choices[1]=1
            if event.key == pygame.K_UP:
                choices[0]=1
            if event.key == pygame.K_DOWN:
                choices[0]=-1
            if event.key == pygame.K_e:
                add_end = True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                choices[1]=0
            if event.key == pygame.K_RIGHT:
                choices[1]= 0
            if event.key == pygame.K_UP:
                choices[0]=0
            if event.key == pygame.K_DOWN:
                choices[0]=0
            if event.key == pygame.K_e:
                add_end = False

            

def init(pygame, window):
    pygame.init()
    screen = pygame.display.set_mode((window.width, window.height))
    pygame.display.set_caption(window.name)
    pygame.mouse.set_visible(1)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(window.color)
    return screen, background



def run(pygame, screen, background, objectList, game_loop, window, pixelBackground):
    clock = pygame.time.Clock()
    choices = [0,0]
    ql = qlearn.QLearn()
    while game_loop.run == True:
        render(pygame, screen, background, objectList, window)
        status = update(objectList, game_loop.FPS, choices, window)
        action = checkEvents(pygame, objectList, choices)
        pixelArray = getPixelArray(pixelBackground, objectList[0])
        choices = ql.chooseAction(pixelArray)
        if action == "quit":
            game_loop.run = False
            return 1
        if status == False: 
            return 0
        clock.tick(game_loop.FPS)