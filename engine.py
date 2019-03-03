# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:13:25 2019

@author: Henry
"""
import math
import physics

def addObject(pygame, background, x):
    if x.name == "car":
        verticies = x.getVerticies()
        pygame.draw.circle(background, (255,0,0), tuple(map(lambda x: int(x+0.5), verticies[0])), 3)
        pygame.draw.circle(background, (0,255,0),tuple(map(lambda x: int(x+0.5), verticies[1])), 3)
        pygame.draw.circle(background, (0,0,255), tuple(map(lambda x: int(x+0.5), verticies[2])), 3)
        pygame.draw.circle(background, (0,0,0), tuple(map(lambda x: int(x+0.5), verticies[3])), 3)
        pygame.draw.polygon(background, (255,0,255), tuple(map(lambda x: tuple(map(lambda y: int(y+0.5), x)), verticies)))
    if x.name == "cone":
        pygame.draw.circle(background, x.color,(int(x.x+0.5),int(x.y+0.5)), int(x.radius+0.5))
    if x.name == "wall":
        pygame.draw.line(background, x.color, (int(x.x+0.5),int(x.y+0.5)),(int(x.x2+0.5),int(x.y2+0.5)), int(x.width+0.5))
    return True

def getPixelBackground(objects, window):
    pixelArray = [[0 for x in range(window.width)] for x in range(window.height)]
    for x in objects:
        if x.name == "car":
            continue
        if x.name == "cone":
            pixels = circlePixelArray(int(x.x+0.5),int(x.y+0.5),x.radius)
        if x.name == "wall":
            pixels = linePixelArray(int(x.x+0.5),int(x.y+0.5),int(x.x2+0.5),int(x.y2+0.5))
        for x in pixels:
            pixelArray[x[1]][x[0]] = 200
        
def circlePixelArray(x,y,r):
    radiusSquared = r*r
    pixels = []
    for xc in range(x-r, x+r+1):
        for yc in range(y-r, y+r+1):
            if (x-xc)*(x-xc)+(y-yc)*(y-yc) <= radiusSquared:
                pixels.append((x,y,))
    return pixels
                

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
        pixels.append((x,y,))
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
            
    
def update(objects, FPS, choices):
    car = objects[0]
    for x in objects:
        if x.name == "car":
            car.update(choices, FPS)
            continue
        if x.name == "cone":
            collision = physics.carCircle(car, x)
        if x.name == "wall":
            collision = physics.carLine(car, (x.x,x.y,x.x2,x.y2))
        if collision:
            x.color = (0,0,0)
        else:
            x.color = (255, 0, 0)
        

def checkEvents(pygame, objects, choices):
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN:
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
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                choices[1]=0
            if event.key == pygame.K_RIGHT:
                choices[1]= 0
            if event.key == pygame.K_UP:
                choices[0]=0
            if event.key == pygame.K_DOWN:
                choices[0]=0
            

def init(pygame, window):
    pygame.init()
    screen = pygame.display.set_mode((window.width, window.height))
    pygame.display.set_caption(window.name)
    pygame.mouse.set_visible(1)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(window.color)
    return screen, background



def run(pygame, screen, background, objects, game_loop, window, pixelBackground):
    clock = pygame.time.Clock()
    choices = [0,0]
    while game_loop.run == True:
        render(pygame, screen, background, objects, window)
        update(objects, game_loop.FPS, choices)
        action = checkEvents(pygame, objects, choices)
        if action == "quit":
            return 1
        clock.tick(game_loop.FPS)