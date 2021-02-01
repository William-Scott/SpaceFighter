import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

from respath import resource_path

class Number(pygame.sprite.Sprite):
    def __init__(self):
        super(Number,self).__init__()
        self.surf_font_image = pygame.image.load(resource_path("res\\font.png")).convert_alpha()
        self.surf_num_0 = pygame.transform.scale(self.surf_font_image.subsurface((120,36),(12,15)), (60,75))
        self.surf_num_1 = pygame.transform.scale(self.surf_font_image.subsurface((0,54),(12,15)), (60,75))
        self.surf_num_2 = pygame.transform.scale(self.surf_font_image.subsurface((15,54),(12,15)), (60,75))
        self.surf_num_3 = pygame.transform.scale(self.surf_font_image.subsurface((30,54),(12,15)), (60,75))
        self.surf_num_4 = pygame.transform.scale(self.surf_font_image.subsurface((45,54),(12,15)), (60,75))
        self.surf_num_5 = pygame.transform.scale(self.surf_font_image.subsurface((60,54),(12,15)), (60,75))
        self.surf_num_6 = pygame.transform.scale(self.surf_font_image.subsurface((75,54),(12,15)), (60,75))
        self.surf_num_7 = pygame.transform.scale(self.surf_font_image.subsurface((90,54),(12,15)), (60,75))
        self.surf_num_8 = pygame.transform.scale(self.surf_font_image.subsurface((105,54),(12,15)), (60,75))
        self.surf_num_9 = pygame.transform.scale(self.surf_font_image.subsurface((120,54),(12,15)), (60,75))
        self.nums_dict = {
                    '0':self.surf_num_0, '1':self.surf_num_1, '2':self.surf_num_2,
                    '3':self.surf_num_3, '4':self.surf_num_4, '5':self.surf_num_5,
                    '6':self.surf_num_6, '7':self.surf_num_7, '8':self.surf_num_8,
                    '9':self.surf_num_9
                    }
        self.image = self.surf_num_0
    def update(self, screen, pos, num):
        self.image = self.nums_dict[num]
        screen.blit(self.image, pos)

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score,self).__init__()
        self.surf_font_image = pygame.image.load(resource_path("res\\font.png")).convert_alpha()
        self.surf_score = pygame.transform.scale(self.surf_font_image.subsurface((60,18),(72,15)), (360,75))
        self.image = self.surf_score
    def update(self, screen, pos):
        screen.blit(self.image, pos)

class ScoreManager():
    def __init__(self):
        self.score = 0
        self.score_add = 10
        self.score_UI = Score()
    def setscore_add(self, sa):
        self.score_add = sa
    def score_up(self, add):
        self.score += add
    def update(self, screen):
        self.score_UI.update(screen,(50,700))
        pos = 0
        for num in str(self.score):
            n = Number()
            n.update(screen, (500+pos*70, 700), num)
            pos += 1