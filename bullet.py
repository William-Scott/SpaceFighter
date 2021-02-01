import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

from respath import resource_path

class Bullet(pygame.sprite.Sprite):
    def __init__(self, posx, posy, speed, direction=0):
        super(Bullet,self).__init__()
        self.surf_bullet_image = pygame.image.load(resource_path("res\\bullet.png")).convert_alpha()
        self.surf_hit_image = pygame.image.load(resource_path("res\\hit.png")).convert_alpha()
        self.surf_bullet_1a = pygame.transform.scale(self.surf_bullet_image.subsurface((0,0),(18,6)), (90,30))
        self.surf_bullet_1b = pygame.transform.scale(self.surf_bullet_image.subsurface((20,0),(18,6)), (90,30))
        self.surf_bullet_2a = pygame.transform.scale(self.surf_bullet_image.subsurface((40,0),(18,6)), (90,30))
        self.surf_bullet_2b = pygame.transform.scale(self.surf_bullet_image.subsurface((60,0),(18,6)), (90,30))
        self.surf_bullet_3a = pygame.transform.scale(self.surf_bullet_image.subsurface((0,7),(20,8)), (100,40))
        self.surf_hit_a = pygame.transform.scale(self.surf_hit_image.subsurface((4,4),(8,8)), (40,40))
        self.surf_hit_b = pygame.transform.scale(self.surf_hit_image.subsurface((17,1),(14,14)), (70,70))
        self.surf_hit_c = pygame.transform.scale(self.surf_hit_image.subsurface((33,1),(14,14)), (70,70))
        self.surf_hit_d = pygame.transform.scale(self.surf_hit_image.subsurface((49,1),(14,14)), (70,70))
        self.image = self.surf_bullet_1a
        self.rect = self.image.get_rect(center=(posx, posy))
        self.mask = pygame.mask.from_surface(self.image)
        self.cdb = 0
        self.cdh = 0
        self.islive = True
        self.w, self.h = self.image.get_size()
        self.posx = self.rect[0] + self.w/2
        self.posy = self.rect[1] + self.h/2
        v = pygame.Vector2()
        v.xy = 0,1
        v.rotate_ip(direction)
        v = v*speed
        self.speed_x = v.x
        self.speed_y = -v.y
        self.direction = direction + 90
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

class Bullet_p(Bullet):
    def update(self, screen, body=0):
        if self.islive:
            if self.cdb < 5:
                self.image = self.surf_bullet_1a
                screen.blit(self.image, self.rect)
                self.cdb += 1
            elif self.cdb >= 5 and self.cdb < 9:
                self.image = self.surf_bullet_1b
                screen.blit(self.image, self.rect)
                self.cdb += 1
            elif self.cdb == 9:
                self.image = self.surf_bullet_1b
                screen.blit(self.image, self.rect)
                self.cdb = 0
            self.rect.move_ip(self.speed_x, self.speed_y)
            if self.rect.left > 1360:
                self.kill()
        else:
            if self.cdh < 5:
                screen.blit(self.surf_hit_a, (self.rect[0]+30,self.rect[1]+15))
                self.cdh += 1
            elif self.cdh >= 5 and self.cdh < 10:
                screen.blit(self.surf_hit_b, (self.rect[0]+40,self.rect[1]))
                self.cdh += 1
            elif self.cdh >= 10 and self.cdh < 15:
                screen.blit(self.surf_hit_c, (self.rect[0]+40,self.rect[1]))
                self.cdh += 1
            elif self.cdh >= 15 and self.cdh < 19:
                screen.blit(self.surf_hit_d, (self.rect[0]+40,self.rect[1]))
                self.cdh += 1
            elif self.cdh == 19:
                screen.blit(self.surf_hit_d, (self.rect[0]+40,self.rect[1]))
                self.cdh += 1
                self.kill()

class Bullet_e1(Bullet):
    def update(self, screen, body=0):
        if self.islive:
            if self.cdb < 5:
                self.image = self.surf_bullet_2a
                screen.blit(self.image, self.rect)
                self.cdb += 1
            elif self.cdb >= 5 and self.cdb < 9:
                self.image = self.surf_bullet_2b
                screen.blit(self.image, self.rect)
                self.cdb += 1
            elif self.cdb == 9:
                self.image = self.surf_bullet_2b
                screen.blit(self.image, self.rect)
                self.cdb = 0
            self.rect.move_ip(self.speed_x, self.speed_y)
            if self.rect.right < 0:
                self.kill()
        else:
            self.kill()

class Bullet_e2(Bullet):
    def __init__(self, posx, posy, speed, direction=0 ):
        super(Bullet_e2, self).__init__(posx, posy, speed, direction)
        self.mask = pygame.mask.from_surface(self.surf_bullet_3a)
    def update(self, screen, body=0):
        super(Bullet_e2, self).update(screen)
        if self.islive:
            if self.cdb < 5:
                self.image = self.surf_bullet_3a
                self.blitRotate(screen, self.image, (self.posx, self.posy), (self.w/2, self.h/2), self.direction)
                self.cdb += 1
            elif self.cdb >= 5 and self.cdb < 9:
                self.image = self.surf_bullet_3a
                self.blitRotate(screen, self.image, (self.posx, self.posy), (self.w/2, self.h/2), self.direction)
                self.cdb += 1
            elif self.cdb == 9:
                self.image = self.surf_bullet_3a
                self.blitRotate(screen, self.image, (self.posx, self.posy), (self.w/2, self.h/2), self.direction)
                self.cdb = 0
            self.rect.move_ip(self.speed_x, self.speed_y)
            self.posx = self.rect[0] + self.w/2
            self.posy = self.rect[1] + self.h/2
            if self.rect.right < 0 or self.rect.bottom < 0 or self.rect.top > 1360:
                self.kill()
            if body.islive == False:
                self.kill()
        else:
            self.kill()