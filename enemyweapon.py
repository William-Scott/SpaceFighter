import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

from respath import resource_path

class EnemyWeapon(pygame.sprite.Sprite):
    def __init__(self, default):
        super(EnemyWeapon, self).__init__()
        self.surf_enemyweapon_image = pygame.image.load(resource_path("res\\boss1weapon.png")).convert_alpha()
        self.surf_enemyweapon_1a = pygame.transform.scale(self.surf_enemyweapon_image.subsurface((0,0),(20,10)), (100,50))
        self.image = self.surf_enemyweapon_1a
        #self.rect = self.image.get_rect(center=(posx, posy))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_r = 1
        self.islive = True
        self.timepass = default
        self.w, self.h = self.image.get_size()
    def blitRotate(self, surf, image, pos, originPos, angle):
        #calcaulate the axis aligned bounding box of the rotated image
        w, h = image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        #calculate the translation of the pivot 
        pivot = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot
        #calculate the upper left origin of the rotated image
        origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])
        #get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        #rotate and blit the image
        surf.blit(rotated_image, origin)
        #draw rectangle around the image
        #pygame.draw.rect (surf, (255, 0, 0), (*origin, *rotated_image.get_size()),2)

class Boss1Weapon(EnemyWeapon):
    def update(self, screen, posx, posy, direction_r):
        if self.islive:
            if direction_r == 1:
                self.blitRotate(screen, self.image, (posx + self.w*3/4, posy+202 - self.h/2), (self.w*3/4, self.h/2), self.speed_r*self.timepass)
                self.timepass += 1
            if direction_r == -1:
                self.blitRotate(screen, self.image, (posx + self.w*3/4, posy+202 - self.h/2), (self.w*3/4, self.h/2), self.speed_r*self.timepass)
                self.timepass -= 1
        else:
            self.kill()