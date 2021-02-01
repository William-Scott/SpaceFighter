import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

class StateManager():
    def __init__(self):
        self.state = {'ready': False, 'start':True, 'run':False, 'pause':False, 'over':False, 'win':False, 'end':False}
    def changestate(self, state_from, state_to):
        if state_from == "all":
            for key in list(self.state.keys()):
                self.state[key] = False
            self.state[state_to] = True
        else:
            self.state[state_from] = False
            self.state[state_to] = True