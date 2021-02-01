import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

from ai import *
from enemyweapon import *
from respath import resource_path

class Enemy(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super(Enemy, self).__init__()
        self.surf_enemy_image = pygame.image.load(resource_path("res\\enemy.png")).convert_alpha()
        self.surf_boss_image = pygame.image.load(resource_path("res\\boss1.png")).convert_alpha()
        self.surf_explosion_image = pygame.image.load(resource_path("res\\explosion.png")).convert_alpha()
        self.surf_enemy_1a = pygame.transform.scale(self.surf_enemy_image.subsurface((3,1),(23,27)), (115,135))
        self.surf_enemy_1b = pygame.transform.scale(self.surf_enemy_image.subsurface((32,4),(23,22)), (115,110))
        self.surf_enemy_1c = pygame.transform.scale(self.surf_enemy_image.subsurface((61,10),(23,11)), (115,55))
        self.surf_enemy_1d = pygame.transform.scale(self.surf_enemy_image.subsurface((90,8),(23,11)), (115,55))
        self.surf_enemy_1e = pygame.transform.scale(self.surf_enemy_image.subsurface((119,3),(23,22)), (115,110))
        self.surf_enemy_2a = pygame.transform.scale(self.surf_enemy_image.subsurface((3,29),(23,27)), (115,135))
        self.surf_enemy_2b = pygame.transform.scale(self.surf_enemy_image.subsurface((32,32),(23,22)), (115,110))
        self.surf_enemy_2c = pygame.transform.scale(self.surf_enemy_image.subsurface((61,38),(23,11)), (115,55))
        self.surf_enemy_2d = pygame.transform.scale(self.surf_enemy_image.subsurface((90,36),(23,11)), (115,55))
        self.surf_enemy_2e = pygame.transform.scale(self.surf_enemy_image.subsurface((119,31),(23,22)), (115,110))
        self.surf_boss_1a = pygame.transform.scale(self.surf_boss_image.subsurface((0,0),(60,90)), (300,450))
        self.surf_explosion_a = pygame.transform.scale(self.surf_explosion_image.subsurface((11,11),(10,10)), (50,50))
        self.surf_explosion_b = pygame.transform.scale(self.surf_explosion_image.subsurface((36,6),(24,22)), (120,110))
        self.surf_explosion_c = pygame.transform.scale(self.surf_explosion_image.subsurface((66,5),(28,24)), (140,120))
        self.surf_explosion_d = pygame.transform.scale(self.surf_explosion_image.subsurface((98,4),(28,26)), (140,130))
        self.surf_explosion_e = pygame.transform.scale(self.surf_explosion_image.subsurface((130,3),(28,27)), (140,135))
        self.image = self.surf_enemy_1a
        self.rect = self.image.get_rect(center=(posx, posy))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5
        self.health = 1
        self.cden = 0
        self.cdex = 0
        self.islive = True
        self.bullets = pygame.sprite.Group()
        self.timeline = 0

class Enemy0(Enemy):
    def __init__(self, posx, posy, players):
        super(Enemy0, self).__init__(posx, posy)
        self.ai = Ai(self, players, 0)
        self.health = 1
    def update(self, screen, bullet_es):
        if self.islive:
            self.ai.update(self.bullets, bullet_es)
            if self.cden < 10:
                self.image = self.surf_enemy_1a
                screen.blit(self.image, (self.rect[0],self.rect[1]))
                self.cden += 1
            elif self.cden >= 10 and self.cden < 20:
                self.image = self.surf_enemy_1b
                screen.blit(self.image, (self.rect[0],self.rect[1]+15))
                self.cden += 1
            elif self.cden >= 20 and self.cden < 30:
                self.image = self.surf_enemy_1c
                screen.blit(self.image, (self.rect[0],self.rect[1]+45))
                self.cden += 1
            elif self.cden >= 30 and self.cden < 40:
                self.image = self.surf_enemy_1d
                screen.blit(self.image, (self.rect[0],self.rect[1]+35))
                self.cden += 1
            elif self.cden >= 40 and self.cden < 49:
                self.image = self.surf_enemy_1e
                screen.blit(self.image, (self.rect[0],self.rect[1]+10))
                self.cden += 1
            elif self.cden == 49:
                self.image = self.surf_enemy_1e
                screen.blit(self.image, (self.rect[0],self.rect[1]+10))
                self.cden = 0
            if self.rect.right < 0:
                self.kill()
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
                self.kill()
class Enemy1(Enemy0):
    def __init__(self, posx, posy, players):
        super(Enemy1, self).__init__(posx, posy, players)
        self.ai = Ai(self, players, 1)
class Enemy2(Enemy):
    def __init__(self, posx, posy, players):
        super(Enemy2, self).__init__(posx, posy)
        self.health = 2
        self.ai = Ai(self, players, 2)
    def update(self, screen, bullet_es):
        if self.islive:
            self.ai.update(self.bullets, bullet_es)
            self.bullets.update(screen)
            if self.cden < 10:
                self.image = self.surf_enemy_2a
                screen.blit(self.image, (self.rect[0],self.rect[1]))
                self.cden += 1
            elif self.cden >= 10 and self.cden < 20:
                self.image = self.surf_enemy_2b
                screen.blit(self.image, (self.rect[0],self.rect[1]+15))
                self.cden += 1
            elif self.cden >= 20 and self.cden < 30:
                self.image = self.surf_enemy_2c
                screen.blit(self.image, (self.rect[0],self.rect[1]+45))
                self.cden += 1
            elif self.cden >= 30 and self.cden < 40:
                self.image = self.surf_enemy_2d
                screen.blit(self.image, (self.rect[0],self.rect[1]+35))
                self.cden += 1
            elif self.cden >= 40 and self.cden < 49:
                self.image = self.surf_enemy_2e
                screen.blit(self.image, (self.rect[0],self.rect[1]+10))
                self.cden += 1
            elif self.cden == 49:
                self.image = self.surf_enemy_2e
                screen.blit(self.image, (self.rect[0],self.rect[1]+10))
                self.cden = 0
            if self.rect.right < 0:
                self.kill()
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

class Boss1(Enemy):
    def __init__(self, posx, posy, players):
        super(Boss1, self).__init__(posx, posy)
        self.speed = 1
        self.health = 59
        self.mask = pygame.mask.from_surface(self.surf_boss_1a)
        #self.weapon1 = Boss1Weapon(-45)
        #self.weapon2 = Boss1Weapon(45)
        self.ai = Ai(self, players, 3)
    def update(self, screen, bullet_es):
        if self.islive:
            self.ai.update(self.bullets, bullet_es)
            self.bullets.update(screen, self)
            if self.cden < 10:
                self.image = self.surf_boss_1a
                screen.blit(self.image, (self.rect[0],self.rect[1]))
                self.cden += 1
            elif self.cden >= 10 and self.cden < 20:
                self.image = self.surf_boss_1a
                screen.blit(self.image, (self.rect[0],self.rect[1]))
                self.cden += 1
            elif self.cden >= 20 and self.cden < 30:
                self.image = self.surf_boss_1a
                screen.blit(self.image, (self.rect[0],self.rect[1]))
                self.cden += 1
            elif self.cden >= 30 and self.cden < 40:
                self.image = self.surf_boss_1a
                screen.blit(self.image, (self.rect[0],self.rect[1]))
                self.cden += 1
            elif self.cden >= 40 and self.cden < 49:
                self.image = self.surf_boss_1a
                screen.blit(self.image, (self.rect[0],self.rect[1]))
                self.cden += 1
            elif self.cden == 49:
                self.image = self.surf_boss_1a
                screen.blit(self.image, (self.rect[0],self.rect[1]))
                self.cden = 0
            if self.rect.right < 0:
                self.kill()
        else:
            if self.cdex < 5:
                screen.blit(self.surf_explosion_a, (self.rect[0]+135,self.rect[1]+215))
                self.cdex += 1
            elif self.cdex >= 5 and self.cdex < 10:
                screen.blit(self.surf_explosion_b, (self.rect[0]+100,self.rect[1]+170))
                self.cdex += 1
            elif self.cdex >= 10 and self.cdex < 15:
                screen.blit(self.surf_explosion_c, (self.rect[0]+100,self.rect[1]+175))
                self.cdex += 1
            elif self.cdex >= 15 and self.cdex < 20:
                screen.blit(self.surf_explosion_d, (self.rect[0]+100,self.rect[1]+175))
                self.cdex += 1
            elif self.cdex >= 20 and self.cdex < 24:
                screen.blit(self.surf_explosion_e, (self.rect[0]+100,self.rect[1]+175))
                self.cdex += 1
            elif self.cdex == 24: 
                screen.blit(self.surf_explosion_e, (self.rect[0]+100,self.rect[1]+175))
                self.cdex += 1
                self.kill()
            if self.bullets.sprites():
                self.bullets.update(screen, self)

class EnemyManager():
    def __init__(self):
        self.cd = 0
        self.time = 1
        self.stage = 4
        self.round = 1
        self.enemys = pygame.sprite.Group()
        self.hasboss = False
    def mob0(self, enemys, players, *pos):
        for p in pos:
            enemy0 = Enemy0(p[0], p[1], players)
            self.enemys.add(enemy0)
            enemys.add(enemy0)
    def mob1(self, enemys, players, *pos):
        for p in pos:
            enemy1 = Enemy1(p[0], p[1], players)
            self.enemys.add(enemy1)
            enemys.add(enemy1)
    def update(self, screen, enemys, players, bullet_es, sc):
        if self.stage == 1:
            if self.round == 1:
                if self.time <= 600:
                    if np.mod(self.time, 200) == 0:
                        self.mob0(enemys, players, (1410, 250), (1560 ,250), (1710, 250))
                    elif np.mod(self.time, 100) == 0:
                        self.mob0(enemys, players, (1410, 550), (1560 ,550), (1710, 550))
                    self.time += 1
                else:
                    if len(self.enemys) == 0:
                        self.round = 2
                        self.time = 1
                    else:
                        pass
            elif self.round == 2:
                if self.time <= 600:
                    if np.mod(self.time, 120) == 0:
                        self.mob1(enemys, players, (1410, 400))
                    self.time += 1
                else:
                    if len(self.enemys) == 0:
                        self.round = 3
                        self.time = 1
                    else:
                        pass
            elif self.round == 3:
                if self.time <= 600:
                    if np.mod(self.time, 200) == 0:
                        self.mob0(enemys, players, (1410, 400), (1510 ,250), (1610, 100))
                    elif np.mod(self.time, 100) == 0:
                        self.mob0(enemys, players, (1410, 400), (1510 ,550), (1610, 700))
                    self.time += 1
                else:
                    if len(self.enemys) == 0:
                        self.round = 4
                        self.time = 1
                    else:
                        pass
            elif self.round == 4:
                pass
            elif self.round == 5:
                if self.time <= 1200:
                    if np.mod(self.time, 400) == 0:
                        self.mob0(enemys, players, (1410, 400), (1410 ,250), (1510 ,550), (1510, 100), (1610, 700))
                    elif np.mod(self.time, 200) == 0:
                        self.mob0(enemys, players, (1410, 700), (1410 ,100), (1510 ,550), (1510, 250), (1610, 400))
                    self.time += 1
                else:
                    if len(self.enemys) == 0:
                        self.round = 0
                        self.time = 1
                        self.stage = 2
                    else:
                        pass
        elif self.stage == 2:
            if self.time < 10:
                if self.cd < 90:
                    self.cd += 1
                elif self.cd == 90:
                    enemy2 = Enemy2(random.randint(1360, 1560), random.randint(50, 750), players)
                    self.enemys.add(enemy2)
                    enemys.add(enemy2)
                    self.cd = 0
                    self.time += 1
            elif self.time == 10:
                if len(self.enemys) == 0:
                    self.stage = 4
                    self.time = 0
        elif self.stage == 3:
            pass
        elif self.stage == 4:
            if self.hasboss == False:
                boss1 = Boss1(1360, 250, players)
                self.enemys.add(boss1)
                enemys.add(boss1)
                self.hasboss = True
            if self.hasboss and len(self.enemys) == 0:
                sc('run', 'win')
        self.enemys.update(screen, bullet_es)