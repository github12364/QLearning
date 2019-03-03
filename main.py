import pygame
import objects
import engine
import os, sys
from pygame.locals import *

objects = []
class temp_window:
    width = 1080
    height = 720
    name = "test"

class game_loop:
    run = True
    FPS = 60

screen, background = engine.init(pygame, temp_window)
engine.run(pygame, screen, background, objects, game_loop)
