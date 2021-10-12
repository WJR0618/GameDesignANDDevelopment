import pygame, sys, os, time

class Player():
    def __init__(self,pos):
        self.pos = pos

class Star():
    def __init__(self,pos):
        self.pos = pos

class Selector():
    def __init__(self,pos):
        self.pos = pos

dir_path = os.path.dirname(os.path.abspath(__file__))

pygame.init()

game_map = [ [' ',' ',' ',' ',' ',' ',' '],
           ['x','#','#','#','#','x','x'],
           ['#','o','o','o','o','#','x'],
           ['#','o','o','o','o','o','#'],
           ['#','o','o','o','o','o','#'],
           ['#','o','o','o','o','o','#'],
           ['#','o','o','o','o','o','#'],
           ['x','#','#','#','#','o','x']]

TILE_WIDTH = 50
TILE_HEIGHT = 85
TILE_FLOOR_HEIGHT = 40
MAP_WIDTH = len(game_map[0])
MAP_HEIGHT = len(game_map)

IMAGES = {'star': pygame.image.load(dir_path+'\\Star.png'),
              'selector': pygame.image.load(dir_path+'\\Selector.png'),
              'corner': pygame.image.load(dir_path+'\\Wall_Block_Tall.png'),
              'wall': pygame.image.load(dir_path+'\\Wood_Block_Tall.png'),
              'inside floor': pygame.image.load(dir_path+'\\Plain_Block.png'),
              'outside floor': pygame.image.load(dir_path+'\\Grass_Block.png'),
              'boy': pygame.image.load(dir_path+'\\boy.png'),
              'rock': pygame.image.load(dir_path+'\\Rock1.png'),
              'restart': pygame.image.load(dir_path+'\\restart.png'),
              'next_stage': pygame.image.load(dir_path+'\\next_stage.png'),
              'stage1': pygame.image.load(dir_path+'\\stage1.png'),
              'stage2': pygame.image.load(dir_path+'\\stage2.png'),
              'stage3': pygame.image.load(dir_path+'\\stage3.png'),
              'start1': pygame.image.load(dir_path+'\\start1.png'),
              'start2': pygame.image.load(dir_path+'\\start2.png'),
              'home': pygame.image.load(dir_path+'\\home.png'),
              'home_start': pygame.image.load(dir_path+'\\home_start.png'),
              'home_bg': pygame.image.load(dir_path+'\\home_bg.png'),
              'clear': pygame.image.load(dir_path+'\\clear.png')
          }

TILE_DEFINITION = {'x': IMAGES['corner'],
               '#': IMAGES['wall'],
               'o': IMAGES['inside floor'],
               ' ': IMAGES['outside floor'],
               '1': IMAGES['rock'],
               }

def set_state(game_map, stage):
    global MAP_WIDTH 
    global MAP_HEIGHT 

    if stage == 'stage1':
        game_map = [[' ',' ',' ',' ',' ',' ',' '],
                   ['x','#','#','#','#','x','x'],
                   ['#','o','o','o','o','#','x'],
                   ['#','o','o','o','o','o','#'],
                   ['#','o','o','o','o','o','#'],
                   ['#','o','o','o','o','o','#'],
                   ['#','o','o','o','o','o','#'],
                   ['x','#','#','#','#','o','x']]
        player = Player((5,4))
        selectors = [Selector((2,3)),Selector((2,4))]
        stars = [Star((4,2)),Star((4,4))]
        MAP_WIDTH = len(game_map[0])
        MAP_HEIGHT = len(game_map)
        draw_stage_start(game_map, player, stars, selectors, stage)
    elif stage == 'stage2':
        game_map = [[' ',' ',' ',' ','x','x',' ',' '],
                   [' ','x','x','x','o','o','x','x'],
                   ['x','#','o','o','o','o','#','x'],
                   ['x','#','o','#','o','x','x','x'],
                   ['x','o','o','#','o','x','o','x'],
                   ['x','o','#','o','o','o','o','x'],
                   ['x','o','o','o','o','o','o','x'],
                   ['x','x','x','x','x','x','x','x']]
        player = Player((1,5))
        selectors = [Selector((4,6)),Selector((5,6)),Selector((6,6))]
        stars = [Star((2,4)),Star((5,5)),Star((6,2))]
        MAP_WIDTH = len(game_map[0])
        MAP_HEIGHT = len(game_map)
        draw_stage_start(game_map, player, stars, selectors, stage)
    elif stage == 'stage3':
        game_map = [[' ',' ','x','x','x','x','x',' '],
                   ['x','#','#','o','o','o','x',' '],
                   ['#','o','o','o','o','o','#','x'],
                   ['#','#','#','o','o','o','#',' '],
                   ['#','o','#','#','o','o','#',' '],
                   ['#','o','#','o','o','o','#','#'],
                   ['#','o','o','o','o','o','o','#'],
                   ['#','o','o','o','o','o','o','#'],
                   ['x','#','#','#','#','#','#','#']]
        player = Player((2,2))
        selectors = [Selector((2,1)),Selector((3,5)),Selector((4,1)),
                     Selector((5,4)),Selector((6,3)),
                     Selector((6,6)),Selector((7,4))]
        stars = [Star((2,3)),Star((3,4)),Star((4,4)),Star((6,1)),Star((6,3)),
                 Star((6,4)),Star((6,5))]
        MAP_WIDTH = len(game_map[0])
        MAP_HEIGHT = len(game_map)
        draw_stage_start(game_map, player, stars, selectors, stage)
    
    return player, selectors, stars,game_map

