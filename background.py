import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

from respath import resource_path

class BackgroundBack(pygame.sprite.Sprite):
    def __init__(self, posx):
        super(BackgroundBack,self).__init__()
        self.surf_bgb_image = pygame.image.load(resource_path("res\\bg-back.png")).convert()
        self.surf_bgb = pygame.transform.scale(self.surf_bgb_image, (1360,800))
        self.rect_bgb = self.surf_bgb.get_rect(topleft=(posx, 0))
        self.speed_bgb = 3
    def update(self, screen):
        screen.blit(self.surf_bgb, self.rect_bgb)
        self.rect_bgb.move_ip(-self.speed_bgb, 0)
        if self.rect_bgb.right < 0:
            self.kill()

class BackgroundPlanet(pygame.sprite.Sprite):
    def __init__(self, posx):
        super(BackgroundPlanet,self).__init__()
        self.surf_bgp_image = pygame.image.load(resource_path("res\\bg-planet.png")).convert_alpha()
        self.rotate = 180 * random.randint(0,1)
        self.surf_bgp = pygame.transform.scale(pygame.transform.rotate(self.surf_bgp_image, self.rotate), (1360,800))
        self.rect_bgp = self.surf_bgp.get_rect(topleft=(posx+random.randint(200, 300), 0))
        self.speed_bgp = 5
    def update(self, screen):
        screen.blit(self.surf_bgp, self.rect_bgp)
        self.rect_bgp.move_ip(-self.speed_bgp, 0)
        if self.rect_bgp.right < 0:
            self.kill()

class BackgroundStar(pygame.sprite.Sprite):
    def __init__(self, posx):
        super(BackgroundStar,self).__init__()
        self.surf_bgs_image = pygame.image.load(resource_path("res\\bg-stars.png")).convert_alpha()
        self.surf_bgs = pygame.transform.scale(self.surf_bgs_image, (1360,800))
        self.rect_bgs = self.surf_bgs.get_rect(topleft=(posx+random.randint(0, 10), 0))
        self.speed_bgs = 3
    def update(self, screen):
        screen.blit(self.surf_bgs, self.rect_bgs)
        self.rect_bgs.move_ip(-self.speed_bgs, 0)
        if self.rect_bgs.right < 0:
            self.kill()

class BackGroundManager():
    def __init__(self):
        self.surf_bgbs = pygame.sprite.Group()
        self.surf_bgps = pygame.sprite.Group()
        self.surf_bgss = pygame.sprite.Group()
        surf_bgb = BackgroundBack(0)
        self.surf_bgbs.add(surf_bgb)
        surf_bgs = BackgroundStar(0)
        self.surf_bgss.add(surf_bgs)
        surf_bgp = BackgroundPlanet(0)
        self.surf_bgps.add(surf_bgp)
    def update(self, screen):
        if len(self.surf_bgbs) < 2:
            surf_bgb = BackgroundBack(1361)
            self.surf_bgbs.add(surf_bgb)
        self.surf_bgbs.update(screen)
        if len(self.surf_bgss) < 2:
            surf_bgs = BackgroundStar(1361)
            self.surf_bgss.add(surf_bgs)
        self.surf_bgss.update(screen)
        if len(self.surf_bgps) < 2:
            surf_bgp = BackgroundPlanet(1361)
            self.surf_bgps.add(surf_bgp)
        self.surf_bgps.update(screen)