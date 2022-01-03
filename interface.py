#!/usr/bin/env python3

import sys
import pygame
from tools import *
from copy import deepcopy
from constant import *
from draw_function import *


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
    # data.points, data.seg = deepcopy(data.mesh_points), deepcopy(data.mesh_seg)
    # data.switch()

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
                        print(data.seg)
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
                    # elif data.WIDTH*0.75 - data.HEIGHT*0.02 <= pos[0] <= data.WIDTH*0.75 + data.HEIGHT*0.02 or data.WIDTH*0.75 + data.HEIGHT*0.04 <= pos[0] <= data.WIDTH*0.75 + data.HEIGHT*0.08:  # Orange Buttons Mesh
                    #     data.switch()
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
                    nearest = find_nearest(data.points, pos2)
                    if [data.liste_cercles[0], nearest] not in data.seg.values():
                        k = len(data.seg.keys())
                        data.seg[k+1] = [data.liste_cercles[0], nearest]
                    data.liste_cercles = []
                elif mouse_down and mode == 1:
                    arr = move2(data.points, data.seg, data.liste_cercles, pos, pos2)
                    data.point = array_to_dict(arr)
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
        