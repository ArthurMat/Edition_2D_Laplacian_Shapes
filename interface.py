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
    return [cercle]

def select(screen, points, seg, pos, pos2):
    liste = inside(points, pos, pos2)
    if len(liste) == 0:
        liste = draw_circle(screen, points, seg, pos)
    return liste

def update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT):
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(0, 0, WIDTH, 0.05 * HEIGHT))
    draw_poly(screen, points, seg)
    for cercle in liste_cerlces:
        pygame.draw.circle(screen, color=(255, 0, 0), center=cercle, radius=4)

def main_interface(points, seg, WIDTH=750, HEIGHT=750):
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    # Faire une copie et repartir de la copie à chaque rescale.
    points = to_pygame(points, WIDTH, HEIGHT)
    copy_points = deepcopy(points)
    points = redimension(points, WIDTH, HEIGHT)

    screen.fill((255, 255, 255))
    draw_poly(screen, points, seg)    

    pos = None
    mousedrag = False
    mouse_down = False
    select_mode = True
    liste_cerlces = []

    update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    select_mode = not select_mode
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = screen.get_size()
                points = deepcopy(copy_points)
                liste_cerlces = []
                points = redimension(points, WIDTH, HEIGHT)
                update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT)
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] > HEIGHT * 0.05:
                    mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                pos2 = pygame.mouse.get_pos()
                if mouse_down and select_mode:
                    liste_cerlces = select(screen, points, seg, pos, pos2)
                    mouse_down = False
                    mousedrag = False
                    update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT)
            if event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    actu_pos = pygame.mouse.get_pos()
                    mousedrag = True
        if mousedrag and select_mode:
            update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT)
            mouseRectCorners = [pos, [pos[0], actu_pos[1]], actu_pos, [actu_pos[0], pos[1]]]
            pygame.draw.lines(screen, color=(0, 0, 255), closed=True, points=mouseRectCorners, width=1)
        elif mousedrag and not select_mode:
            continue  # fonction move(points, liste_cercle) avec fonction qui lie liste_cercle et points
        pygame.display.update()


        # https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/
        