import pygame
import objects
import engine
import qlearn
import os, sys
import random
import numpy as np
from pygame.locals import *


class game_loop:
    run = True
    FPS = 120
    mode= "drawing"

observeTime = 75
counter = 0
ql = qlearn.QLearn()
while (game_loop.run):
    if counter < observeTime:
        objectList = [
            objects.Car(500, 300, (0,255,0), "car"), 
            objects.Cone(800, 325, 50, (255,0,0)), 
            objects.Cone(700, 200, 50, (255,0,0),),
            objects.Wall(900, 300, 900, 700, 50, (255,0,0)), 
            objects.Wall(500, 000, 200, 700, 50, (255,0,0)), 
            objects.Wall(700, 500, 400, 800, 50, (255,0,0)),
            objects.Wall(700, 500, 400, 800, 50, (255,0,0)),
            objects.Goal(650, 300, 25, (0, 255, 255)),
            objects.Goal(700, 375, 25, (0, 255, 255)),
            objects.Goal(750, 475 , 25, (0, 255, 255)),
            objects.Goal(725, 650, 25, (0, 255, 255)),
            ]
    
    
        window = objects.Map(1080,720, "test", (255,255,255))
        screen, background = engine.init(pygame, window)
        engine.renderfirst(pygame, screen, background, objectList, window)
        pixelBackground = engine.compressPixelArray(engine.getPixelBackground(objectList, background, window), 30)
        print ("TRY")
        engine.run(pygame, screen, background, objectList, game_loop, window, pixelBackground, ql)
        print("DONE")
        counter += 1
        
    
    else:  
        print(ql.D, ql.mb_size)
        minibatch = random.sample(ql.D, ql.mb_size)    
        inputs_shape = (ql.mb_size,) + (1,2,36,24)[1:]
        inputs = np.zeros(inputs_shape)
        targets = np.zeros((ql.mb_size, 9))
    
        for i in range(0, ql.mb_size):
            state = minibatch[i][0]
            action = minibatch[i][1]
            reward = minibatch[i][2]
            state_new = minibatch[i][3]
            done = minibatch[i][4]
            
        # Build Bellman equation for the Q function
            inputs[i:i+1] = np.expand_dims(state, axis=0)
            targets[i] = ql.model.predict(state)
            Q_sa = ql.model.predict(state_new)
            
            if done:
                targets[i, action] = reward
            else:
                targets[i, action] = reward + ql.gamma * np.max(Q_sa)
        
        # Train network to output the Q function
            model.train_on_batch(inputs, targets)
        print('Learning Finished')