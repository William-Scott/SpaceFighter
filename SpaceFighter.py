import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

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
                elif self.flash_cd == True and self.cd < 20:
                    self.cd += 1
                elif self.flash_cd == True and self.cd == 20:
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

class Enemy1(Enemy):
    def __init__(self, posx, posy, players):
        super(Enemy1, self).__init__(posx, posy)
        print("to modle 1")
        self.ai = Ai(self, players, 1)
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

class Enemy2(Enemy):
    def __init__(self, posx, posy, players):
        super(Enemy2, self).__init__(posx, posy)
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
        self.speed = 3
        self.health = 49
        self.mask = pygame.mask.from_surface(self.surf_boss_1a)
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

class Ai():
    def __init__(self, body, players, species):
        self.timeline = 0
        self.body = body
        self.rect = body.rect
        self.speed = body.speed
        self.players = players
        self.posx = 0
        self.posy = 0
        self.cd = 0
        self.species = species
    def go_up(self):
        self.rect.move_ip(0, -self.speed)
    def go_down(self):
        self.rect.move_ip(0, self.speed)
    def go_forward(self):
        self.rect.move_ip(-self.speed, 0)
    def go_backward(self):
        self.rect.move_ip(self.speed, 0)
    def hit(self):
        if self.players.sprites():
            if self.rect[1] > self.posy+50:
                self.go_up()
            elif self.rect[1] < self.posy-50:
                self.go_down()
            if self.rect[0] > self.posx+50:
                self.go_forward()
            elif self.rect[0] < self.posx-50:
                self.go_backward()
    def shot1(self, bullets, bullet_es):
        bullet = Bullet_e1(self.rect[0]-30, self.rect[1]+65, 7, 90)
        bullets.add(bullet)
        bullet_es.add(bullet)
    def shot2(self, bullets, bullet_es, direction):
        bullet = Bullet_e2(self.rect[0], self.rect[1]+225, 5, direction)
        bullets.add(bullet)
        bullet_es.add(bullet)
    def avoid(self):
        pass
    def seek(self):
        if self.players.sprites():
            self.posx = self.players.sprites()[0].posx
            self.posy = self.players.sprites()[0].posy-55
    def update(self, bullets=None, bullet_es=None):
        if self.species == 0:
            pass
        elif self.species == 1:
            if self.body.islive:
                if self.timeline < 360:
                    if self.cd < 60:
                        self.cd += 1
                    elif self.cd == 60:
                        self.seek()
                        self.cd = 0
                    self.hit()
                    self.timeline += 1
                else:
                    self.go_forward()
        elif self.species == 2:
            if self.body.islive:
                if self.timeline < 360:
                    if self.cd < 60:
                        self.cd += 1
                    elif self.cd == 60:
                        self.seek()
                        self.shot1(bullets, bullet_es)
                        self.cd = 0
                    self.hit()
                    self.timeline += 1
                else:
                    self.go_forward()
        elif self.species == 3:
            if self.body.islive:
                if self.timeline < 90:
                    self.go_forward()
                    self.timeline += 1
                elif self.timeline >= 90 and self.timeline < 120:
                    self.timeline += 1
                elif self.timeline >= 120 and self.timeline < 180:
                    if np.mod(self.timeline,20) == 0:
                        self.shot2(bullets, bullet_es, 90)
                    self.go_up()
                    self.timeline += 1
                elif self.timeline >= 180 and self.timeline < 240:
                    if np.mod(self.timeline,30) == 0:
                        self.shot2(bullets, bullet_es, 30)
                        self.shot2(bullets, bullet_es, 60)
                        self.shot2(bullets, bullet_es, 120)
                        self.shot2(bullets, bullet_es, 150)
                    self.timeline += 1
                elif self.timeline >= 240 and self.timeline < 300:
                    if np.mod(self.timeline,20) == 0:
                        self.shot2(bullets, bullet_es, 90)
                    self.go_down()
                    self.timeline += 1
                elif self.timeline >= 300 and self.timeline < 360:
                    if np.mod(self.timeline,30) == 0:
                        self.shot2(bullets, bullet_es, 30)
                        self.shot2(bullets, bullet_es, 60)
                        self.shot2(bullets, bullet_es, 120)
                        self.shot2(bullets, bullet_es, 150)
                    self.timeline += 1
                elif self.timeline >= 360 and self.timeline < 420:
                    if np.mod(self.timeline,20) == 0:
                        self.shot2(bullets, bullet_es, 90)
                    self.go_down()
                    self.timeline += 1
                elif self.timeline >= 420 and self.timeline < 480:
                    if np.mod(self.timeline,30) == 0:
                        self.shot2(bullets, bullet_es, 30)
                        self.shot2(bullets, bullet_es, 60)
                        self.shot2(bullets, bullet_es, 120)
                        self.shot2(bullets, bullet_es, 150)
                    self.timeline += 1
                elif self.timeline >= 480 and self.timeline < 540:
                    if np.mod(self.timeline,20) == 0:
                        self.shot2(bullets, bullet_es, 90)
                    self.go_up()
                    self.timeline += 1
                elif self.timeline >= 540 and self.timeline < 599:
                    if np.mod(self.timeline,30) == 0:
                        self.shot2(bullets, bullet_es, 30)
                        self.shot2(bullets, bullet_es, 60)
                        self.shot2(bullets, bullet_es, 120)
                        self.shot2(bullets, bullet_es, 150)
                    self.timeline += 1
                elif self.timeline == 599:
                    self.timeline = 120

