import pygame
import numpy as np
import os, sys, copy
import time
from threading import Timer
dir_path = os.path.dirname(os.path.abspath(__file__))

pygame.init()
pygame.key.set_repeat(1,10)

startb = pygame.image.load(dir_path + '\\start_b.png') 
dance_bg = pygame.image.load(dir_path+'\\danceback.png')
bg = pygame.image.load(dir_path+'\\desert_BG.png')
st_background = pygame.image.load(dir_path+'\\back1.png')
player1 = pygame.image.load(dir_path+'\\dance1.png')
player2 = pygame.image.load(dir_path+'\\dance2.png')
bloodbar = pygame.image.load(dir_path+'\\bloodbar1.png')
floor = pygame.image.load(dir_path+'\\floor.png')
play_button = pygame.image.load(dir_path+'\\play.png')
coin = pygame.image.load(dir_path+'\\coin.png')
obstacle1 = pygame.image.load(dir_path+'\\obstacle1.png')
obstacle2 = pygame.image.load(dir_path+'\\obstacle2.png')
obstacle3 = pygame.image.load(dir_path+'\\obstacle3.png')
bg_top = pygame.image.load(dir_path+'\\bg_top.png')
bg_bottom = pygame.image.load(dir_path+'\\d_back2.png')
transparent = pygame.image.load(dir_path+'\\transparent.png')
ob_trans1 = pygame.image.load(dir_path+'\\ob1_transparent.png')
ob_trans2 = pygame.image.load(dir_path+'\\ob2_transparent.png')
ob_trans2 = pygame.image.load(dir_path+'\\ob2_transparent.png')
jump1 = pygame.image.load(dir_path+'\\one_jump1_1.png')
jump2 = pygame.image.load(dir_path+'\\one_jump2_1.png')
down = pygame.image.load(dir_path+'\\down_1.png')
red = pygame.image.load(dir_path+'\\red.png')
crash1 = pygame.image.load(dir_path+'\\crash1.png')
crash2 = pygame.image.load(dir_path+'\\crash2.png')
die1 = pygame.image.load(dir_path+'\\die1.png')
die2 = pygame.image.load(dir_path+'\\die2.png')
die3 = pygame.image.load(dir_path+'\\die3.png')
slide = pygame.image.load(dir_path+'\\slide_1.png')
bg_result = pygame.image.load(dir_path+'\\result.png')

base = pygame.display.set_mode((800,400))
bg_pos = [0,0]
ob1_pos = [850, 263]
ob2_pos = [850, 230]
ob3_pos = [850, 0]
power_pos = [100,5]
floor_pos = [0,330]
score = 0
money = 0

class Obstacle():
    def __init__(self, obatacle_name, pos):
        if obatacle_name == 'obstacle1':
            self.name = 'obstacle1'
            self.img = pygame.image.load(dir_path+'\\obstacle1.png')
            self.pos = pos
        if obatacle_name == 'obstacle2':
            self.name = 'obstacle2'
            self.img = pygame.image.load(dir_path+'\\obstacle2.png')
            self.pos = pos
        if obatacle_name == 'obstacle3':
            self.name = 'obstacle3'
            self.img = pygame.image.load(dir_path+'\\obstacle3.png')
            self.pos = pos
            
    def get_pos(self):
        return self.pos
        
    def go_right(self, speed):
        self.pos[0] -= speed
        
class Food():
    def __init__(self, food_name, pos):
        if food_name == 'candy':
            self.name = food_name
            self.img = pygame.image.load(dir_path+'\\candy.png')
            self.pos = pos
        if food_name == 'coin':
            self.name = food_name
            self.img = pygame.image.load(dir_path+'\\coin.png')
            self.pos = pos
        if food_name == 'energy':
            self.name = food_name
            self.img = pygame.image.load(dir_path+'\\energy.png')
            self.pos = pos
        if food_name == 'fast':
            self.name = food_name
            self.img = pygame.image.load(dir_path+'\\fast.png')
            self.pos = pos
            
    def get_pos(self):
        return self.pos
        
    def go_right(self, speed):
        self.pos[0] -= speed  
        
