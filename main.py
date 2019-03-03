import pygame
import objects
import engine
import os, sys
from pygame.locals import *


class game_loop:
    run = True
    FPS = 120
    mode= "drawing"


while (game_loop.run):
    objectList = [
        objects.Car(500, 300, (0,255,0), "car"), 
        objects.Cone(100, 100, 20, (255,0,0)), 
        objects.Cone(100, 200, 20, (255,0,0),),
        objects.Wall(300, 300, 300, 200, 5, (255,0,0)), 
        objects.Wall(700, 500, 400, 800, 5, (255,0,0)),
        objects.Goal(750, 650, 20, (0, 255, 0))
        ]


    window = objects.Map(1080,720, "test", (255,255,0))
    pixelBackground = engine.getPixelBackground(objectList, window)
    
    screen, background = engine.init(pygame, window)
    print ("TRY")
    engine.run(pygame, screen, background, objectList, game_loop, window, pixelBackground)