class EnemyManager():
    def __init__(self):
        self.cd = 0
        self.time = 0
        self.stage = 1
        self.enemys = pygame.sprite.Group()
        self.hasboss = False
    def update(self, screen, enemys, players, bullet_es, sc):
        if self.stage == 1:
            if self.cd < 60:
                self.cd += 1
            elif self.cd == 60:
                enemy1 = Enemy1(random.randint(1360, 1560), random.randint(50, 750), players)
                self.enemys.add(enemy1)
                enemys.add(enemy1)
                self.cd = 0
                self.time += 1
            if self.time == 16:
                self.stage = 2
                self.time = 0
        elif self.stage == 2:
            if self.cd < 90:
                self.cd += 1
            elif self.cd == 90:
                enemy2 = Enemy2(random.randint(1360, 1560), random.randint(50, 750), players)
                self.enemys.add(enemy2)
                enemys.add(enemy2)
                self.cd = 0
                self.time += 1
            if self.time == 10:
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
    def update(self, screen):
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
    def update(self, screen):
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
    def update(self, screen, body):
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
                sc('over', 'start')
                self.beclick = False
        else:
            self.beclick = False
            self.image = self.surf_con_a
            self.rect = self.image.get_rect(center=(680,350))
        screen.blit(self.image, self.rect)

class StateManager():
    def __init__(self):
        self.state = {'start':True, 'run':False, 'pause':False, 'over':False, 'win':False, 'end':False}
    def changestate(self, state_from, state_to):
        if state_from == "all":
            for key in list(self.state.keys()):
                self.state[key] = False
            self.state[state_to] = True
        else:
            self.state[state_from] = False
            self.state[state_to] = True

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

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 初始化 pygame
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
# 创建屏幕对象
# 设定尺寸
display = pygame.display.set_mode((1350,790), NOFRAME, 32)
screen = pygame.Surface((1360,800))

#ADDENEMY = pygame.USEREVENT +1
#pygame.time.set_timer(ADDENEMY,250)
# 初始化管理类
statem = StateManager()
bm = BackGroundManager()
em = EnemyManager()
am = AsteroidManager()
pm = PlayerManager()
sm = ScoreManager()
shock = Shock()
bts = BtStart()
btq = BtQuit()
btc = BtCon()
btrs = BtReStart()
over = Over()
win = Win()

players = pygame.sprite.Group()
bullet_ps = pygame.sprite.Group()
bullet_es = pygame.sprite.Group()
enemys = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

cd = CollisionDetection(bullet_ps, bullet_es, enemys, asteroids, players)
# 用于保证主循环运行的变量
running = True

pygame.mixer.music.load("res\\spaceasteroids.ogg")
pygame.mixer.music.play(-1)
# 主循环！
while running:
    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    if statem.state.get('start'):
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        pressed_mouse = pygame.mouse.get_pressed()
        pos_mouse = pygame.mouse.get_pos()
        bm.update(screen)
        bts.update(screen, pos_mouse, pressed_mouse, statem.changestate)
        btq.update(screen, pos_mouse, pressed_mouse, statem.changestate)
        shock.update(display, screen)
        players.empty()
        bullet_ps.empty()
        bullet_es.empty()
        enemys.empty()
        asteroids.empty()
        em.enemys.empty()
        em.cd = 0
        em.time = 0
        em.stage = 1
        em.hasboss = False
        am.asteroids.empty()
        pm.players.empty()
        sm.score = 0
        pm.life = 6
        pygame.display.flip()
    elif statem.state.get('run'):
        pressed_keys = 0
        # 让pygame完全控制鼠标
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_SPACE:
                    statem.changestate('run', 'pause')
                else:
                    pressed_keys = pygame.key.get_pressed()
        bm.update(screen)
        em.update(screen, enemys, players, bullet_es, statem.changestate)
        am.update(screen, asteroids)
        pressed_mouse = pygame.mouse.get_pressed()
        pos_mouse = pygame.mouse.get_pos()
        rel_mouse = pygame.mouse.get_rel()
        pm.update(screen, pressed_keys, pressed_mouse, pos_mouse, rel_mouse, bullet_ps, players, statem.changestate)
        cd.update(screen, shock.setshock, sm.score_up)
        sm.update(screen)
        shock.update(display, screen)
        # 更新
        pygame.display.flip()
    elif statem.state.get('pause'):
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        pressed_mouse = pygame.mouse.get_pressed()
        pos_mouse = pygame.mouse.get_pos()
        bm.update(screen)
        btc.update(screen, pos_mouse, pressed_mouse, statem.changestate)
        btq.update(screen, pos_mouse, pressed_mouse, statem.changestate)
        shock.update(display, screen)
        pygame.display.flip()
    elif statem.state.get('over'):
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        pressed_mouse = pygame.mouse.get_pressed()
        pos_mouse = pygame.mouse.get_pos()
        bm.update(screen)
        over.update(screen)
        btrs.update(screen, pos_mouse, pressed_mouse, statem.changestate)
        sm.update(screen)
        shock.update(display, screen)
        pygame.display.flip()
    elif statem.state.get('win'):
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        pressed_mouse = pygame.mouse.get_pressed()
        pos_mouse = pygame.mouse.get_pos()
        bm.update(screen)
        win.update(screen)
        btq.update(screen, pos_mouse, pressed_mouse, statem.changestate)
        sm.update(screen)
        shock.update(display, screen)
        pygame.display.flip()
    elif statem.state.get('end'):
        running = False
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)