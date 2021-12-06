#!/usr/bin/env python3

import pygame
import sys
from redimension import *
from tools import *

def draw_poly(screen, points, seg):
    for key, value in seg.items():
        pygame.draw.line(screen, color=(0, 0, 0), start_pos=points[value[0]], end_pos=points[value[1]], width=2)

def draw_circle(screen, points, seg, pos):
    screen.fill((255, 255, 255))
    draw_poly(screen, points, seg)
    cercle = find_nearest(points, pos)
    pygame.draw.circle(screen, color=(255, 0, 0), center=cercle, radius=5)

def select(screen, points, seg, pos, pos2):
    liste = inside(points) #check si points dans selection sinon draw circle si oui recupe les point et circle sur tous

def main_interface(points, seg, WIDTH=1000, HEIGHT=1000):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    clock = pygame.time.Clock()

    points = redimension(points, WIDTH, HEIGHT)

    screen.fill((255, 255, 255))
    draw_poly(screen, points, seg)

    pos = None
    
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                pos2 = pygame.mouse.get_pos()
                select(screen, points, seg, pos, pos2)

        pygame.display.update()