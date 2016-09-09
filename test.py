# -*- coding: utf-8 -*-


import pygame
from pygame.locals import *
from sys import exit
from gameRole import *

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT));
background_img = pygame.image.load('resources/Image/background.png');
window.blit(background_img,(0,0))
while True:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            exit()