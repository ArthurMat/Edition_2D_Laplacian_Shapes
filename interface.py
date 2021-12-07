#!/usr/bin/env python3

import pygame
import sys
from copy import deepcopy
from redimension import *
from tools import *

def draw_poly(screen, points, seg):
    for key, value in seg.items():
        pygame.draw.line(screen, color=(0, 0, 0), start_pos=points[value[0]], end_pos=points[value[1]], width=2)

def draw_circle(screen, points, seg, pos):
    screen.fill((255, 255, 255))
    draw_poly(screen, points, seg)
    cercle = find_nearest(points, pos)
    pygame.draw.circle(screen, color=(255, 0, 0), center=cercle, radius=4)
    return [cercle]

def select(screen, points, seg, pos, pos2):
    liste = inside(points, pos, pos2)
    if len(liste) == 0:
        liste = draw_circle(screen, points, seg, pos)
    else:
        screen.fill((255, 255, 255))
        draw_poly(screen, points, seg)
        for elmt in liste:
            pygame.draw.circle(screen, color=(255, 0, 0), center=elmt, radius=4)
    return liste

def update(screen, points, seg, liste_cerlces):
    screen.fill((255, 255, 255))
    draw_poly(screen, points, seg)
    for cercle in liste_cerlces:
        pygame.draw.circle(screen, color=(255, 0, 0), center=cercle, radius=4)

def main_interface(points, seg, WIDTH=750, HEIGHT=750):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    # Faire une copie et repartir de la copie à chaque rescale.
    copy_points = deepcopy(points)
    points = redimension(points, WIDTH, HEIGHT)
    points = to_pygame(points, HEIGHT)

    screen.fill((255, 255, 255))
    draw_poly(screen, points, seg)

    pos = None
    mousedrag = False
    mouse_down = False
    liste_cerlces = []

    update(screen, points, seg, liste_cerlces)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = screen.get_size()
                liste_cerlces = []
                points = deepcopy(copy_points)
                points = to_pygame(redimension(points, WIDTH, HEIGHT), HEIGHT)
                update(screen, points, seg, liste_cerlces)
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                pos2 = pygame.mouse.get_pos()
                liste_cerlces = select(screen, points, seg, pos, pos2)
                mouse_down = False
                mousedrag = False
            if event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    actu_pos = pygame.mouse.get_pos()
                    mousedrag = True
        if mousedrag:
            update(screen, points, seg, liste_cerlces)
            mouseRectCorners = [pos, [pos[0], actu_pos[1]], actu_pos, [actu_pos[0], pos[1]]]
            pygame.draw.lines(screen, color=(0, 0, 255), closed=True, points=mouseRectCorners, width=1)
        
        pygame.display.update()