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
move_dict =	{
  0: [-1,-1],
  1: [0,0],
  2: [1,1],
  3: [0,1],
  4: [0,0],
  5: [0,-1],
  6: [1,-1],
  7: [1,0],
  8: [1,1]
}

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

def getPixelBackground(objects, background, window):
    pixelArray = [[0 for x in range(window.width)] for x in range(window.height)]
    for x in range(window.width):
        for y in range(window.height):
            pixelArray[y][x] = int(sum(background.get_at((x, y))[:3])/3)
    return pixelArray
        
def getPixelArray(pixelBackground, car):
    pixelArray = copy.deepcopy(pixelBackground)
    carx = int(car.x/30+0.5)
    cary = int(car.y/30+0.5)
    for i in range(carx-1, carx+2):
        for j in range(cary -1, cary + 2):
            pixelArray[j][i] -= 50
    pixelArray[cary][carx] = 0
    return pixelArray



def render(pygame, screen, background, objects, window):
    return;
    background.fill(window.color)
    for x in objects:
        addObject(pygame, background, x)
    screen.blit(background, (0, 0))
    pygame.display.update()
            
    
def renderfirst(pygame, screen, background, objects, window):
    background.fill(window.color)
    for x in objects:
        if x.name == 'car':
            continue
        addObject(pygame, background, x)
    screen.blit(background, (0, 0))
    pygame.display.update()
    
def update(objects, FPS, choices, window):
    car = objects[0]
    if car.x < car.length/2 or car.y < car.length/2 or car.x > window.width - car.length/2 or car.y > window.height - car.length/2:
        return "punish"
    for x in objects:
        if x.name == "car":
            car.update(choices, FPS)
            continue
        if x.name == "goal":
            collision = physics.carCircle(car, x)
            if collision: 
                x.color = (0,255,0)
                return "win"
            continue
            
        if x.name == "cone":
            collision = physics.carCircle(car, x)
        if x.name == "wall":
            collision = physics.carLine(car, (x.x,x.y,x.x2,x.y2))
        if collision:
            x.color = (0,0,0)
            return "punish"
        else:
            x.color = (255, 0, 0)
    return True
        
def addCone(objects, x, y):
    objects.append(objs.Cone(x, y, 50, (255,0,0)),)

def addWall(objects, x, y, x2, y2):
    objects.append(objs.Wall(x, y, x2, y2, 50, (255,0,0)),)

def addGoal(objects, x, y):
    objects.append(objs.Goal(x, y, 25, (0,255,0)),)

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

def compressPixelArray(pixelArray, step):
    output = []
    for y in range(0, len(pixelArray), step):
        tempArray = []
        for x in range(0, len(pixelArray[y]), step):
            val = 0
            for i in range(step):
                for j in range(step):
                    val += pixelArray[y+i][x+j]
            val = int(val / (step*step))
            tempArray.append(val)
        output.append(tempArray)
    return output

def init(pygame, window):
    pygame.init()
    screen = pygame.display.set_mode((window.width, window.height))
    pygame.display.set_caption(window.name)
    pygame.mouse.set_visible(1)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(window.color)
    return screen, background


def run(pygame, screen, background, objectList, game_loop, window, pixelBackground, ql):
    clock = pygame.time.Clock()
    choices = [0,0]
    p_pixelArray = None
    while game_loop.run == True:
        render(pygame, screen, background, objectList, window)
        status = update(objectList, game_loop.FPS, choices, window)
        action = checkEvents(pygame, objectList, choices)
        pixelArray = getPixelArray(pixelBackground, objectList[0])
        if p_pixelArray != None:
            choices = move_dict[ql.observe(p_pixelArray, pixelArray, status)]
        else:
            choices = [0, 0]
        p_pixelArray = pixelArray
        if action == "quit":
            game_loop.run = False
            return 1
        if status == "punish":
            ql.updateAction(-500, True)
            return
        elif status == "win":
            ql.updateAction(500, True)
