#!/usr/bin/env python3

import sys
import pygame
from tools import *
from copy import deepcopy
from constant import *

def draw_poly(screen, points, seg, item, seg_proche):
    for key, value in seg.items():
        if item and key == seg_proche:
            pygame.draw.line(screen, color=RED, start_pos=points[value[0]], end_pos=points[value[1]], width=2)
        else:
            pygame.draw.line(screen, color=BLACK, start_pos=points[value[0]], end_pos=points[value[1]], width=2)

def draw_points(screen, data):
    for key, value in data.points.items():
        pygame.draw.circle(screen, color=BLACK, center=value, radius=max(min(4, min(data.WIDTH, data.HEIGHT)* 0.009),1.75))

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
    pygame.draw.circle(screen, color=DARK_RED, center=(WIDTH*0.95, HEIGHT*0.05/2), radius=HEIGHT*0.02)
    pygame.draw.arc(screen, color=WHITE, rect=rec, start_angle=pi, stop_angle=pi/2, width=3)

def s(screen, WIDTH, HEIGHT, white):
    if white:
        color = WHITE
    else:
        color = BLACK
    pi = 3.14159265359
    rec = pygame.Rect(WIDTH*0.05-HEIGHT*0.0125,HEIGHT*0.0125, HEIGHT*0.025, HEIGHT*0.0175)
    rec2 = pygame.Rect(WIDTH*0.05-HEIGHT*0.0125,HEIGHT*0.025, HEIGHT*0.025, HEIGHT*0.0175)
    pygame.draw.arc(screen, color, rect=rec, start_angle=pi/3, stop_angle=3*pi/2, width=3)
    pygame.draw.arc(screen, color, rect=rec2, start_angle=4*pi/3, stop_angle=pi/2, width=3)

def m(screen, WIDTH, HEIGHT, white):
    if white:
        color = WHITE
    else:
        color = BLACK
    points=[[WIDTH*0.11-HEIGHT*0.011, HEIGHT*0.032], [WIDTH*0.11-HEIGHT*0.011, HEIGHT*0.013], [WIDTH*0.11, HEIGHT*0.025], [WIDTH*0.11+HEIGHT*0.011, HEIGHT*0.013], [WIDTH*0.11+HEIGHT*0.011, HEIGHT*0.032]]
    pygame.draw.lines(screen, color, closed=False, points=points, width=3)