def draw_map(game_map, player, stars, selectors):
    """Draws the map to a Surface object, including the player's position"""
    print( (MAP_WIDTH,MAP_HEIGHT)  )
    # map_surf will be the single Surface object that the tiles are drawn on,
    # by doing so it is easy to position the entire map on the BASE_SURF object

    # First, the width and height must be calculated.    
    map_surf_w = MAP_WIDTH * TILE_WIDTH
    map_surf_h = (MAP_HEIGHT-1) * TILE_FLOOR_HEIGHT + TILE_HEIGHT
    map_surf = pygame.Surface((map_surf_w, map_surf_h))
    map_surf.fill((0, 170, 255)) # start with a blank color on the surface.

    # Draw the tile sprites onto this surface.
    for r in range(len(game_map)):
        for c in range(len(game_map[r])):
            space_rect = pygame.Rect((c * TILE_WIDTH, r * TILE_FLOOR_HEIGHT, TILE_WIDTH, TILE_HEIGHT))

            if game_map[r][c] in TILE_DEFINITION:
                base_tile = TILE_DEFINITION[game_map[r][c]]

            # First draw the base ground/wall tile.
            map_surf.blit(base_tile, space_rect)

            for item in selectors:
                if (r, c) == item.pos:
                    map_surf.blit(IMAGES['selector'], space_rect)

            for item in stars:
                if (r, c) == item.pos:
                    map_surf.blit(IMAGES['star'], space_rect)
                    
            # Last draw the player on the board.
            if (r, c) == player.pos:
                map_surf.blit(IMAGES['boy'], space_rect)

    return map_surf

def make_move(game_map, player, stars, move_to):
    offset = (0,0)
    if move_to == 'UP':
        offset = (-1,0)
    elif move_to == 'DOWN':
        offset = (1,0)
    elif move_to == 'LEFT':
        offset = (0,-1)
    elif move_to == 'RIGHT':
        offset = (0,1)
    # '#' : 牆
    # 'x' : 牆
    player_want_to_move = ( player.pos[0] + offset[0], player.pos[1] + offset[1] )
    star_want_to_move = ( player.pos[0] + 2*offset[0], player.pos[1] + 2*offset[1] )
    try:
        if game_map[player_want_to_move[0]][player_want_to_move[1]] =='o':
            for star in stars:
                if player_want_to_move == star.pos:
                    if game_map[star_want_to_move[0]][star_want_to_move[1]] =='o':
                        #player.pos = player_want_to_move
                        star.pos = star_want_to_move
                        break
                    else:
                        return
            player.pos = player_want_to_move

        else:
            pass
    except: #list out of range
        pass
    
    # TODO: compute the position that the player want to move
    # TODO: check if that position is on the floor

    # TODO: check if there is a star on that position 
    # TODO: if the star can be pushed, push that star and move player to that position

def is_solved(selectors, stars):
    # TODO: check if the puzzle is solved
    solved = []
    for selector in selectors:
        for star in stars:
            if selector.pos == star.pos:
                if selector.pos not in solved:
                    solved.append(selector.pos)
    if len(solved) == len(selectors):
        return True
    else:
        return False
    
def draw_stage_start(game_map, player, stars, selectors, stage):
    for i in range(5):     
        BASE_SURF.fill((0, 170, 255))
        map_surf = draw_map(game_map, player, stars, selectors)
        map_surf_rect = map_surf.get_rect()
        map_surf_rect.center = BASE_SURF.get_rect().center
        BASE_SURF.blit(map_surf, map_surf_rect)
        if i%2 == 0:
            BASE_SURF.blit( IMAGES[stage], (map_surf_rect[0],map_surf_rect[1]+100) )
        pygame.display.update()
        time.sleep(0.4)
    BASE_SURF.fill((0, 170, 255))
    map_surf = draw_map(game_map, player, stars, selectors)
    map_surf_rect = map_surf.get_rect()
    map_surf_rect.center = BASE_SURF.get_rect().center
    BASE_SURF.blit(map_surf, map_surf_rect)
    BASE_SURF.blit( IMAGES['start2'], (map_surf_rect[0],map_surf_rect[1]+80) )
    pygame.display.update()
    time.sleep(0.8)
    
