import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

from respath import resource_path

class AsteroidSmall(pygame.sprite.Sprite):
    def __init__(self, pos, speed_p, speed_r, direction):
        super(AsteroidSmall,self).__init__()
        self.surf_asteroidsmall_image = pygame.image.load(resource_path("res\\asteroid-small.png")).convert_alpha()
        self.surf_asteroidsmall = pygame.transform.scale(self.surf_asteroidsmall_image.subsurface((1,0),(13,13)), (65,65))
        self.image = self.surf_asteroidsmall
        self.rect = self.image.get_rect(center=(pos[0], pos[1]))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_r = speed_r
        self.islive = True
        self.timepass = 0
        self.w, self.h = self.image.get_size()
        self.posx = self.rect[0] + self.w/2
        self.posy = self.rect[1] + self.h/2
        v = pygame.Vector2()
        v.xy = 0,1
        v.rotate_ip(direction)
        v = v*speed_p
        self.speed_x = v.x
        self.speed_y = -v.y
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
    def update(self, screen):
        if self.islive:
            self.blitRotate(screen, self.image, (self.posx, self.posy), (self.w/2, self.h/2), self.speed_r*self.timepass)
            self.rect.move_ip(self.speed_x, self.speed_y)
            self.posx = self.rect[0] + self.w/2
            self.posy = self.rect[1] + self.h/2
            self.timepass += 1
            if self.rect.left > 1360 or self.rect.right < 0 or self.rect.top > 800 or self.rect.bottom < 0:
                self.islive = False
                self.kill()
        else:
            self.kill()

class Asteroid(AsteroidSmall):
    def __init__(self, pos, speed_p, speed_r, direction):
        super(Asteroid,self).__init__(pos, speed_p, speed_r, direction)
        self.asteroidsmalls = pygame.sprite.Group()
        self.surf_asteroid_image = pygame.image.load(resource_path("res\\asteroid.png")).convert_alpha()
        self.surf_explosion_image = pygame.image.load(resource_path("res\\explosion.png")).convert_alpha()
        self.surf_asteroid = pygame.transform.scale(self.surf_asteroid_image.subsurface((1,1),(33,35)), (165,175))
        self.surf_explosion_a = pygame.transform.scale(self.surf_explosion_image.subsurface((11,11),(10,10)), (50,50))
        self.surf_explosion_b = pygame.transform.scale(self.surf_explosion_image.subsurface((36,6),(24,22)), (120,110))
        self.surf_explosion_c = pygame.transform.scale(self.surf_explosion_image.subsurface((66,5),(28,24)), (140,120))
        self.surf_explosion_d = pygame.transform.scale(self.surf_explosion_image.subsurface((98,4),(28,26)), (140,130))
        self.surf_explosion_e = pygame.transform.scale(self.surf_explosion_image.subsurface((130,3),(28,27)), (140,135))
        self.image = self.surf_asteroid
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_r = speed_r
        self.islive = True
        self.timepass = 0
        self.w, self.h = self.surf_asteroid.get_size()
        self.posx = self.rect[0] + self.w/2
        self.posy = self.rect[1] + self.h/2
        v = pygame.Vector2()
        v.xy = 0,1
        v.rotate_ip(direction)
        v = v*speed_p
        self.speed_x = v.x
        self.speed_y = -v.y
        self.hascreate = False
        self.cdex = 0
    def update(self, screen, group):
        if self.islive:
            self.blitRotate(screen, self.image, (self.posx, self.posy), (self.w/2, self.h/2), self.speed_r*self.timepass)
            self.rect.move_ip(self.speed_x, self.speed_y)
            self.posx = self.rect[0] + self.w/2
            self.posy = self.rect[1] + self.h/2
            self.timepass += 1
            if self.rect.left > 1560 or self.rect.right < -200 or self.rect.top > 1000 or self.rect.bottom < -200:
                self.kill()
        else :
            if self.cdex < 5:
                screen.blit(self.surf_explosion_a, (self.rect[0]+35,self.rect[1]+40))
                self.cdex += 1
            elif self.cdex >= 5 and self.cdex < 10:
                screen.blit(self.surf_explosion_b, (self.rect[0],self.rect[1]-5))
                self.cdex += 1
            elif self.cdex >= 10 and self.cdex < 15:
                screen.blit(self.surf_explosion_c, (self.rect[0],self.rect[1]))
                self.cdex += 1
            elif self.cdex >= 15 and self.cdex < 20:
                screen.blit(self.surf_explosion_d, (self.rect[0],self.rect[1]))
                self.cdex += 1
            elif self.cdex >= 20 and self.cdex < 24:
                screen.blit(self.surf_explosion_e, (self.rect[0],self.rect[1]))
                self.cdex += 1
            elif self.cdex == 24:
                screen.blit(self.surf_explosion_e, (self.rect[0],self.rect[1]))
                self.cdex += 1
            if self.hascreate:
                if self.asteroidsmall1.islive or self.asteroidsmall2.islive:
                    self.asteroidsmalls.update(screen)
                else:
                    self.kill()
            else:
                self.asteroidsmall1 = AsteroidSmall(self.rect, random.randint(2, 5), random.randint(5, 10), random.randint(0, 360))
                self.asteroidsmall2 = AsteroidSmall(self.rect, random.randint(2, 5), random.randint(5, 10), random.randint(0, 360))
                self.hascreate = True
                self.asteroidsmalls.add(self.asteroidsmall1)
                self.asteroidsmalls.add(self.asteroidsmall2)
                group.add(self.asteroidsmall1)
                group.add(self.asteroidsmall2)
                self.asteroidsmalls.update(screen)

class AsteroidManager():
    def __init__(self):
        self.cd = 0
        self.asteroids = pygame.sprite.Group()
    def update(self, screen, group):
        if self.cd < 600:
            self.cd += 1
        elif self.cd == 600:
            x = 0
            y = 0
            nat1 = 0
            nat2 = 0
            pos = random.randint(0,1)
            if pos == 0:
                x = random.randint(1410, 1510)
                y = random.randint(0, 800)
                nat1 = np.degrees(np.arctan((x-1360)/y))+30
                nat2 = 90+np.degrees(np.arctan((800-y)/(x-1360)))-30
            elif pos == 1:
                x = random.randint(450, 1310)
                y = random.randint(850, 950)
                nat1 = 360-np.degrees(np.arctan((1360-x)/(y-800)))+30
                nat2 = 360+np.degrees(np.arctan(x/(y-800)))-30
            elif pos == 2:
                x = random.randint(450, 1310)
                y = random.randint(-150, -50)
                nat1 = 180-np.degrees(np.arctan(x/(-y)))+30
                nat2 = 180+np.degrees(np.arctan((1360-x)/(-y)))-30
            asteroid = Asteroid((x, y), random.randint(5, 10), random.randint(1, 5), random.randint(int(nat1), int(nat2)))
            self.asteroids.add(asteroid)
            group.add(asteroid)
            self.cd = 0
        self.asteroids.update(screen, group)