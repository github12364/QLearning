from keras.models import Sequential
from keras.layers import Dense, Flatten
from collection import deque
import numpy as np

import random

class QLearn:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(16, input_shape=(2,) + (1080,720), init='uniform', activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(16, init='uniform', activation='relu'))
        self.model.add(Dense(16, init='uniform', activation='relu'))
        self.model.add(Dense(9, init='uniform', activation='linear'))
        self.model.compile(loss='mse', optimizer='adam', metrics={'accuracy'})

        self.D = deque()

        self.observetime=2000

        self.epsilon = 0.7
        self.gamma = 0.9
        self.mb_size = 50

    def chooseAction(self, pixelArray):
        return (np.random.randint(0, 2, size=1)[0], np.random.randint(0,2, size=1)[0])
        # if np.random.rand() <= self.epsilon:
        #     action = np.random.randint(0, 9, size=1)[0]
        # else:
        #     Q = model.predict(state)