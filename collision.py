import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

from respath import resource_path

class CollisionDetection():
    def __init__(self, bullet_ps, bullet_es, enemys, asteroids, players):
        self.hit = pygame.mixer.Sound("res\\hit.ogg")
        self.explosion = pygame.mixer.Sound("res\\explosion.ogg")
        self.bullet_ps = bullet_ps
        self.bullet_es = bullet_es
        self.enemys = enemys
        self.asteroids = asteroids
        self.players = players
    def update(self, screen, ss, su):
        for entity1 in self.bullet_ps:
            for entity2 in self.enemys:
                if entity1 and entity2:
                    if pygame.sprite.collide_mask(entity1, entity2):
                        ss(10,6.28,0)
                        #pygame.draw.rect (screen, (255, 0, 0), entity1.rect, 5)
                        #pygame.draw.rect (screen, (255, 0, 0), entity2.rect, 5)
                        self.bullet_ps.remove(entity1)
                        entity1.islive = False
                        channel = self.hit.play()
                        if entity2.health:
                            entity2.health -= 1
                        else:
                            su(100)
                            self.enemys.remove(entity2)
                            entity2.islive = False
                            channel = self.explosion.play()
        for entity1 in self.bullet_ps:
            for entity3 in self.asteroids:
                if entity1 and entity3:
                    if pygame.sprite.collide_mask(entity1, entity3):
                        ss(10,6.28,0)
                        su(50)
                        #pygame.draw.rect (screen, (255, 0, 0), entity1.rect, 5)
                        #pygame.draw.rect (screen, (255, 0, 0), entity3.rect, 5)
                        self.bullet_ps.remove(entity1)
                        entity1.islive = False
                        channel = self.hit.play()
                        self.asteroids.remove(entity3)
                        entity3.islive = False
                        channel = self.explosion.play()
        for entity4 in self.players:
            for entity5 in self.bullet_es:
                if entity4 and entity5:
                    if pygame.sprite.collide_mask(entity4, entity5):
                        if entity4.god == False:
                            ss(10,6.28,0)
                            #pygame.draw.rect (screen, (255, 0, 0), entity4.rect, 5)
                            self.players.remove(entity4)
                            entity4.islive = False
                            self.bullet_es.remove(entity5)
                            entity5.islive = False
                            channel = self.explosion.play()
        for entity4 in self.players:
            for entity3 in self.asteroids:
                if entity4 and entity3:
                    if pygame.sprite.collide_mask(entity4, entity3):
                        if entity4.god == False:
                            ss(10,6.28,0)
                            #pygame.draw.rect (screen, (255, 0, 0), entity4.rect, 5)
                            self.players.remove(entity4)
                            entity4.islive = False
                            self.asteroids.remove(entity3)
                            entity3.islive = False
                            channel = self.explosion.play()
        for entity4 in self.players:
            for entity2 in self.enemys:
                if entity4 and entity2:
                    if pygame.sprite.collide_mask(entity4, entity2):
                        if entity4.god == False:
                            ss(10,6.28,0)
                            #pygame.draw.rect (screen, (255, 0, 0), entity4.rect, 5)
                            self.players.remove(entity4)
                            entity4.islive = False
                            self.enemys.remove(entity2)
                            entity2.islive = False
                            channel = self.explosion.play()