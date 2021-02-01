import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

class Shock():
    def __init__(self):
        self.t = 60
        self.A = 0
        self.Lambda = 0.15
        self.Phi = 0
        self.Omega = 0
    def setshock(self, A, Omega, Phi):
        self.t = 0
        self.A = A
        self.Omega = Omega
        self.Phi = Phi
    def update(self, display, screen):
        if self.t == 60:
            display.blit(screen, (-5,-5))
        else:
            if self.t < 60:
                self.t += 1
            fx = round(float(self.A*np.power(2.72,(-self.Lambda*self.t))*np.cos(self.Omega*self.t+self.Phi)),2)
            fy = round(float(self.A*np.power(2.72,(-self.Lambda*self.t))*np.cos(self.Omega*self.t+self.Phi+3.14)),2)
            display.blit(screen, (-5+fx,-5+fy))