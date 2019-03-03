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
    return background

def render(pygame, screen, background, objects, window):
    background.fill(window.color)
    for x in objects:
        addObject(pygame, background, x)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
def update(objects, FPS):
    car = objects[0]
    for x in objects:
        if x.name == "car":
            continue
        if x.name == "cone":
            continue
        if x.name == "wall":
            collision = physics.carLine(car, (x.x,x.y,x.x2,x.y2))
            if collision:
                x.color = (0,0,0)
            else:
                x.color = (255, 0, 0)
            
        

def checkEvents(pygame, objects):
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"
            if event.key == pygame.K_LEFT:
                objects[0].turn("left")
            if event.key == pygame.K_RIGHT:
                objects[0].turn("right")
            if event.key == pygame.K_UP:
                objects[0].accelerate()
            if event.key == pygame.K_DOWN:
                objects[0].decelerate()
            

def init(pygame, window):
    pygame.init()
    screen = pygame.display.set_mode((window.width, window.height))
    pygame.display.set_caption(window.name)
    pygame.mouse.set_visible(1)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(window.color)
    return screen, background

def run(pygame, screen, background, objects, game_loop, window):
    clock = pygame.time.Clock()
    while game_loop.run == True:
        update(objects, game_loop.FPS)
        render(pygame, screen, background, objects, window)
        action = checkEvents(pygame, objects)
        if action == "quit":
            return 1
        