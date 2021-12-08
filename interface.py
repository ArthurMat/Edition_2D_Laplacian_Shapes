#!/usr/bin/env python3

import sys
import pygame
from tools import *
from copy import deepcopy

def draw_poly(screen, points, seg):
    for key, value in seg.items():
        pygame.draw.line(screen, color=(0, 0, 0), start_pos=points[value[0]], end_pos=points[value[1]], width=2)

def select(points, pos, pos2):
    liste = inside(points, pos, pos2)
    if len(liste) == 0:
        cercle = find_nearest(points, pos)
        liste.append(cercle)
    return liste

def move(points, liste_cercles, pos, pos2):
    dx = (pos2[0] - pos[0]) / 1  # Gain
    dy = (pos2[1] - pos[1]) / 1  # Gain
    for key in liste_cercles:
        points[key][0] += dx
        points[key][1] += dy

def update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT, select_mode):
    # Screen
    screen.fill((255, 255, 255))
    # Polyline
    draw_poly(screen, points, seg)
    # Nodes
    for key in liste_cerlces:
        pygame.draw.circle(screen, color=(255, 0, 0), center=points[key], radius=max(min(4, min(WIDTH, HEIGHT)* 0.009),1.75))
    # Toolbar
    pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(0, 0, WIDTH, 0.05 * HEIGHT))
    # Buttons
    if select_mode:
        pygame.draw.circle(screen, color=(255, 0, 0), center=(WIDTH*0.05, HEIGHT*0.05/2), radius=HEIGHT*0.04/2)
        pygame.draw.circle(screen, color=(0, 50, 0), center=(WIDTH*0.11, HEIGHT*0.05/2), radius=HEIGHT*0.04/2)
    else:
        pygame.draw.circle(screen, color=(50, 0, 0), center=(WIDTH*0.05, HEIGHT*0.05/2), radius=HEIGHT*0.04/2)
        pygame.draw.circle(screen, color=(0, 255, 0), center=(WIDTH*0.11, HEIGHT*0.05/2), radius=HEIGHT*0.04/2)

def main_interface(points, seg, WIDTH=750, HEIGHT=750):
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    # Faire une copie et repartir de la copie à chaque rescale.
    points = to_pygame(points, WIDTH, HEIGHT)
    copy_points = deepcopy(points)
    points = redimension(points, WIDTH, HEIGHT)
    save_points = deepcopy(points)

    screen.fill((255, 255, 255))
    draw_poly(screen, points, seg)    

    pos = None
    mousedrag = False
    mouse_down = False
    select_mode = True
    liste_cerlces = []

    update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT, select_mode)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                if event.key == pygame.K_s:
                    select_mode = not select_mode
                    update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT, select_mode)
                if event.key == pygame.K_z and mods & pygame.KMOD_CTRL:
                    points = deepcopy(save_points)
                    update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT, select_mode)
                if event.key == pygame.K_a:
                    if mods & pygame.KMOD_CTRL and mods & pygame.KMOD_SHIFT:
                        liste_cerlces = []
                        update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT, select_mode)
                    elif mods & pygame.KMOD_CTRL:
                        liste_cerlces = list(points.keys())
                        update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT, select_mode)
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = screen.get_size()
                points = deepcopy(copy_points)
                points = redimension(points, WIDTH, HEIGHT)
                update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT, select_mode)
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                last_pos = pos
                if pos[1] > HEIGHT * 0.05:
                    save_points = deepcopy(points)
                    mouse_down = True
                elif WIDTH*0.05 - HEIGHT*0.04/2 <= pos[0] <= WIDTH*0.05 + HEIGHT*0.04/2 or WIDTH*0.11 - HEIGHT*0.04/2 <= pos[0] <= WIDTH*0.11 + HEIGHT*0.04/2:
                    select_mode = not select_mode
                    update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT, select_mode)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos2 = pygame.mouse.get_pos()
                if mouse_down and select_mode:
                    liste_cerlces = select(points, pos, pos2)
                    mouse_down = False
                    mousedrag = False
                    update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT, select_mode)
                elif mouse_down and not select_mode:
                    mouse_down = False
                    mousedrag = False
            if event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    actu_pos = pygame.mouse.get_pos()
                    mousedrag = True
        if mousedrag and select_mode:
            update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT, select_mode)
            mouseRectCorners = [pos, [pos[0], actu_pos[1]], actu_pos, [actu_pos[0], pos[1]]]
            pygame.draw.lines(screen, color=(0, 0, 255), closed=True, points=mouseRectCorners, width=1)
        elif mousedrag and not select_mode:
            move(points, liste_cerlces, last_pos, actu_pos)
            update(screen, points, seg, liste_cerlces, WIDTH, HEIGHT, select_mode)
            last_pos = actu_pos
        pygame.display.update()


        # https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/
        