import xlrd
from bullet import *

class Ai():
    def __init__(self, body, players, es):
        self.body = body
        self.rect = body.rect
        self.speed = body.speed
        self.players = players
        self.posx = 0
        self.posy = 0
        self.cd = 0
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
    def shot2(self, bullets, bullet_es):
        bullet1 = Bullet_e2(self.rect[0], self.rect[1]+225, 5, 36)
        bullet2 = Bullet_e2(self.rect[0], self.rect[1]+225, 5, 72)
        bullet3 = Bullet_e2(self.rect[0], self.rect[1]+225, 5, 108)
        bullet4 = Bullet_e2(self.rect[0], self.rect[1]+225, 5, 144)
        bullets.add(bullet1)
        bullets.add(bullet2)
        bullets.add(bullet3)
        bullets.add(bullet4)
        bullet_es.add(bullet1)
        bullet_es.add(bullet2)
        bullet_es.add(bullet3)
        bullet_es.add(bullet4)
    def avoid(self):
        pass
    def seek(self):
        if self.players.sprites():
            self.posx = self.players.sprites()[0].posx
            self.posy = self.players.sprites()[0].posy-55
    def update(self, bullets=None, bullet_es=None):
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
                            elif pointer.name == "go_direction":
                                self.go_direction(pointer.extra)
                            elif pointer.name == "shot1":
                                self.shot1(bullets, bullet_es)
                            elif pointer.name == "shot2":
                                self.shot2(bullets, bullet_es, 36)
                                self.shot2(bullets, bullet_es, 72)
                                self.shot2(bullets, bullet_es, 108)
                                self.shot2(bullets, bullet_es, 144)
                            elif pointer.name == "stop":
                                pass
                            elif pointer.name == "avoid":
                                self.avoid()
                            elif pointer.name == "seek":
                                self.seek()
                            elif pointer.name == "hit":
                                self.hit()
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