def add_remove(screen, data, mode, item):
    p=[[data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.005],
       [data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.045],
       [data.WIDTH*0.45 + data.HEIGHT*0.1, data.HEIGHT*0.045],
       [data.WIDTH*0.45 + data.HEIGHT*0.1, data.HEIGHT*0.005]]
    if mode < 2:
        pygame.draw.circle(screen, color=BLUE_OFF, center=(data.WIDTH*0.45, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.rect(screen, color=GRAY_OFF, rect=pygame.Rect(data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.005, data.HEIGHT*0.06, data.HEIGHT*0.04))
        pygame.draw.lines(screen, color=BLACK, closed=True, points=p, width=2)
    else:
        pygame.draw.circle(screen, color=LIGHT_BLUE, center=(data.WIDTH*0.45, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.rect(screen, color=LIGHT_GRAY, rect=pygame.Rect(data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.005, data.HEIGHT*0.06, data.HEIGHT*0.04))
        pygame.draw.lines(screen, color=BLACK, closed=True, points=p, width=2)
        pygame.draw.rect(screen,color=VERY_LIGHT_GRAY, rect=pygame.Rect(data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.005, data.HEIGHT*0.03, data.HEIGHT*0.04))
        pygame.draw.lines(screen, color=BLACK, closed=True, points=[[data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.005], [data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.045], [data.WIDTH*0.45 + data.HEIGHT*0.14, data.HEIGHT*0.045], [data.WIDTH*0.45 + data.HEIGHT*0.14, data.HEIGHT*0.005]], width=2)
        pygame.draw.rect(screen, color=WHITE, rect=pygame.Rect(data.WIDTH*0.45-data.HEIGHT*0.015, data.HEIGHT*0.0225, data.HEIGHT*0.03, data.HEIGHT*0.005))
        pygame.draw.polygon(screen, color=BLACK, points=[[data.WIDTH*0.45 + data.HEIGHT*0.115, data.HEIGHT*0.02], [data.WIDTH*0.45 + data.HEIGHT*0.135, data.HEIGHT*0.02], [data.WIDTH*0.45 + data.HEIGHT*0.125, data.HEIGHT*0.01]])
        pygame.draw.polygon(screen, color=BLACK, points=[[data.WIDTH*0.45 + data.HEIGHT*0.115, data.HEIGHT*0.03], [data.WIDTH*0.45 + data.HEIGHT*0.135, data.HEIGHT*0.03], [data.WIDTH*0.45 + data.HEIGHT*0.125, data.HEIGHT*0.04]])
        if mode == 3:  # mode ajout
            pygame.draw.rect(screen, color=WHITE, rect=pygame.Rect(data.WIDTH*0.45-data.HEIGHT*0.0025, data.HEIGHT*0.01, data.HEIGHT*0.005, data.HEIGHT*0.03))
        else:  # mode suppression
            pygame.draw.circle(screen, color=LIGHT_RED, center=(data.WIDTH*0.45 - data.HEIGHT*0.04, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.015)
            pygame.draw.rect(screen, color=WHITE, rect=pygame.Rect(data.WIDTH*0.45-data.HEIGHT*0.051, data.HEIGHT*0.0225, data.HEIGHT*0.02, data.HEIGHT*0.005))
        if item:  # segment
            pygame.draw.line(screen, color=BLACK, start_pos=[data.WIDTH*0.45 + data.HEIGHT*0.05, data.HEIGHT*0.025], end_pos=[data.WIDTH*0.45 + data.HEIGHT*0.09, data.HEIGHT*0.025], width=3)
        else:  # point
            pygame.draw.circle(screen, color=BLACK, center=(data.WIDTH*0.45 + data.HEIGHT*0.07, data.HEIGHT*0.025), radius=data.HEIGHT*0.015)

def update(screen, data, mode, item, seg_proche):
    # Screen
    screen.fill(WHITE)
    # Polyline
    draw_poly(screen, data.points, data.seg, item, seg_proche)
    # Toolbar
    pygame.draw.rect(screen, GRAY, pygame.Rect(0, 0, data.WIDTH, 0.05 * data.HEIGHT))
    add_remove(screen, data, mode, item)
    # Buttons
    if mode > 1:
        draw_points(screen, data)
        pygame.draw.circle(screen, color=RED_OFF, center=(data.WIDTH*0.05, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.circle(screen, color=GREEN_OFF, center=(data.WIDTH*0.11, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        s(screen, data.WIDTH, data.HEIGHT, 0)
        m(screen, data.WIDTH, data.HEIGHT, 0)
    elif mode == 0:
        pygame.draw.circle(screen, color=RED, center=(data.WIDTH*0.05, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.circle(screen, color=GREEN_OFF, center=(data.WIDTH*0.11, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        s(screen, data.WIDTH, data.HEIGHT, 1)
        m(screen, data.WIDTH, data.HEIGHT, 0)
    elif mode == 1:
        pygame.draw.circle(screen, color=RED_OFF, center=(data.WIDTH*0.05, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.circle(screen, color=GREEN, center=(data.WIDTH*0.11, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        s(screen, data.WIDTH, data.HEIGHT, 0)
        m(screen, data.WIDTH, data.HEIGHT, 1)
    if data.load:
        pygame.draw.circle(screen, color=ORANGE, center=(data.WIDTH*0.75, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.circle(screen, color=ORANGE_OFF, center=(data.WIDTH*0.75 + data.HEIGHT*0.06, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
    else:
        pygame.draw.circle(screen, color=ORANGE_OFF, center=(data.WIDTH*0.75, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.circle(screen, color=ORANGE, center=(data.WIDTH*0.75 + data.HEIGHT*0.06, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
    reset_button(screen, data.WIDTH, data.HEIGHT)
    # Nodes
    for key in data.liste_cercles:
        pygame.draw.circle(screen, color=RED, center=data.points[key], radius=max(min(4, min(data.WIDTH, data.HEIGHT)* 0.009),1.75))


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

    screen.fill(WHITE)

    pos = None
    mousedrag = False
    mouse_down = False
    seg_proche = None
    
    mode = 0      # 0=select, 1=move, 2=suppr, 3=add
    item = False  # False=Point / True=Seg

    update(screen, data, mode, item, seg_proche)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            
            """"Event Quit"""
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            """Event Key Down"""
            if event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                if event.key == pygame.K_s:
                    mode = (mode + 1) % 3
                if event.key == pygame.K_z and mods & pygame.KMOD_CTRL:
                    if len(data.save_points) > 0:
                        data.points = deepcopy(data.save_points[-1][0])
                        data.seg = deepcopy(data.save_points[-1][1])
                        data.save_points.pop(-1)
                if event.key == pygame.K_a:
                    if mods & pygame.KMOD_CTRL and mods & pygame.KMOD_SHIFT:
                        data.liste_cercles = []
                    elif mods & pygame.KMOD_CTRL:
                        data.liste_cercles = list(data.points.keys())
                update(screen, data, mode, item, seg_proche)
                
            """Event Resize Window"""
            if event.type == pygame.VIDEORESIZE:
                data.WIDTH, data.HEIGHT = screen.get_size()
                data.points = deepcopy(data.copy_points)
                data.redim()
                redimension(data.points, data.WIDTH, data.HEIGHT)
                update(screen, data, mode, item, seg_proche)
                pygame.display.update()
            
            """"Event MouseButton Down"""
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                last_pos = pos
                # Object Event
                if pos[1] > HEIGHT * 0.05:
                    mouse_down = True
                    if mode != 0:
                        data.save_points.append([deepcopy(data.points), deepcopy(data.seg)])
                    if mode != 2:
                        seg_proche = None
                    if mode == 2 and item:
                        data.liste_cercles = []
                        seg_proche = nearest_seg(data.points, data.seg, pos)
                        update(screen, data, mode, item, seg_proche)
                    elif mode == 3:  # Ajout
                        if item:  # Segment
                            data.liste_cercles = [find_nearest(data.points, pos)]
                        else:  # Point
                            k = len(data.points.keys())
                            data.points[k+1] = [pos[0], pos[1]]
                        update(screen, data, mode, item, seg_proche)
                # Toolbar Event
                else:
                    if data.WIDTH*0.05 - data.HEIGHT*0.02 <= pos[0] <= data.WIDTH*0.05 + data.HEIGHT*0.02:  # Red Button Select
                        mode = 0  # mode selection
                        item = False
                    elif data.WIDTH*0.11 - data.HEIGHT*0.02 <= pos[0] <= data.WIDTH*0.11 + data.HEIGHT*0.02:  # Green Button Move
                        mode = 1  # mode deplacement
                    elif data.WIDTH*0.45 - data.HEIGHT*0.02 <= pos[0] <= data.WIDTH*0.45 + data.HEIGHT*0.02:  # Blue Button Add/Remove
                        if mode != 2:
                            mode = 2  # mode suppression
                        else:
                            mode = 3  # mode ajout
                        data.liste_cercles = []
                    elif mode > 1 and data.WIDTH*0.45 - data.HEIGHT*0.04 - data.HEIGHT*0.015/2 <= pos[0] <= data.WIDTH*0.45 - data.HEIGHT*0.04 + data.HEIGHT*0.015/2:  # Red Button Suppr
                        if not item:  # Point
                            data.suppression()
                        else:  # Segment
                            data.suppr_seg(seg_proche)
                            seg_proche = None
                    elif mode > 1 and data.WIDTH*0.45 + data.HEIGHT*0.11 <= pos[0] <= data.WIDTH*0.45 + data.HEIGHT*0.14:  # Gray Selector Point/Segment
                        item = not item
                    elif data.WIDTH*0.75 - data.HEIGHT*0.02 <= pos[0] <= data.WIDTH*0.75 + data.HEIGHT*0.02 or data.WIDTH*0.75 + data.HEIGHT*0.04 <= pos[0] <= data.WIDTH*0.75 + data.HEIGHT*0.08:  # Orange Buttons Mesh
                        data.switch()
                    elif data.WIDTH*0.95 - data.HEIGHT*0.012 <= pos[0] <= data.WIDTH*0.95 + data.HEIGHT*0.012:  # Red Button Reset
                        data.WIDTH, data.HEIGHT = screen.get_size()
                        data.reset()
                    update(screen, data, mode, item, seg_proche)
                    
            """Event MouseButton Up"""
            if event.type == pygame.MOUSEBUTTONUP:
                pos2 = pygame.mouse.get_pos()
                if mouse_down and (mode % 2) == 0 and not item:
                    data.liste_cercles = select(data.points, pos, pos2)
                elif mouse_down and mode == 3 and item:
                    nearest = find_nearest(data.points, actu_pos)
                    if [data.liste_cercles[0], nearest] not in data.seg.values():
                        k = len(data.seg.keys())
                        data.seg[k+1] = [data.liste_cercles[0], nearest]
                    data.liste_cercles = []
                update(screen, data, mode, item, seg_proche)
                mousedrag = False
                mouse_down = False
                
            """Event Mouse Motion"""
            if event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    actu_pos = pygame.mouse.get_pos()
                    mousedrag = True
        
        """Selection Box"""
        if mousedrag and (mode % 2) == 0:
            update(screen, data, mode, item, seg_proche)
            mouseRectCorners = [pos, [pos[0], actu_pos[1]], actu_pos, [actu_pos[0], pos[1]]]
            pygame.draw.lines(screen, color=BLUE, closed=True, points=mouseRectCorners, width=1)
        
        """Segment Drawing"""
        if mousedrag and mode == 3 and item:
            update(screen , data, mode, item, seg_proche)
            nearest = find_nearest(data.points, actu_pos)
            pygame.draw.line(screen, color=DARK_GREEN, start_pos=data.points[data.liste_cercles[0]], end_pos=actu_pos, width=2)
            pygame.draw.circle(screen, color=GREEN, center=data.points[data.liste_cercles[0]], radius=max(min(4, min(data.WIDTH, data.HEIGHT) * 0.009), 1.75))
            pygame.draw.circle(screen, color=GREEN, center=data.points[nearest], radius=max(min(4, min(data.WIDTH, data.HEIGHT) * 0.009), 1.75))
        
        """Mooving Points"""
        if mousedrag and mode == 1:
            move(data.points, data.liste_cercles, last_pos, actu_pos)
            update(screen, data, mode, item, seg_proche)
            last_pos = actu_pos
        
        
        pygame.display.update()


        # https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/
        