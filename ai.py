import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

from bullet import *

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
        self.seqlist1 = []
        self.seqlist2 = []
        self.seqlist3 = []
        self.seqlist4 = []
        self.seqlist5 = []
        self.seqlist6 = []
        self.seqlist7 = []
        self.seqlist8 = []
        self.seqlist9 = []
        self.seqlist10 = []
        self.seqlistsum = []
        self.save = 0
        if species == 3:
            self.seq1 = Sequence(1, "go_forward", 180, 0, 1)
            self.seq2 = Sequence(2, "stop", 60, 0, 1)
            self.seq3 = Sequence(2, "shot2", 1, 19, 3)
            self.seq4 = Sequence(2, "save", 1, 0, 1)
            self.seq5 = Sequence(3, "go_up", 120, 0, 1)
            self.seq6 = Sequence(3, "shot1", 1, 19, 6)
            self.seq7 = Sequence(4, "stop", 60, 0, 1)
            self.seq8 = Sequence(4, "shot2", 1, 19, 3)
            self.seq9 = Sequence(5, "go_down", 120, 0, 1)
            self.seq10 = Sequence(5, "shot1", 1, 19, 6)
            self.seq11 = Sequence(6, "stop", 60, 0, 1)
            self.seq12 = Sequence(6, "shot2", 1, 19, 3)
            self.seq13 = Sequence(7, "go_down", 120, 0, 1)
            self.seq14 = Sequence(7, "shot1", 1, 19, 6)
            self.seq15 = Sequence(8, "stop", 60, 0, 1)
            self.seq16 = Sequence(8, "shot2", 1, 19, 3)
            self.seq17 = Sequence(9, "go_up", 120, 0, 1)
            self.seq18 = Sequence(9, "shot1", 1, 19, 6)
            self.seq19 = Sequence(10, "load", 1, 0, 1)
            self.seqlist1.append(self.seq1)
            self.seqlist2.append(self.seq2)
            self.seqlist2.append(self.seq3)
            self.seqlist2.append(self.seq4)
            self.seqlist3.append(self.seq5)
            self.seqlist3.append(self.seq6)
            self.seqlist4.append(self.seq7)
            self.seqlist4.append(self.seq8)
            self.seqlist5.append(self.seq9)
            self.seqlist5.append(self.seq10)
            self.seqlist6.append(self.seq11)
            self.seqlist6.append(self.seq12)
            self.seqlist7.append(self.seq13)
            self.seqlist7.append(self.seq14)
            self.seqlist8.append(self.seq15)
            self.seqlist8.append(self.seq16)
            self.seqlist9.append(self.seq17)
            self.seqlist9.append(self.seq18)
            self.seqlist10.append(self.seq19)
            self.seqlistsum.append(self.seqlist1)
            self.seqlistsum.append(self.seqlist2)
            self.seqlistsum.append(self.seqlist3)
            self.seqlistsum.append(self.seqlist4)
            self.seqlistsum.append(self.seqlist5)
            self.seqlistsum.append(self.seqlist6)
            self.seqlistsum.append(self.seqlist7)
            self.seqlistsum.append(self.seqlist8)
            self.seqlistsum.append(self.seqlist9)
            self.seqlistsum.append(self.seqlist10)
    def go_up(self):
        self.rect.move_ip(0, -self.speed)
    def go_down(self):
        self.rect.move_ip(0, self.speed)
    def go_forward(self):
        self.rect.move_ip(-self.speed, 0)
    def go_backward(self):
        self.rect.move_ip(self.speed, 0)
    def go_direction(self, direction, rotation=False):
        v = pygame.Vector2()
        v.xy = 0,1
        v.rotate_ip(direction)
        v = v*self.speed
        self.rect[0] += v.x
        self.rect[1] -= v.y
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
        bullet = Bullet_e1(self.rect[0]-30, self.rect[1]+225, 7, 90)
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
            if self.body.islive:
                self.go_forward()
        elif self.species == 1:
            if self.body.islive:
                if self.timeline < 180:
                    self.go_direction(self.timeline)
                elif self.timeline >= 180 and self.timeline < 360:
                    self.go_direction(-self.timeline)
                self.timeline += 1
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
                for pointerlist in self.seqlistsum:
                    hasst = False
                    #print(random.randint(1,99))
                    for pointer in pointerlist:
                        #print(random.randint(1,99))
                        #print(pointer.haspass)
                        if not pointer.haspass:
                            #print(random.randint(1,99))
                            if pointer.state == "play":
                                if pointer.name == "go_up":
                                    self.go_up()
                                elif pointer.name == "go_down":
                                    self.go_down()
                                elif pointer.name == "go_forward":
                                    self.go_forward()
                                elif pointer.name == "go_backward":
                                    self.go_backward()
                                elif pointer.name == "shot1":
                                    self.shot1(bullets, bullet_es)
                                elif pointer.name == "shot2":
                                    self.shot2(bullets, bullet_es, 36)
                                    self.shot2(bullets, bullet_es, 72)
                                    self.shot2(bullets, bullet_es, 108)
                                    self.shot2(bullets, bullet_es, 144)
                                elif pointer.name == "stop":
                                    pass
                                elif pointer.name == "save":
                                    self.save = pointer.num
                                pointer.update()
                                if pointer.name == "load":
                                    for pointerlist_ in self.seqlistsum:
                                        for pointer_ in pointerlist_:
                                            if pointer_.num >= self.save:
                                                pointer_.restore()
                                                #print(pointer_.name,pointer_.haspass)
                                hasst = True
                            elif pointer.state == "wait":
                                pointer.update()
                                hasst = True
                    if hasst:
                        break

class Sequence():
    def __init__(self, num, name, last, interval, cycles, priority=0):
        self.num = num
        self.name = name
        self.last_old = last
        self.last = last
        self.interval_old = interval
        self.interval = interval
        self.cycles_old = cycles
        self.cycles = cycles
        self.priority = priority
        self.haspass = False
        self.state = "play"
    def update(self):
        if self.cycles > 0:
            if self.state == "play":
                self.last -= 1
                if self.last <= 0:
                    self.state = "wait"
            elif self.state == "wait":
                self.interval -= 1
                if self.interval <= 0:
                    self.last = self.last_old
                    self.interval = self.interval_old
                    self.state = "play"
                    self.cycles -= 1
                    if self.cycles == 0:
                        self.haspass = True
        else:
            self.haspass = True
    def restore(self):
        self.last = self.last_old
        self.interval = self.interval_old
        self.cycles = self.cycles_old
        self.state = "play"
        self.haspass = False