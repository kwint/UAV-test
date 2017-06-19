# Read data
import numpy as np

global flag
global move

def process():

    flag = 1
    move = 0
    while True:
        if flag == 1:
            move += 10
            print("edit move")
            flag = 2