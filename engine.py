# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:13:25 2019

@author: Henry
"""


def addObject(pygame, background, x):
    if x.name == "car":
        return
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
    pass

def checkEvents(pygame):
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            return "quit"

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
        action = checkEvents(pygame)
        if action == "quit":
            return 1
        clock.tick(game_loop.FPS)
