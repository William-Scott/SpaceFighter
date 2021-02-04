# SpaceFighter
Game by Pygame

运行所需库：

pygame
numpy
xlrd

敌人脚本文件说明：

num：此行为的顺序，相同顺序的行为会同时执行

name：行为的名字，save是设置循环点，load是返回到save点以完成循环

last:该行为持续的帧数

interval：做完一次行为后停止的帧数

cycles：循环的次数，因为每个num为一组，长度为max（cycles（last+interval），其中较短的行为可以循环执行，比如在一次向前走中连开两次枪，间隔是1s

extra：额外传入的一些参数，比如go_direction（向某个方向走）可以传入走的方向（度数）
