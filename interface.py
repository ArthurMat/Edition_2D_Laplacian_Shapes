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

    screen.fill(WHITE[data.day])

    pos = None
    mousedrag = False
    mouse_down = False
    seg_proche = None
    
    mode = 0      # 0=select, 1=move, 2=suppr, 3=add
    item = False  # False=Point / True=Seg  or  False=handle / True=fix

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
                if event.key == pygame.K_p:
                    data.update_keys()
                if event.key == pygame.K_n:
                    data.day = (data.day + 1) % 2
                if (event.key == pygame.K_UP or event.key == pygame.K_DOWN) and mode != 1:
                    item = not item
                if (event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE) and mode == 2:
                    if not item:  # Point
                        data.suppression()
                    else:  # Segment
                        data.suppr_seg(seg_proche)
                        seg_proche = None
                if event.key == pygame.K_z and mods & pygame.KMOD_CTRL:
                    if len(data.save_points) > 0:
                        data.points = deepcopy(data.save_points[-1][0])
                        data.seg = deepcopy(data.save_points[-1][1])
                        data.save_points.pop(-1)
                if event.key == pygame.K_a:
                    if mods & pygame.KMOD_CTRL and mods & pygame.KMOD_SHIFT:
                        if item:
                            data.fixes = []
                        else:
                            data.handles = []
                    elif mods & pygame.KMOD_CTRL:
                        if item:
                            for key in data.points.key():
                                if key not in data.handles:
                                    data.fixes.append(key)
                        else:
                            for key in data.points.key():
                                if key not in data.fixes:
                                    data.handles.append(key)
                if event.key == pygame.K_r and mods & pygame.KMOD_CTRL:
                    data.WIDTH, data.HEIGHT = screen.get_size()
                    data.reset()
                if event.key == pygame.K_s:
                    if mods & pygame.KMOD_CTRL:
                        file = open("test/new_file.poly", "w")
                        file.write(write_file(data))
                        file.close()
                    else:
                        if mode == 3:
                            mode -= 1
                        mode = (mode + 1) % 3
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
                        data.handles = []
                        data.fixes = []
                        seg_proche = nearest_seg(data.points, data.seg, pos)
                        update(screen, data, mode, item, seg_proche)
                    elif mode == 3:  # Ajout
                        if item:  # Segment
                            data.handles = [find_nearest(data.points, pos)]
                        else:  # Point
                            data.indice_point +=1
                            data.points[data.indice_point] = [pos[0], pos[1]]
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
                        data.handles = []
                        data.fixes = []
                    elif mode > 1 and data.WIDTH*0.45 - data.HEIGHT*0.04 - data.HEIGHT*0.015/2 <= pos[0] <= data.WIDTH*0.45 - data.HEIGHT*0.04 + data.HEIGHT*0.015/2:  # Red Button Suppr
                        if not item:  # Point
                            data.suppression()
                        else:  # Segment
                            data.suppr_seg(seg_proche)
                            seg_proche = None
                    elif mode != 1 and data.WIDTH*0.45 + data.HEIGHT*0.11 <= pos[0] <= data.WIDTH*0.45 + data.HEIGHT*0.14:  # Gray Selector Point/Segment
                        item = not item
                    elif data.WIDTH*0.95 - data.HEIGHT*0.012 <= pos[0] <= data.WIDTH*0.95 + data.HEIGHT*0.012:  # Red Button Reset
                        data.WIDTH, data.HEIGHT = screen.get_size()
                        data.reset()
                    update(screen, data, mode, item, seg_proche)
                    
            """Event MouseButton Up"""
            if event.type == pygame.MOUSEBUTTONUP:
                pos2 = pygame.mouse.get_pos()
                if mouse_down and (mode % 2) == 0 and not item:
                    l = select(data.points, pos, pos2)
                    for i in range(len(l)):
                        if l[i] in data.fixes:
                            l.pop(i)
                    data.handles = l
                if mouse_down and mode == 0 and item:  # Warning to not select points that are already selected in the other list or you will select nothing
                    l = select(data.points, pos, pos2)
                    for i in range(len(l)):
                        if l[i] in data.handles:
                            l.pop(i)
                    data.fixes = l
                elif mouse_down and mode == 3 and item:
                    nearest = find_nearest(data.points, pos2)
                    if [data.handles[0], nearest] not in data.seg.values() and data.handles[0] != nearest:
                        data.indice_seg +=1
                        data.seg[data.indice_seg] = [data.handles[0], nearest]
                    data.handles = []
                elif mouse_down and mode == 1:
                    if len(data.handles) > 0:
                        handles = deepcopy(data.handles)
                        if len(data.fixes) == 0:
                            handles.append(find_farest(data.points, data.handles))
                        else:
                            handles += deepcopy(data.fixes)
                        old_coords = list()
                        for k in handles:
                            old_coords.append(data.points[k])
                        arr = move2(data.save_points[-1][0], data.seg, handles, old_coords)
                        data.points = array_to_dict(arr)
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
            pygame.draw.line(screen, color=DARK_GREEN, start_pos=data.points[data.handles[0]], end_pos=actu_pos, width=2)
            pygame.draw.circle(screen, color=GREEN, center=data.points[data.handles[0]], radius=max(min(4, min(data.WIDTH, data.HEIGHT) * 0.009), 1.75))
            pygame.draw.circle(screen, color=GREEN, center=data.points[nearest], radius=max(min(4, min(data.WIDTH, data.HEIGHT) * 0.009), 1.75))
        
        """Mooving Points"""
        if mousedrag and mode == 1:
            move(data.points, data.handles, last_pos, actu_pos)
            update(screen, data, mode, item, seg_proche)
            last_pos = actu_pos
        
        
        pygame.display.update()


        # https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/
        