import numpy as np
from keras.model import Sequential
from keras.layers import Conv2D

class Model:
    def __init__(self):
        return

    def train(self):
        model = Sequential()
        model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(28,28,1)))
        model.add(Conv2D(64, kernel_size=3, activation='relu'))
        model.add(Conv2D(64, kernel_size=3, activation='relu'))
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])