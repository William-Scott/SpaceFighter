import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

from respath import resource_path

class Button(pygame.sprite.Sprite):
    def __init__(self):
        super(Button,self).__init__()
        self.surf_font_image = pygame.image.load(resource_path("res\\font.png")).convert_alpha()
        self.surf_start_a = pygame.transform.scale(self.surf_font_image.subsurface((0,0),(72,15)), (360,75))
        self.surf_start_b = pygame.transform.scale(self.surf_font_image.subsurface((0,72),(95,20)), (475,100))
        self.surf_quit_a = pygame.transform.scale(self.surf_font_image.subsurface((75,0),(57,15)), (285,75))
        self.surf_quit_b = pygame.transform.scale(self.surf_font_image.subsurface((99,72),(76,20)), (380,100))
        self.surf_con_a = pygame.transform.scale(self.surf_font_image.subsurface((0,36),(117,15)), (585,75))
        self.surf_con_b = pygame.transform.scale(self.surf_font_image.subsurface((0,96),(156,20)), (780,100))
        self.image = self.surf_start_a
        self.rect = self.image.get_rect(center=(680,400))
        self.beclick = False

class BtStart(Button):
    def update(self, screen, pos, click, sc):
        if self.rect.collidepoint(pos):
            self.image = self.surf_start_b
            self.rect = self.image.get_rect(center=(680,350))
            if click[0] and self.beclick == False:
                self.beclick = True
            elif click[0] == False and self.beclick:
                sc('start', 'run')
                self.beclick = False
        else:
            self.beclick = False
            self.image = self.surf_start_a
            self.rect = self.image.get_rect(center=(680,350))
        screen.blit(self.image, self.rect)

class BtQuit(Button):
    def update(self, screen, pos, click, sc):
        if self.rect.collidepoint(pos):
            self.image = self.surf_quit_b
            self.rect = self.image.get_rect(center=(680,550))
            if click[0] and self.beclick == False:
                self.beclick = True
            elif click[0] == False and self.beclick:
                sc('all', 'end')
                self.beclick = False
        else:
            self.beclick = False
            self.image = self.surf_quit_a
            self.rect = self.image.get_rect(center=(680,550))
        screen.blit(self.image, self.rect)

class BtCon(Button):
    def update(self, screen, pos, click, sc):
        if self.rect.collidepoint(pos):
            self.image = self.surf_con_b
            self.rect = self.image.get_rect(center=(680,350))
            if click[0] and self.beclick == False:
                self.beclick = True
            elif click[0] == False and self.beclick:
                sc('pause', 'run')
                self.beclick = False
        else:
            self.beclick = False
            self.image = self.surf_con_a
            self.rect = self.image.get_rect(center=(680,350))
        screen.blit(self.image, self.rect)

class BtReStart(Button):
    def update(self, screen, pos, click, sc):
        if self.rect.collidepoint(pos):
            self.image = self.surf_con_b
            self.rect = self.image.get_rect(center=(680,350))
            if click[0] and self.beclick == False:
                self.beclick = True
            elif click[0] == False and self.beclick:
                sc('over', 'ready')
                self.beclick = False
        else:
            self.beclick = False
            self.image = self.surf_con_a
            self.rect = self.image.get_rect(center=(680,350))
        screen.blit(self.image, self.rect)

class Over(pygame.sprite.Sprite):
    def __init__(self):
        super(Over,self).__init__()
        self.surf_font_image = pygame.image.load(resource_path("res\\font.png")).convert_alpha()
        self.surf_over = pygame.transform.scale(self.surf_font_image.subsurface((0,120),(164,20)), (820,100))
        self.image = self.surf_over
        self.rect = self.image.get_rect(center=(680,550))
    def update(self, screen):
        screen.blit(self.image, self.rect)

class Win(pygame.sprite.Sprite):
    def __init__(self):
        super(Win,self).__init__()
        self.surf_font_image = pygame.image.load(resource_path("res\\font.png")).convert_alpha()
        self.surf_win = pygame.transform.scale(self.surf_font_image.subsurface((0,144),(145,25)), (820,125))
        self.image = self.surf_win
        self.rect = self.image.get_rect(center=(680,350))
    def update(self, screen):
        screen.blit(self.image, self.rect)