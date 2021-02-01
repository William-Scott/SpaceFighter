import pygame
import random
import numpy as np
from pygame.locals import *
import sys
import os

from asteroid import *
from background import *
from button import *
from collision import *
from enemy import *
from player import *
from score import *
from shock import *
from state import *

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

    if statem.state.get('ready'):
        players.empty()
        bullet_ps.empty()
        bullet_es.empty()
        enemys.empty()
        asteroids.empty()
        em.enemys.empty()
        em.cd = 0
        em.time = 0
        em.stage = 1
        em.round = 1
        em.hasboss = False
        am.asteroids.empty()
        pm.players.empty()
        sm.score = 0
        pm.life = 6
        statem.changestate('ready', 'start')
    elif statem.state.get('start'):
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