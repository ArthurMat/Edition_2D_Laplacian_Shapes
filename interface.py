#!/usr/bin/env python3

import sys
import pygame
from pygame import color
from tools import *
from copy import deepcopy

def draw_poly(screen, points, seg):
    for key, value in seg.items():
        pygame.draw.line(screen, color=(0, 0, 0), start_pos=points[value[0]], end_pos=points[value[1]], width=2)

def draw_points(screen, data):
    for key, value in data.points.items():
        pygame.draw.circle(screen, color=(0, 0, 0), center=value, radius=max(min(4, min(data.WIDTH, data.HEIGHT)* 0.009),1.75))

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

def reset_button(screen, WIDTH, HEIGHT):
    pi = 3.14159265359
    rec = pygame.Rect(WIDTH*0.95 - HEIGHT*0.012, HEIGHT*0.012, HEIGHT*0.025, HEIGHT*0.025)
    pygame.draw.circle(screen, color=(128, 0, 0), center=(WIDTH*0.95, HEIGHT*0.05/2), radius=HEIGHT*0.02)
    pygame.draw.arc(screen, color=(255, 255, 255), rect=rec, start_angle=pi, stop_angle=pi/2, width=3)

def s(screen, WIDTH, HEIGHT, white):
    if white:
        color = (255, 255, 255)
    else:
        color = (0, 0, 0)
    pi = 3.14159265359
    rec = pygame.Rect(WIDTH*0.05-HEIGHT*0.0125,HEIGHT*0.0125, HEIGHT*0.025, HEIGHT*0.0175)
    rec2 = pygame.Rect(WIDTH*0.05-HEIGHT*0.0125,HEIGHT*0.025, HEIGHT*0.025, HEIGHT*0.0175)
    pygame.draw.arc(screen, color, rect=rec, start_angle=pi/3, stop_angle=3*pi/2, width=3)
    pygame.draw.arc(screen, color, rect=rec2, start_angle=4*pi/3, stop_angle=pi/2, width=3)

def m(screen, WIDTH, HEIGHT, white):
    if white:
        color = (255, 255, 255)
    else:
        color = (0, 0, 0)
    points=[[WIDTH*0.11-HEIGHT*0.011, HEIGHT*0.032], [WIDTH*0.11-HEIGHT*0.011, HEIGHT*0.013], [WIDTH*0.11, HEIGHT*0.025], [WIDTH*0.11+HEIGHT*0.011, HEIGHT*0.013], [WIDTH*0.11+HEIGHT*0.011, HEIGHT*0.032]]
    pygame.draw.lines(screen, color, closed=False, points=points, width=3)

