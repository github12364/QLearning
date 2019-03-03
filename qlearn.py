from keras.models import Sequential
from keras.layers import Dense, Flatten
from collection import deque
import numpy as numpy

import random

model = Sequential()
model.add(Dense(32, input_shape=(2,)))
model.add(Flatten())
model.add()