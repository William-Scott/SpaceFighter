import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

from bullet import *
from respath import resource_path

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.shot1 = pygame.mixer.Sound("res\\shot1.ogg")
        self.surf_player_image = pygame.image.load(resource_path("res\\player.png")).convert_alpha()
        self.surf_flash_image = pygame.image.load(resource_path("res\\flash.png")).convert_alpha()
        self.surf_explosion_image = pygame.image.load(resource_path("res\\explosion.png")).convert_alpha()
        self.surf_player_front =  pygame.transform.scale(self.surf_player_image.subsurface((0,0),(25,20)), (130,105))
        self.surf_player_down = pygame.transform.scale(self.surf_player_image.subsurface((26,0),(25,20)), (130,105))
        self.surf_player_up  = pygame.transform.scale(self.surf_player_image.subsurface((53,0),(25,20)), (130,105))
        self.surf_player_flash = pygame.transform.scale(self.surf_flash_image, (50,90))
        self.surf_explosion_a = pygame.transform.scale(self.surf_explosion_image.subsurface((11,11),(10,10)), (50,50))
        self.surf_explosion_b = pygame.transform.scale(self.surf_explosion_image.subsurface((36,6),(24,22)), (120,110))
        self.surf_explosion_c = pygame.transform.scale(self.surf_explosion_image.subsurface((66,5),(28,24)), (140,120))
        self.surf_explosion_d = pygame.transform.scale(self.surf_explosion_image.subsurface((98,4),(28,26)), (140,130))
        self.surf_explosion_e = pygame.transform.scale(self.surf_explosion_image.subsurface((130,3),(28,27)), (140,135))
        self.image = self.surf_player_front
        self.mask = pygame.mask.from_surface(self.image)
        self.posx = 0
        self.posy = 400
        self.rect = self.image.get_rect(center=(self.posx, self.posy))
        self.time = 0
        self.speed_x = 0
        self.speed_y = 0
        self.distance_x = 0
        self.distance_y = 0
        self.flash_cd = False
        self.cd = 0
        self.god = True
        self.islive = True
        self.bullets = pygame.sprite.Group()
        self.i = 0
        self.cdex = 0
    def shot(self, bullet_ps):
        bullet = Bullet_p(self.rect[0]+180, self.rect[1]+70, 15, -90)
        self.bullets.add(bullet)
        bullet_ps.add(bullet)
        channel = self.shot1.play(0,356,100)
    def update(self, screen, pressed_keys, pressed_mouse, pos_mouse, rel_mouse, bullet_ps):
        if self.i < 20:
            self.god = True
            self.i += 1
            self.rect = self.image.get_rect(center=(self.posx, self.posy))
            if np.mod(self.i, 30) < 15:
                screen.blit(self.image, self.rect)
            self.posx += 10
        else:
            self.i += 1
            #print(self.i)
            if self.i < 120:
                self.god = True
            else:
                self.god = False
            if self.islive:
                self.time = 0.5
                self.speed_x = rel_mouse[0]
                self.speed_y = rel_mouse[1]
                #限制最大速度
                if self.speed_y >= 300:
                    self.speed_y = 300
                elif self.speed_y <= -300:
                    self.speed_y = -300
                if self.speed_x >=300:
                    self.speed_x = 300
                elif self.speed_x <= -300:
                    self.speed_x = -300
                if self.speed_y == 0:
                    self.image = self.surf_player_front
                elif self.speed_y >= 1:
                    self.image = self.surf_player_down
                elif self.speed_y <= -1:
                    self.image = self.surf_player_up
                self.distance_x = self.speed_x * self.time
                self.distance_y = self.speed_y * self.time
                self.posx = self.posx + self.distance_x
                self.posy = self.posy + self.distance_y
                # 限定player在屏幕中
                if self.posx < 75:
                    self.posx = 75
                elif self.posx > 1285:
                    self.posx = 1285
                if self.posy < 62:
                    self.posy = 62
                elif self.posy > 738:
                    self.posy = 738
                self.rect = self.image.get_rect(center=(self.posx, self.posy))
                if self.i < 120:
                    if np.mod(self.i, 30) < 15:
                        screen.blit(self.image, self.rect)
                else:
                    screen.blit(self.image, self.rect)
                self.bullets.update(screen)
                if pressed_mouse[0] and self.flash_cd == False:
                    if self.speed_y == 0:
                        screen.blit(self.surf_player_flash, (self.rect[0]+130,self.rect[1]+25))
                    elif self.speed_y >= 1:
                        screen.blit(self.surf_player_flash, (self.rect[0]+130,self.rect[1]+15))
                    elif self.speed_y <= 1:
                        screen.blit(self.surf_player_flash, (self.rect[0]+130,self.rect[1]+15))
                    #发射子弹
                    self.shot(bullet_ps)
                    self.flash_cd = True
                if self.flash_cd == True and self.cd < 5:
                    self.cd += 1
                    if self.speed_y == 0:
                        screen.blit(self.surf_player_flash, (self.rect[0]+130,self.rect[1]+25))
                    elif self.speed_y >= 1:
                        screen.blit(self.surf_player_flash, (self.rect[0]+130,self.rect[1]+15))
                    elif self.speed_y <= 1:
                        screen.blit(self.surf_player_flash, (self.rect[0]+130,self.rect[1]+15))
                elif self.flash_cd == True and self.cd < 10:
                    self.cd += 1
                elif self.flash_cd == True and self.cd == 10:
                    self.flash_cd = False
                    self.cd = 0
            else:
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
                else:
                    if len(self.bullets.sprites()) == 0:
                        self.kill()
                if self.bullets.sprites():
                    self.bullets.update(screen)

class PlayerManager():
    def __init__(self):
        self.players = pygame.sprite.Group()
        self.life = 6
    def update(self, screen, pressed_keys, pressed_mouse, pos_mouse, rel_mouse, bullet_ps, players, sc):
        if len(self.players) == 0:
            self.life -= 1
            if self.life:
                player = Player()
                self.players.add(player)
                players.add(player)
            else:
                sc('run', 'over')
        self.players.update(screen, pressed_keys, pressed_mouse, pos_mouse, rel_mouse, bullet_ps)