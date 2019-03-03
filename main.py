import pygame
import objects
import engine
import os, sys
from pygame.locals import *

objectList = [objects.Car(0,0,0,0), objects.Obstructions(100, 100, "cone"), objects.Obstructions(200, 100, "cone")]
window = objects.Map(1080,720, "test", (255,255,0))

class game_loop:
    run = True
    FPS = 60

screen, background = engine.init(pygame, window)
engine.run(pygame, screen, background, objectList, game_loop)