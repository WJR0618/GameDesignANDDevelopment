# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 14:22:13 2019

@author: 王俊儒
"""

import pygame
import time
import random
import math

def create_sea(r,c):
    '''
    create the sea struture. Returns a 2d list
    '''
    grass_img = pygame.image.load('grass.png')
    grass_img = pygame.transform.scale(grass_img, (1000, 1000))
    base.blit(grass_img,(0,0))
    return [['~' for i in range(c)] for j in range(r)]

def draw_sea(board):
    n_row = len(board)
    n_col = len(board[0])
    # print column indices
    print('  ', end='')
    for i in range(n_col):
        print('{:2d} '.format(i), end='')
    print()

    # for each row, print row index first
    for i in range(n_row):
        print(str(i)+' ', end='')
        for j in range(n_col):
            print('{:>2s} '.format(board[i][j]), end='')
        print()

def set_chest(board, n_chest):
    n_row = len(board)
    n_col = len(board[0])
    chests = []
    while len(chests) < n_chest:
        new_chest = (random.randint(0,n_row-1), random.randint(0,n_col-1))
        if new_chest not in chests:
            chests.append(new_chest)
    return chests

def is_on_board(board,r,c):
    n_row = len(board)
    n_col = len(board[0])
    return r >= 0 and c >= 0 and r < n_row and c < n_col

def get_move(board, x, y):
    move = [x,y]                                          #這裡要將user_input換成滑鼠輸入 
    # input must be two numbers and must be on the board
    if is_on_board(board, int(move[0]), int(move[1])):
        print(move)
        return (int(move[0]), int(move[1]))
    #print('invalid input. Please try again.')

def make_move(board,chests,r,c,gold_list):
    if (r,c) in chests:
        # we use '*' to represent a chest
        board[r][c]='*'
        
        grass_img = pygame.image.load('grass.png')
        grass_img = pygame.transform.scale(grass_img, (1000, 1000))
        base.blit(grass_img,(0,0))
        gold_img = pygame.image.load('gold.gif')
        #gold_img = pygame.transform.scale(gold_img, (40, 40))
        gold_list.append((c*100,r*100))
        for ii in gold_list:
            base.blit(gold_img, ii)
        
        chests.remove((r,c))

        return True
    else:
        minD = inf
        # iterate all chests to find minimum distance
        for ch in chests:
            distance = math.sqrt(math.pow(ch[0] - r, 2)+ math.pow(ch[1] - c,2))
            if distance < minD:
                minD = distance
        # only display distances for non chest locations
        if board[r][c] != '*' and minD != inf:  
            board[r][c] = str(round(minD))
            num_img = pygame.image.load(number_img_list[int(minD)-1])
            #gold_img = pygame.transform.scale(gold_img, (40, 40))
            base.blit(num_img,(c*100,r*100))
            
        return False
    
def mouse_pos_into_list_pos( mouse_pos ):
    mx = mouse_pos[0]
    my = mouse_pos[1]
    lx = int(mx/100) #0~9
    ly = int(my/100) #0~7
    #print(str(ly) + '、' + str(lx))
    return ly,lx


def run():
    GAME_FONT1 = pygame.font.SysFont('areal', 52)
    n_sonar = 20
    board = create_sea(8,10)
    draw_sea(board)
    chests = set_chest(board, n_chest)
    previous_moves = []
    gold_list = []
    line_list_x = [0,100,200,300,400,500,600,700,800,900,1000]
    line_list_y = [0,100,200,300,400,500,600,700,800]
    pygame.key.set_repeat(1)
    IS_RUNNING = True
    while IS_RUNNING:     
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                IS_RUNNING = False
                return IS_RUNNING
            if event.type == pygame.MOUSEBUTTONDOWN:
                lx, ly = mouse_pos_into_list_pos(pygame.mouse.get_pos())
                move = get_move(board, lx, ly)
                
                previous_moves.append(move)
                try:
                    hit = make_move(board,chests,move[0],move[1],gold_list)
                    
                    if hit:
                        for (r,c) in previous_moves:
                            # update all placed sonars
                            make_move(board,chests,r,c,gold_list)
                            
                    if len(chests) == 0:
                        print('you found all chests!')
                        end_surf = GAME_FONT1.render('you found all chests!...Game will restart in 2 seconds',True,(255,255,255),(0, 0, 0) )
                        end_rect = end_surf.get_rect(centerx=1002/2,centery = 802/2)
                        base.blit(end_surf, end_rect )
                        pygame.display.update()
                        time.sleep(2)
                        IS_RUNNING = False
                        break
                    if n_sonar == 0:
                        print('you spent all sonars!')
                        end_surf = GAME_FONT1.render('you spent all sonars!...Game will restart in 2 seconds',True,(255,255,255),(0, 0, 0) )
                        end_rect = end_surf.get_rect(centerx=1002/2,centery = 802/2)
                        base.blit(end_surf, end_rect )
                        pygame.display.update()
                        time.sleep(2)
                        IS_RUNNING = False
                        break
                    draw_sea(board)
                    n_sonar -= 1
                    
                except:
                    pass
                    
        for x in line_list_x:
            pygame.draw.rect(base,(255,255,255),pygame.Rect(x,0,2,800))
        for y in line_list_y: 
            pygame.draw.rect(base,(255,255,255),pygame.Rect(0,y,1000,2))
        pygame.display.update()
    return True

pygame.init()
base = pygame.display.set_mode((1002,802))
base.fill((100, 230, 255))
n_chest = 3
inf = float('inf')
number_img_list = [ '1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png']
bg_img = pygame.image.load('background.png')
bg_img = pygame.transform.scale(bg_img,(1800,1000))
start_btn = pygame.image.load('startBUTTON.jpg')
base.blit( bg_img, (0,0) )
base.blit( start_btn,(350,500) )
pygame.display.update()
RUN = True

while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()
            #print(m_pos)
            if 350 < m_pos[0] and  m_pos[0] < 650 and 500 < m_pos[1] and m_pos[1] < 600:
                RUN = run()
                if RUN == False:
                    break
                base.blit( bg_img, (0,0) )
                base.blit( start_btn,(350,500) )
                pygame.display.update()
        
pygame.quit()  # 退出pygame
