import pygame
import objects
import engine
import os, sys
from pygame.locals import *

objectList = [
        objects.Car(500, 300, (0,255,0), "car"), 
        objects.Cone(100, 100, 20, (255,0,0)), 
        objects.Cone(100, 200, 20, (255,0,0),),
        objects.Wall(300, 300, 300, 200, 5, (255,0,0)), 
        objects.Wall(700, 500, 400, 800, 5, (255,0,0)),
        ]
window = objects.Map(1080,720, "test", (255,255,0))
pixelArray = []

class game_loop:
    run = True
    FPS = 60
    mode= "drawing"

screen, background = engine.init(pygame, window)
engine.run(pygame, screen, background, objectList, game_loop, window, pixelArray)