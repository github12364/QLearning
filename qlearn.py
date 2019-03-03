import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from collections import deque


import random

class QLearn:
    
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(16, input_shape=(2,) + (int(1080/30),int(720/30)), init='uniform', activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(16, init='uniform', activation='relu'))
        self.model.add(Dense(16, init='uniform', activation='relu'))
        self.model.add(Dense(9, init='uniform', activation='linear'))
        self.model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])


        self.D = deque()
        self.tempD = []

        self.observetime=2000

        self.epsilon = 0.7
        self.gamma = 0.9
        self.mb_size = 50
        
        
    def observe(self, p_pixelArray, pixelArray, status):
        obs = np.expand_dims(rotateDim(np.array(p_pixelArray)), axis=0)
        #print (np.array(p_pixelArray).shape)
        print (obs.shape)
        obs2 = np.expand_dims(rotateDim(np.array(pixelArray)), axis=0)
        #print (np.array(pixelArray).shape)
        print (obs2.shape)
        state = np.stack((obs, obs2), axis=1)
        print (state.shape)
        if np.random.rand() <= self.epsilon:
            return self.chooseRandomAction(pixelArray, status)
        else:
            Q = self.model.predict(state, batch_size=1)
            print (np.argmax(Q))
            action = np.argmax(Q)
            self.tempD.append(state)
            self.tempD.append(action)
            return action
        
    #def learn(self)
         
    def chooseRandomAction(self, pixelArray, status):
        return np.random.randint(0,8, size=1)[0]
    
    def updateAction(self, reward, done):
        self.tempD.append(reward)
        self.tempD.append(done)
        
    
def rotateDim(array):
    newArray = np.zeros((array.shape[1], array.shape[0]))
    #print (newArray)
    for x in range(0,len(array)):
        for y in range(0,len(array[x])):
            temp = array[x][y]
            newArray[y][x] = temp
    return newArray
        
        