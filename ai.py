import xlrd
from bullet import *

class Ai():
    def __init__(self, body, players, species, es):
        self.timeline = 0
        self.body = body
        self.rect = body.rect
        self.speed = body.speed
        self.players = players
        self.posx = 0
        self.posy = 0
        self.cd = 0
        self.species = species
        self.seqlistsum = es
        self.save = 0
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
                    for pointer in pointerlist:
                        if not pointer.haspass:
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
                                #由于是先重置再updata,所以load并不能重置自身，所以load可以不update
                                if pointer.name == "load":
                                    for pointerlist_ in self.seqlistsum:
                                        for pointer_ in pointerlist_:
                                            if pointer_.num >= self.save:
                                                pointer_.restore()
                                hasst = True
                            elif pointer.state == "wait":
                                pointer.update()
                                hasst = True
                    if hasst:
                        break

