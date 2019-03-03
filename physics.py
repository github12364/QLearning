# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 17:49:20 2019

@author: Henry
"""

def lineLine(line1, line2):
    x1 = float(line1[0])
    y1 = float(line1[1])
    x2 = float(line1[2])
    y2 = float(line1[3]) 
    x3 = line2[0]
    y3 = line2[1]
    x4 = line2[2]
    y4 = line2[3]   
    
    try:
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    except ZeroDivisionError:
        return False
    return (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1)
    
def carLine(car, line):
    verticies = car.getVerticies()
    line1 = verticies[0]+verticies[1]
    line2 = verticies[1]+verticies[2]
    line3 = verticies[2]+verticies[3]
    line4 = verticies[3]+verticies[0]
    return (lineLine(line1, line) or lineLine(line2, line) or lineLine(line3, line) or lineLine(line4, line))