def add_remove(screen, data, ar_mode):
    p=[[data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.005],
       [data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.045],
       [data.WIDTH*0.45 + data.HEIGHT*0.1, data.HEIGHT*0.045],
       [data.WIDTH*0.45 + data.HEIGHT*0.1, data.HEIGHT*0.005]]
    if not ar_mode[0]:
        pygame.draw.circle(screen, color=(0, 0, 50), center=(data.WIDTH*0.45, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.rect(screen, color=(100, 100, 100), rect=pygame.Rect(data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.005, data.HEIGHT*0.06, data.HEIGHT*0.04))
        pygame.draw.lines(screen, color=(0, 0, 0), closed=True, points=p, width=2)
    else:
        pygame.draw.circle(screen, color=(0, 0, 200), center=(data.WIDTH*0.45, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.rect(screen, color=(200, 200, 200), rect=pygame.Rect(data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.005, data.HEIGHT*0.06, data.HEIGHT*0.04))
        pygame.draw.lines(screen, color=(0, 0, 0), closed=True, points=p, width=2)
        pygame.draw.rect(screen,color=(220, 220, 220), rect=pygame.Rect(data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.005, data.HEIGHT*0.03, data.HEIGHT*0.04))
        pygame.draw.lines(screen, color=(0, 0, 0), closed=True, points=[[data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.005], [data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.045], [data.WIDTH*0.45 + data.HEIGHT*0.14, data.HEIGHT*0.045], [data.WIDTH*0.45 + data.HEIGHT*0.14, data.HEIGHT*0.005]], width=2)
        pygame.draw.rect(screen, color=(255, 255, 255), rect=pygame.Rect(data.WIDTH*0.45-data.HEIGHT*0.015, data.HEIGHT*0.0225, data.HEIGHT*0.03, data.HEIGHT*0.005))
        pygame.draw.polygon(screen, color=(0, 0, 0), points=[[data.WIDTH*0.45 + data.HEIGHT*0.115, data.HEIGHT*0.02], [data.WIDTH*0.45 + data.HEIGHT*0.135, data.HEIGHT*0.02], [data.WIDTH*0.45 + data.HEIGHT*0.125, data.HEIGHT*0.01]])
        pygame.draw.polygon(screen, color=(0, 0, 0), points=[[data.WIDTH*0.45 + data.HEIGHT*0.115, data.HEIGHT*0.03], [data.WIDTH*0.45 + data.HEIGHT*0.135, data.HEIGHT*0.03], [data.WIDTH*0.45 + data.HEIGHT*0.125, data.HEIGHT*0.04]])
        if data.add:
            pygame.draw.rect(screen, color=(255, 255, 255), rect=pygame.Rect(data.WIDTH*0.45-data.HEIGHT*0.0025, data.HEIGHT*0.01, data.HEIGHT*0.005, data.HEIGHT*0.03))
        else:
            pygame.draw.circle(screen, color=(200, 0, 0), center=(data.WIDTH*0.45 - data.HEIGHT*0.04, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.015)
            pygame.draw.rect(screen, color=(255, 255, 255), rect=pygame.Rect(data.WIDTH*0.45-data.HEIGHT*0.051, data.HEIGHT*0.0225, data.HEIGHT*0.02, data.HEIGHT*0.005))
        if ar_mode[1]:
            pygame.draw.line(screen, color=(0, 0, 0), start_pos=[data.WIDTH*0.45 + data.HEIGHT*0.05, data.HEIGHT*0.025], end_pos=[data.WIDTH*0.45 + data.HEIGHT*0.09, data.HEIGHT*0.025], width=3)
        else:
            pygame.draw.circle(screen, color=(0, 0, 0), center=(data.WIDTH*0.45 + data.HEIGHT*0.07, data.HEIGHT*0.025), radius=data.HEIGHT*0.015)

def update(screen, data, select_mode, ar_mode):
    # Screen
    screen.fill((255, 255, 255))
    # Polyline
    draw_poly(screen, data.points, data.seg)
    # Toolbar
    pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(0, 0, data.WIDTH, 0.05 * data.HEIGHT))
    # Buttons
    if ar_mode[0]:
        draw_points(screen, data)
        add_remove(screen, data, ar_mode)
        pygame.draw.circle(screen, color=(50, 0, 0), center=(data.WIDTH*0.05, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.circle(screen, color=(0, 50, 0), center=(data.WIDTH*0.11, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        s(screen, data.WIDTH, data.HEIGHT, 0)
        m(screen, data.WIDTH, data.HEIGHT, 0)
    else:
        add_remove(screen, data, ar_mode)
        if select_mode:
            pygame.draw.circle(screen, color=(255, 0, 0), center=(data.WIDTH*0.05, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
            pygame.draw.circle(screen, color=(0, 50, 0), center=(data.WIDTH*0.11, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
            s(screen, data.WIDTH, data.HEIGHT, 1)
            m(screen, data.WIDTH, data.HEIGHT, 0)
        else:
            pygame.draw.circle(screen, color=(50, 0, 0), center=(data.WIDTH*0.05, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
            pygame.draw.circle(screen, color=(0, 255, 0), center=(data.WIDTH*0.11, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
            s(screen, data.WIDTH, data.HEIGHT, 0)
            m(screen, data.WIDTH, data.HEIGHT, 1)
    if data.load:
        pygame.draw.circle(screen, color=(200, 100, 0), center=(data.WIDTH*0.75, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.circle(screen, color=(50, 25, 0), center=(data.WIDTH*0.75 + data.HEIGHT*0.06, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
    else:
        pygame.draw.circle(screen, color=(50, 25, 0), center=(data.WIDTH*0.75, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.circle(screen, color=(200, 100, 0), center=(data.WIDTH*0.75 + data.HEIGHT*0.06, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
    reset_button(screen, data.WIDTH, data.HEIGHT)
    # Nodes
    for key in data.liste_cercles:
        pygame.draw.circle(screen, color=(255, 0, 0), center=data.points[key], radius=max(min(4, min(data.WIDTH, data.HEIGHT)* 0.009),1.75))


def main_interface(data, WIDTH=750, HEIGHT=750):
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("2D Laplacian Editor")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    # Faire une copie et repartir de la copie à chaque rescale.
    data.WIDTH, data.HEIGHT = WIDTH, HEIGHT
    data.transform()
    data.redim()
    data.points, data.seg = deepcopy(data.mesh_points), deepcopy(data.mesh_seg)
    data.switch()

    screen.fill((255, 255, 255))
    draw_poly(screen, data.points, data.seg)    

    pos = None
    mousedrag = False
    mouse_down = False
    select_mode = True
    ar_mode = [False, False]  # [add/remove mode (decide by data.add), False=Point / True=Seg]

    update(screen, data, select_mode, ar_mode)
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
                if event.key == pygame.K_z and mods & pygame.KMOD_CTRL:
                    if len(data.save_points) > 0:
                        data.points = deepcopy(data.save_points[-1])
                        data.save_points.pop(-1)
                if event.key == pygame.K_a:
                    if mods & pygame.KMOD_CTRL and mods & pygame.KMOD_SHIFT:
                        data.liste_cercles = []
                    elif mods & pygame.KMOD_CTRL:
                        data.liste_cercles = list(data.points.keys())
                update(screen, data, select_mode, ar_mode)
            if event.type == pygame.VIDEORESIZE:
                data.WIDTH, data.HEIGHT = screen.get_size()
                data.points = deepcopy(data.copy_points)
                data.redim()
                redimension(data.points, data.WIDTH, data.HEIGHT)
                update(screen, data, select_mode, ar_mode)
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                last_pos = pos
                if pos[1] > HEIGHT * 0.05:
                    mouse_down = True
                    if ar_mode[0]:
                        if not data.add:
                            select_mode = True
                        if not ar_mode[1] and data.add:
                            select_mode = False
                            k = len(data.points.keys())
                            data.points[k+1] = [pos[0], pos[1]]
                    elif not select_mode:
                        data.save_points.append(deepcopy(data.points))
                elif ar_mode[0] and not ar_mode[1] and not data.add and data.WIDTH*0.45 - data.HEIGHT*0.04 - data.HEIGHT*0.015/2 <= pos[0] <= data.WIDTH*0.45 - data.HEIGHT*0.04 + data.HEIGHT*0.015/2:
                    data.suppression()
                elif data.WIDTH*0.05 - data.HEIGHT*0.02 <= pos[0] <= data.WIDTH*0.05 + data.HEIGHT*0.02 or data.WIDTH*0.11 - data.HEIGHT*0.02 <= pos[0] <= data.WIDTH*0.11 + data.HEIGHT*0.02:
                    select_mode = not select_mode
                    ar_mode[0]= False
                elif data.WIDTH*0.45 - data.HEIGHT*0.02 <= pos[0] <= data.WIDTH*0.45 + data.HEIGHT*0.02:
                    ar_mode[0] = True
                    data.add = not data.add
                elif data.WIDTH*0.45 + data.HEIGHT*0.11 <= pos[0] <= data.WIDTH*0.45 + data.HEIGHT*0.14 and ar_mode[0]:
                    ar_mode[1] = not ar_mode[1]
                elif data.WIDTH*0.75 - data.HEIGHT*0.02 <= pos[0] <= data.WIDTH*0.75 + data.HEIGHT*0.02 or data.WIDTH*0.75 + data.HEIGHT*0.04 <= pos[0] <= data.WIDTH*0.75 + data.HEIGHT*0.08:
                    data.switch()
                    ar_mode[0] = False
                elif data.WIDTH*0.95 - data.HEIGHT*0.012 <= pos[0] <= data.WIDTH*0.95 + data.HEIGHT*0.012:
                    data.WIDTH, data.HEIGHT = screen.get_size()
                    data.reset()
                update(screen, data, select_mode, ar_mode)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos2 = pygame.mouse.get_pos()
                if mouse_down and select_mode:
                    data.liste_cercles = select(data.points, pos, pos2)
                    mouse_down = False
                    mousedrag = False
                    update(screen, data, select_mode, ar_mode)
                elif mouse_down and not select_mode:
                    mouse_down = False
                    mousedrag = False
            if event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    actu_pos = pygame.mouse.get_pos()
                    mousedrag = True
        if mousedrag and select_mode:
            update(screen, data, select_mode, ar_mode)
            mouseRectCorners = [pos, [pos[0], actu_pos[1]], actu_pos, [actu_pos[0], pos[1]]]
            pygame.draw.lines(screen, color=(0, 0, 255), closed=True, points=mouseRectCorners, width=1)
        elif mousedrag and not select_mode:
            move(data.points, data.liste_cercles, last_pos, actu_pos)
            update(screen, data, select_mode, ar_mode)
            last_pos = actu_pos
        pygame.display.update()


        # https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/
        