class Power():
    def __init__(self):
        self.power = 100
        
    def set_power_bar(self, number):
        self.power = number
    
    def get_power_bar(self):
        return self.power
    
    def power_down(self, bloodbar ,number):
        if self.power > 7:
            self.power -= number
            if self.power < 7:
                self.power = 7
        else:
            return 'game_over'
        pxa = pygame.PixelArray(bloodbar)
        pxa[int(600*(self.power/100)):600,:] = (0,0,0, 0)
        del pxa
    
    def power_up(self, bloodbar ,number):
        if self.power < 100:
            self.power += number
            if self.power > 100:
                self.power = 100

        new_bloodbar = pygame.image.load(dir_path+'\\bloodbar1.png')
        newpxa = pygame.PixelArray(new_bloodbar)
        newpxa[int(600*(self.power/100)):600,:] = (0,0,0, 0)
        pxa = pygame.PixelArray(bloodbar)
        pxa[:,:] = newpxa[:,:]
        del newpxa
        del pxa
        
class Mario():

    def __init__(self):
        self.pos = [200,240] # initial position
        self.dir = 'r' #moving direction
        self.speed = 7  #moving speed
        self.jump_times = 2
        self.super1 = False
        self.super2 = False
        self.protect_time = 0
        self.super_fast_time = 0
        self.state = 'run'
        self.state_time = 0
        self.bool_state = False
        
    def protect(self):
        print('protect')
        self.super1 = True
        self.protect_time = time.time()
        
    def deprotect(self):
        if (time.time() - self.protect_time >= 3) and self.super1 == True :
            print('deeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            self.super1 = False
        
    def super_fast(self):
        self.super1 = True
        self.super2 = True
        self.speed = 14
        self.super_fast_time = time.time()
        self.protect_time = time.time()
        
    def desuper_fast(self):
        if (time.time() - self.super_fast_time >= 3) and self.super2 == True :
            print('deeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            self.speed = 7
            self.super1 = False
            self.super2 = False
            
    def blit_state(self, change_image):
        print(self.state)
        self.bool_state = True
        
        if self.state == 'crash1':
            base.blit(crash1,player1_rect)
        elif self.state == 'crash2':
            base.blit(crash1,player1_rect)
        elif self.state == 'jump1':
            base.blit(jump1,player1_rect)
        elif self.state == 'jump2':
            base.blit(jump1,player1_rect)
        elif self.state == 'slide' and change_image != -1:
            base.blit(slide,(self.pos[0],self.pos[1]+30))
        elif self.state == 'run' and change_image != -1:
            if change_image % 8 >= 1 and change_image % 8 <= 4 :
                base.blit(player1,player1_rect)
            else:
                base.blit(player2,player2_rect)

    def destate(self):
        if (time.time() - self.state_time >= 0.5) and self.state != 'run'\
            and self.state != 'slide':
            print('deeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            self.state = 'run'
            self.bool_state = False
            return True
        return False

    def turbo(self):
        self.speed = 10

    def normal(self):
        self.speed = 5

    def stop(self):
        self.speed = 0

    def get_speed(self):
        return self.speed
    
    def reset_jump_times(self):
        self.jump_times = 2
        
    def slide(self):
        self.state = 'slide'

    def jumpheigher(self):
        print('jump2')
        collision = False
        self.jump_times -= 1
        for i in range(10):
            while self.pos[1] >= 90:  #一段跳100
                go_right(bg_top, foods, obstacles, mario.speed)
                self.pos[1] -= 8
                draw_base()
                player1_rect.topleft = self.pos
                trans_rect.topleft = self.pos
                base.blit(transparent,trans_rect)
                if collide( player1_rect, foods, obstacles ):
                    base.blit(crash1,player1_rect)
                    collision = True
                    self.state = 'crash1'
                    self.state_time = time.time()
                else:   
                    if collision == False:
                        base.blit(jump2,player1_rect)
                    else:
                        base.blit(crash1,player1_rect)
                
                mario.blit_state(-1)
                pygame.display.update()
                
        while self.pos[1] <= 235:  #一段跳100
            go_right(bg_top, foods, obstacles, mario.speed)
            self.pos[1] += 8
            draw_base()
            player1_rect.topleft = self.pos
            trans_rect.topleft = self.pos
            base.blit(transparent,trans_rect)
            if collide( player1_rect, foods, obstacles ):
                base.blit(crash1,player1_rect)
                collision = True
                self.state = 'crash1'
                self.state_time = time.time()
            else:   
                if collision == False:
                    base.blit(jump2,player1_rect)
                else:
                    base.blit(crash1,player1_rect)
            mario.blit_state(-1)
            pygame.display.update()
            
    
    def jump(self):
        self.jump_times -= 1
        collision = False
        print('jump')
        for height in range(12):  #一段跳100
            if self.pos[1]  >= 90:
                go_right(bg_top, foods, obstacles, mario.speed)
                self.pos[1] -= 8
                draw_base()
                player1_rect.topleft = self.pos
                trans_rect.topleft = self.pos
                base.blit(transparent,trans_rect)
                if collide( player1_rect, foods, obstacles ):
                    collision = True
                    self.state = 'crash1'
                    self.state_time = time.time()
                    base.blit(crash1,player1_rect)
                    print('hit3')
                else:
                    if collision == False:
                        base.blit(jump1,player1_rect)
                    else:
                        base.blit(crash1,player1_rect)
                if self.jump_times == 1: #檢查是否二段跳
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        
                        if e.type == pygame.KEYDOWN:
                            if pygame.key.get_pressed()[pygame.K_SPACE]:
                                self.jumpheigher()
                                break
                if self.jump_times == 0:
                    break
                pygame.display.update()
        
                
        for height in range(33): #二段跳不超過235
            if self.pos[1] <= 235:
                go_right(bg_top, foods, obstacles, mario.speed)
                self.pos[1] += 8
                draw_base()
                player1_rect.topleft = self.pos
                trans_rect.topleft = self.pos
                base.blit(transparent,trans_rect)
                if collide( player1_rect, foods, obstacles ):
                    self.state = 'crash1'
                    self.state_time = time.time()
                    base.blit(crash1,player1_rect)
                    print('hit4')
                else:
                    if collision == False:
                        base.blit(jump1,player1_rect)
                    else:
                        base.blit(crash1,player1_rect)
                if self.jump_times == 1: #檢查是否二段跳
                     for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        
                        if e.type == pygame.KEYDOWN:
                            if pygame.key.get_pressed()[pygame.K_SPACE]:
                                self.jumpheigher()
                if self.jump_times == 0:
                    break
                pygame.display.update()

def bonus():
    pass

def go_left(bg, speed):
    bg_speed = int(speed/5)
    # TODO: use pixel array to change your background         
    pxa = pygame.PixelArray(bg)
    temp = pxa[800-bg_speed:800,:]
    pxa[bg_speed:800,:] = pxa[0:800-bg_speed,:]
    pxa[0:bg_speed,:] = temp
    del pxa
    
def obj_go_right(foods,obstacles, speed):
    for i in range(len(obstacles)):
        obstacles[i].go_right(speed)
    for i in range(len(foods)):
        foods[i].go_right(speed)
    
def game_over():
    draw_base()
    base.blit(die1,die_rect)
    die_rect.topleft = [200,250]
    pygame.display.update()
    time.sleep(0.5)
    draw_base()
    base.blit(die2,die_rect)
    die_rect.topleft = [200,245]
    pygame.display.update()
    time.sleep(0.5)
    draw_base()
    base.blit(die3,die_rect)
    pygame.display.update()
    time.sleep(3)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                print(m_pos)
                if m_pos[0] >= 315 and m_pos[0] <= 475 and m_pos[1] >= 340 \
                and m_pos[1] <= 395 :
                    return
                
        base.blit(bg_result,(0,0))
        pygame.display.update()
        print('money')
        print(money)
        print('score')
        print(score)
        
    


def go_right(bg, foods, obstacles, speed):
    bg_speed = int(speed/5)
    obj_go_right(foods, obstacles, speed)
    pygame.display.update()
    # TODO: use pixel array to change your background
    if power.power_down(bloodbar, 0.06) == 'game_over':
        return False

    pxa = pygame.PixelArray(bg)
    temp = pxa[0:bg_speed,:]
    pxa[0:800-bg_speed,:] = pxa[bg_speed:800,:]
    pxa[800-bg_speed:800,:] = temp
    del pxa
    pxa = pygame.PixelArray(floor)
    temp = pxa[0:speed,:]
    pxa[0:800-speed,:] = pxa[speed:800,:]
    pxa[800-speed:800,:] = temp
    del pxa

def collide( player_rect, foods, obstacles ):
    eat( player_rect, foods)
    if mario.super1 == False:
        for i in range(len(obstacles)):
            if obstacles[i].name != 'obstacle3':
                if obstacles[i].pos[0]+50 < player_rect.right \
                    and obstacles[i].pos[0] > player_rect.left:
                    if player_rect.bottom > obstacles[i].pos[1]:
                        base.blit(red,bg_pos)
                        pygame.display.update()
                        power.power_down(bloodbar,8)
                        mario.protect()
                        return True
            else:
                if obstacles[i].pos[0]+50 < player_rect.right \
                    and obstacles[i].pos[0] > player_rect.left:
                    if mario.state != 'slide':
                        base.blit(red,bg_pos)
                        pygame.display.update()
                        power.power_down(bloodbar,8)
                        mario.protect()
                        return True
                    
        return False
    else:
        pass

last_food = -1
def eat( player_rect, foods):
    global money, score, last_food
    for i in range(len(foods)):
        if foods[i].pos[0]+10 < player_rect.right \
        and foods[i].pos[0] > player_rect.left:
            if player_rect.bottom > foods[i].pos[1]:
                #吃到東西
                if last_food != i:
                    last_food = i
                    if foods[i].name == 'coin':
                        money+= 100
                    if foods[i].name == 'candy':
                        score+= 100
                    if foods[i].name == 'fast':
                        mario.super_fast()
                    if foods[i].name == 'energy':
                        power.power_up(bloodbar,10)
                    foods[i].img = transparent
                else:
                    pass
    
def game_init():
    bloodbar = pygame.image.load(dir_path+'\\bloodbar1.png')
    obstacles = [Obstacle('obstacle1', [ob1_pos[0]-110,ob1_pos[1]]),\
                 Obstacle('obstacle1', [ob1_pos[0]+1000,ob1_pos[1]]),\
                 Obstacle('obstacle1', [ob1_pos[0]+1190,ob1_pos[1]]),\
                 Obstacle('obstacle2', [ob2_pos[0]+1390,ob2_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+2000,ob3_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+2100,ob3_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+2200,ob3_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+2300,ob3_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+2400,ob3_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+2500,ob3_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+2600,ob3_pos[1]]),\
                 Obstacle('obstacle2', [ob2_pos[0]+2820,ob2_pos[1]]),\
                 Obstacle('obstacle1', [ob1_pos[0]+3500,ob1_pos[1]]),\
                 Obstacle('obstacle1', [ob1_pos[0]+3680,ob1_pos[1]]),\
                 Obstacle('obstacle2', [ob2_pos[0]+3870,ob2_pos[1]]),\
                 Obstacle('obstacle1', [ob1_pos[0]+4330,ob1_pos[1]]),\
                 Obstacle('obstacle1', [ob1_pos[0]+4490,ob1_pos[1]]),\
                 Obstacle('obstacle2', [ob2_pos[0]+4690,ob2_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+4900,ob3_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+5000,ob3_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+5100,ob3_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+5200,ob3_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+5300,ob3_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+5400,ob3_pos[1]]),\
                 Obstacle('obstacle3', [ob3_pos[0]+5500,ob3_pos[1]]),\
                 Obstacle('obstacle2', [ob2_pos[0]+5700,ob2_pos[1]])]
    #[Food('coin',[500,280]),Food('coin',[550,280]),Food('coin',[600,280]),Food('coin',[650,280]),
    
    foods = [Food('coin',[500,280]),Food('coin',[550,280]),Food('coin',[600,280]),Food('coin',[650,280]),\
             Food('coin',[700,280]),Food('coin',[730,240]),\
             Food('coin',[760,200]),Food('coin',[790,240]),\
             Food('coin',[820,280]),Food('coin',[870,280]),\
             Food('candy',[920,280]),Food('energy',[970,280]),\
             Food('coin',[1020,280]),Food('coin',[1070,280]),\
             Food('candy',[1120,280]),Food('coin',[1170,280]),\
             Food('candy',[1220,280]),Food('candy',[1270,280]),\
             Food('coin',[1320,280]),Food('coin',[1370,280]),\
             Food('candy',[1420,280]),Food('coin',[1470,280]),\
             Food('candy',[1520,280]),Food('candy',[1570,280]),\
             Food('coin',[1620,280]),Food('coin',[1670,280]),\
             Food('coin',[1720,280]),Food('coin',[1770,280]),\
             Food('coin',[1810,280]),Food('coin',[1840,240]),\
             Food('candy',[1870,200]),Food('coin',[1900,240]),\
             Food('coin',[1930,280]),Food('coin',[1980,280]),\
             Food('coin',[2030,240]),Food('candy',[2060,200]),Food('coin',[2090,240]),\
             Food('coin',[2120,280]),Food('coin',[2170,280]),Food('coin',[2200,240]),\
             Food('coin',[2230,200]),Food('candy',[2260,160]),Food('coin',[2290,200]),\
             Food('coin',[2320,240]),Food('coin',[2350,280]),\
             Food('candy',[2400,280]),Food('coin',[2450,280]),\
             Food('candy',[2500,280]),Food('candy',[2550,280]),\
             Food('coin',[2600,280]),Food('coin',[2650,280]),\
             Food('candy',[2700,280]),Food('coin',[2750,280]),\
             Food('candy',[2800,280]),Food('candy',[2850,280]),\
             Food('coin',[2900,280]),Food('coin',[2950,280]),\
             Food('coin',[3000,280]),Food('coin',[3050,280]),\
             Food('candy',[3100,280]),Food('coin',[3150,280]),\
             Food('candy',[3200,280]),Food('candy',[3250,280]),\
             Food('coin',[3300,280]),Food('coin',[3350,280]),
             Food('coin',[3400,280]),Food('coin',[3450,280]),\
             Food('candy',[3500,280]),Food('coin',[3550,280]),\
             Food('coin',[3600,280]),Food('coin',[3630,240]),\
             Food('coin',[3660,200]),Food('candy',[3690,160]),Food('coin',[3720,200]),\
             Food('coin',[3750,240]),Food('coin',[3780,280]),\
             Food('candy',[3830,280]),Food('candy',[3880,280]),\
             Food('coin',[3930,280]),Food('coin',[3980,280]),\
             Food('coin',[4030,280]),Food('coin',[4060,230]),\
             Food('coin',[4090,180]),Food('candy',[4120,130]),Food('coin',[4150,180]),\
             Food('coin',[4180,230]),Food('coin',[4210,280]),\
             Food('coin',[4260,280]),Food('coin',[4310,280]),\
             Food('coin',[4340,240]),Food('candy',[4370,200]),Food('coin',[4400,240]),\
             Food('coin',[4430,280]),Food('coin',[4480,280]),\
             Food('coin',[4510,240]),Food('candy',[4540,200]),Food('coin',[4570,240]),\
             Food('coin',[4600,280]),Food('coin',[4650,280]),Food('coin',[4680,240]),\
             Food('coin',[4710,200]),Food('candy',[4740,160]),Food('coin',[4770,200]),\
             Food('coin',[4800,240]),Food('coin',[4830,280]),\
             Food('candy',[4880,280]),Food('coin',[4930,280]),\
             Food('candy',[4980,280]),Food('coin',[5030,280]),\
             Food('coin',[5080,280]),\
             Food('coin',[5130,280]),\
             Food('coin',[5160,240]),Food('candy',[5190,200]),Food('coin',[5220,240]),\
             Food('coin',[5250,280]),Food('coin',[5300,280]),\
             Food('coin',[5330,240]),Food('candy',[5360,200]),Food('coin',[5390,240]),\
             Food('coin',[5420,280]),Food('coin',[5470,280]),Food('coin',[5500,240]),\
             Food('coin',[5530,200]),Food('candy',[5560,160]),Food('coin',[5590,200]),\
             Food('coin',[5620,240]),Food('coin',[5650,280]),\
             Food('candy',[5700,280]),Food('coin',[5750,280]),\
             Food('candy',[5800,280]),Food('coin',[5850,280]),\
             Food('candy',[5900,280]),Food('candy',[5950,280]),\
             Food('coin',[6000,280]),Food('coin',[6050,280]),\
             Food('candy',[6100,280]),Food('coin',[6150,280]),\
             Food('candy',[6200,280]),Food('candy',[6250,280]),\
             Food('candy',[6300,280]),Food('candy',[6350,280]),\
             Food('coin',[6400,280]),Food('coin',[6450,280]),\
             Food('coin',[6500,280]),Food('coin',[6530,230]),\
             Food('coin',[6560,180]),Food('candy',[6590,130]),Food('coin',[6620,180]),\
             Food('coin',[6650,230]),Food('coin',[6680,280]),]

    power = Power()
    mario = Mario()
    return mario, power, foods, obstacles, bloodbar

def display_objects(foods, obstacles):
    for i in range(len(obstacles)):
        base.blit(obstacles[i].img, obstacles[i].pos)
    for i in range(len(foods)):
        base.blit(foods[i].img, foods[i].pos)
        
def draw_base():
    base.fill((0,0,0))
    base.blit(bg_bottom,bg_pos)
    base.blit(bg_top,bg_pos)
    base.blit(floor, floor_pos)
    display_objects(foods, obstacles)
    base.blit(bloodbar, power_pos)
    
"""    
obstacles = [Obstacle('obstacle1', [ob1_pos[0],ob1_pos[1]]),\
             Obstacle('obstacle1', [ob1_pos[0]+200,ob1_pos[1]]),\
             Obstacle('obstacle2', [ob2_pos[0]+400,ob2_pos[1]]),\
             Obstacle('obstacle2', [ob2_pos[0]+800,ob2_pos[1]]),\
             Obstacle('obstacle1', [ob1_pos[0],ob1_pos[1]]),\
             Obstacle('obstacle1', [ob1_pos[0]+200,ob1_pos[1]]),\
             Obstacle('obstacle2', [ob2_pos[0]+400,ob2_pos[1]]),\
             Obstacle('obstacle2', [ob2_pos[0]+800,ob2_pos[1]]),\
             Obstacle('obstacle1', [ob1_pos[0],ob1_pos[1]]),\
             Obstacle('obstacle1', [ob1_pos[0]+200,ob1_pos[1]]),\
             Obstacle('obstacle2', [ob2_pos[0]+400,ob2_pos[1]]),\
             Obstacle('obstacle2', [ob2_pos[0]+800,ob2_pos[1]]),\
             Obstacle('obstacle1', [ob1_pos[0],ob1_pos[1]]),\
             Obstacle('obstacle1', [ob1_pos[0]+200,ob1_pos[1]]),\
             Obstacle('obstacle2', [ob2_pos[0]+400,ob2_pos[1]]),\
             Obstacle('obstacle2', [ob2_pos[0]+800,ob2_pos[1]])]  

foods = [Food('coin',[950,900]),Food('coin',[970,900]),Food('coin',[980,900]),\
         Food('coin',[990,900]),Food('coin',[1000,900]),Food('coin',[1200,900])]
"""

power = Power()
mario = Mario()

player_pos = mario.pos
pygame.key.set_repeat()
player1_rect = player1.get_rect()
player1_rect.topleft = mario.pos
player2_rect = player2.get_rect()
player2_rect.topleft = mario.pos
crash2_rect = crash2.get_rect()
crash2_rect.topleft = [200,260]
die_rect = player1.get_rect()
die_rect.topleft = mario.pos  
trans_rect = transparent.get_rect(topleft= (mario.pos[0],mario.pos[1]))


def run():
    clock = pygame.time.Clock()   #建立時間元件
    change_image = 0
    while True:
    # TODO: (bonus) think about adding a key to accelerate mario. slow down when releasing that key.
        clock.tick(50)
        #print(clock)
        change_image += 1
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if e.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    mario.jump()
                    mario.reset_jump_times()
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    mario.slide()
            if e.type == pygame.KEYUP:
                if mario.state == 'slide':
                    mario.state = 'run'
    
        if go_right(bg_top, foods, obstacles, mario.speed) == False:
            game_over()
            break
             
        mario.desuper_fast()
        mario.deprotect() 
        mario.destate()
        draw_base()
        mario.blit_state(change_image)
        base.blit(transparent,trans_rect)
        if collide( player1_rect, foods, obstacles ) :
            print('hit5')
            mario.state = 'crash1'
            mario.state_time = time.time()
        pygame.display.update()


IS_RUNNING = True
while IS_RUNNING:
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if e.type == pygame.MOUSEBUTTONDOWN :
            m_pos = pygame.mouse.get_pos()
            print(m_pos)
            IS_RUNNING = False
                  
    base.fill((0,0,0))
    base.blit(startb,(0,0))
    pygame.display.update()  


while True :
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if e.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()
            print(m_pos)
            if m_pos[0] >= 575 and m_pos[0] <= 785 and m_pos[1] >= 310 \
               and m_pos[1] <= 375 :
                   mario, power, foods, obstacles, bloodbar = game_init()
                   run()
                   
    base.fill((0,0,0))
    base.blit(dance_bg,(0,0))
    base.blit(play_button,(0,0))
    pygame.display.update()               
                
                