def next_state(level):
    while True:
        BASE_SURF.blit(IMAGES['restart'], (300,380))
        if level != 4:
            BASE_SURF.blit(IMAGES['next_stage'], (275,310))
            BASE_SURF.blit(IMAGES['home'], (300, 450))
        else:
            BASE_SURF.blit(IMAGES['home'], (300, 310))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONUP:
                #按restart重複此關
                #按next_stage到下一關
                #按BACK TO MENU回到主畫面
                m_pos = pygame.mouse.get_pos() 
                print(m_pos)
                if m_pos[0] >= 315 and m_pos[0] <= 485 and m_pos[1] >= 400 \
                    and m_pos[1] <= 458:
                    next_state1 = 'restart'
                    print(next_state1)
                    return next_state1
                if m_pos[0] >= 290 and m_pos[0] <= 510 and m_pos[1] >= 333 \
                    and m_pos[1] <= 389 and level != 4:
                    next_state1 = 'next_stage'
                    print(next_state1)
                    return next_state1
                if m_pos[0] >= 315 and m_pos[0] <= 485 and m_pos[1] >= 475 \
                    and m_pos[1] <= 528 and level != 4:
                    next_state1 = 'home'
                    print(next_state1)
                    return next_state1
                
                if m_pos[0] >= 315 and m_pos[0] <= 485 and m_pos[1] >= 330 \
                    and m_pos[1] <= 390 and level == 4:
                    next_state1 = 'home'
                    print(next_state1)
                    return next_state1
        pygame.display.update()

    
def run(game_map):   
    
    player,selectors,stars,game_map = set_state(game_map, 'stage1')
    level = 1
    stage = 'stage1'
    while True:
        
        move_to = None
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    move_to = 'LEFT'
                if e.key == pygame.K_RIGHT:
                    move_to = 'RIGHT'
                if e.key == pygame.K_UP:
                    move_to = 'UP'
                if e.key == pygame.K_DOWN:
                    move_to = 'DOWN'
                if e.key == pygame.K_r:
                    player,selectors,stars,game_map = set_state(game_map, stage)
                    map_surf = draw_map(game_map, player, stars, selectors)   
        make_move(game_map, player, stars, move_to)
        BASE_SURF.fill((0, 170, 255))
        map_surf = draw_map(game_map, player, stars, selectors)
        map_surf_rect = map_surf.get_rect()
        map_surf_rect.center = BASE_SURF.get_rect().center
        BASE_SURF.blit(map_surf, map_surf_rect)
        pygame.display.update()
        # TODO: if the puzzle is solved, display a message to indicate user
    
        # TODO: render a text to indicate user  how to reset the game  
    
        if is_solved(selectors, stars):
            BASE_SURF.fill((0, 170, 255))
            map_surf = draw_map(game_map, player, stars, selectors)
            map_surf_rect = map_surf.get_rect()
            map_surf_rect.center = BASE_SURF.get_rect().center
            BASE_SURF.blit(map_surf, map_surf_rect)
            BASE_SURF.blit( IMAGES[stage], (map_surf_rect[0],map_surf_rect[1]) )
            BASE_SURF.blit( IMAGES['clear'], (map_surf_rect[0],map_surf_rect[1]) )
            pygame.display.update()
            time.sleep(1)
            if level < 4:
                level = level + 1 
            stage = 'stage' + str(level)
            state = next_state(level)
            if state == 'next_stage':
                player,selectors,stars,game_map = set_state(game_map, stage)
                map_surf = draw_map(game_map, player, stars, selectors)
                print(game_map)
            elif state == 'restart':
                level = level - 1
                stage = 'stage' + str(level)
                player,selectors,stars,game_map = set_state(game_map, stage)
                map_surf = draw_map(game_map, player, stars, selectors)
                print(game_map)
            elif state == 'home':
                return

while True:
   BASE_SURF = pygame.display.set_mode((800, 600))
   BASE_SURF.fill((0, 170, 255))
   BASE_SURF.blit(IMAGES['home_bg'], (0,0))
   BASE_SURF.blit(IMAGES['home_start'], (305,380))
   pygame.display.update()
   for e in pygame.event.get():
       if e.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
       if e.type == pygame.MOUSEBUTTONDOWN:
           m_pos = pygame.mouse.get_pos()
           print(m_pos)
           if m_pos[0] >= 315 and m_pos[0] <= 485 and m_pos[1] >= 400 \
              and m_pos[1] <= 458:
              run(game_map)