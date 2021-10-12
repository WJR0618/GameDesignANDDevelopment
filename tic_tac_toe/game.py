import pygame
import random
import time

def input_player_letter():
    """
    let the player type which letter they want to be.
    Returns a list with the player's letter as the first item and the
    computer's letter as the second.
    """
    while True:
        display_message('choose your symbol: (O or X)')
        userletter = input().upper()
        if len(userletter) > 1:
            display_message('Please input a singlt letter.')
        elif userletter not in 'OX':
            display_message('Please input O or X')
        else:
            if userletter == 'X':
                return ['X','O']
            else:
                return ['O','X']

def who_goes_first():
    # Randomly choose which player goes first.
    if random.randint(0, 1) == 0:
        return 'player'
    else:
        return 'computer'

def draw_board(board):
    # This function prints out the board that it was passed.
    # "board" is a list of 10 strings representing the board (ignore index 0).
    print(board[7] + '|' + board[8] + '|' + board[9])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[1] + '|' + board[2] + '|' + board[3])

def is_winner(bd, lt):
    # Given a board and a player's letter, this function returns True if
    #  that player has won.
    # We use "bd" instead of "board" and "lt" instead of "letter" so we
    # don't have to type as much.
    return ((bd[7] == lt and bd[8] == lt and bd[9] == lt) or 
            (bd[4] == lt and bd[5] == lt and bd[6] == lt) or 
            (bd[1] == lt and bd[2] == lt and bd[3] == lt) or 
            (bd[7] == lt and bd[4] == lt and bd[1] == lt) or 
            (bd[8] == lt and bd[5] == lt and bd[2] == lt) or 
            (bd[9] == lt and bd[6] == lt and bd[3] == lt) or 
            (bd[7] == lt and bd[5] == lt and bd[3] == lt) or 
            (bd[9] == lt and bd[5] == lt and bd[1] == lt)) 

def is_space_free(board, move):
    return board[move] == ' '

def is_board_full(board):
    # Return True if every space on the board has been taken. Otherwise,
    # return False.
    for i in range(1, 10):
        if is_space_free(board, i):
            return False
    return True

def get_player_move(board):
    # Let the player enter their move.
    move = ' ';
    display_message('What is your next move? (1-9)')
    while move not in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] or \
    not is_space_free(board, int(move)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False
                return is_playing
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                move = str(mouse_pos_to_array_index( m_pos ))
    return int(move)

def make_move(board, letter, move):
    board[move] = letter

def random_choose(board):
    """Returns a valid move from the passed list on the passed board.
    Returns None if there is no valid move."""
    print('computer is thinking...')
    time.sleep(0.5)

    
    #possible_moves = [] 
    #TODO: check valid locations and randomly pick one.


def find_winning_move(board, computer_letter):
    """For every possible move, check if it can win with that move."""
    for i in range(len(board)):
        boardcopy = board.copy()
        if is_space_free(boardcopy, i):
            make_move(boardcopy, computer_letter, i)
            if is_winner(boardcopy, computer_letter):
                return i
    return None

def block_player_move(board, player_letter):
    """try to block a player's move"""
    board_copy = board.copy()
    move = find_winning_move(board_copy, player_letter)
    return move

def choose_corner(board):
    """choose a corner move if possible"""
    boardcopy = board.copy()
    possible_moves = []
    
    if is_space_free( boardcopy, 1 ):
        possible_moves.append(1)
    if is_space_free( boardcopy, 3 ):
        possible_moves.append(3)
    if is_space_free( boardcopy, 7 ):
        possible_moves.append(7)
    if is_space_free( boardcopy, 9 ):
        possible_moves.append(9)
    
    
    move = random.choice(possible_moves)
    return move
        
def choose_center(board):
    """choose the center if possible"""
    boardcopy = board.copy()
    if is_space_free(boardcopy, 5):
        move = 5
        return move
    
def choose_side(board):
    """choose side positions if possible"""
    boardcopy = board.copy()
    possible_moves = []
    
    if is_space_free( boardcopy, 2 ):
        possible_moves.append(2)
    if is_space_free( boardcopy, 4 ):
        possible_moves.append(4)
    if is_space_free( boardcopy, 6 ):
        possible_moves.append(6)
    if is_space_free( boardcopy, 8 ):
        possible_moves.append(8)
    
    
    move = random.choice(possible_moves)
    return move

def get_computer_move(board, computer_letter, player_letter):
    move = find_winning_move(board, computer_letter)
    if move != None: return move
    move = block_player_move(board, player_letter)
    if move != None: return move
    move = choose_corner(board)
    if move != None: return move
    move = choose_center(board)
    if move != None: return move
    return choose_side(board)

def get_computer_move1(board, computer_letter, player_letter):
    move = find_winning_move(board, computer_letter)
    if move != None: return move
    move = block_player_move(board, player_letter)
    if move != None: return move
    move = minimax(board, 'O')[1]
    if move != None: return move

def display_message(msg):
    """display some texts."""
    print(msg)
    
def mouse_pos_to_array_index( m_pos ):
    if m_pos[0] >= 30 and m_pos[0] <= 105 and m_pos[1] >= 120 and m_pos[1] <= 195:
        index = 7
        print(index)
        return index
    if m_pos[0] >= 108 and m_pos[0] <= 195 and m_pos[1] >= 120 and m_pos[1] <= 195:
        index = 8
        print(index)
        return index
    if m_pos[0] >= 198 and m_pos[0] <= 270 and m_pos[1] >= 120 and m_pos[1] <= 195:
        index = 9
        print(index)
        return index
    if m_pos[0] >= 30 and m_pos[0] <= 105 and m_pos[1] >= 198 and m_pos[1] <= 285:
        index = 4
        print(index)
        return index
    if m_pos[0] >= 108 and m_pos[0] <= 195 and m_pos[1] >= 198 and m_pos[1] <= 285:
        index = 5
        print(index)
        return index
    if m_pos[0] >= 198 and m_pos[0] <= 270 and m_pos[1] >= 198 and m_pos[1] <= 285:
        index = 6
        print(index)
        return index
    if m_pos[0] >= 30 and m_pos[0] <= 105 and m_pos[1] >= 288 and m_pos[1] <= 360:
        index = 1
        print(index)
        return index
    if m_pos[0] >= 108 and m_pos[0] <= 195 and m_pos[1] >= 288 and m_pos[1] <= 360:
        index = 2
        print(index)
        return index
    if m_pos[0] >= 198 and m_pos[0] <= 270 and m_pos[1] >= 273 and m_pos[1] <= 360:
        index = 3
        print(index)
        return index
def find_picture_pos( array_index ):
    if array_index in [1,4,7]:
        x = 18
    if array_index in [2,5,8]:
        x = 98
    if array_index in [3,6,9]:
        x = 190
    if array_index in [1,2,3]:
        y = 278
    if array_index in [4,5,6]:
        y = 192
    if array_index in [7,8,9]:
        y = 100
    return (x,y)


def draw(board):
    base.fill((255, 255, 255))
    base.blit( bg_img, (0,50) )
    #base.blit( o_img,(15,270) )
    #base.blit( x_img,(15,190) )
    pygame.draw.line( base, (0,0,0), (30,195), (270,195), 3 )
    pygame.draw.line( base, (0,0,0), (30,285), (270,285), 3 )
    pygame.draw.line( base, (0,0,0), (105,120), (105,360), 3 )
    pygame.draw.line( base, (0,0,0), (195,120), (195,360), 3 )
    
    for i in range(len(board)):
        if board[i] != ' ':
            if board[i] == 'O':
                #print(find_picture_pos(i))
                base.blit( o_img,find_picture_pos(i) )
            if board[i] == 'X':
                #print(find_picture_pos(i))
                base.blit( x_img,find_picture_pos(i) )
    pygame.display.update()
    
def restart_button_down(result):
    m_pos = (0,0);
    if result == 'win':
        base.blit( win_img,(10,20) )
    if result == 'lose':
        base.blit( lose_img,(10,20) )
    if result == 'draw':
        base.blit( draw_img,(40,20) )
        
    base.blit( restart_img,(90,300) )
    pygame.display.update()
    while m_pos[0] < 90 or m_pos[0] >210 or m_pos[1] < 300 or m_pos[1] > 340:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False
                return is_playing
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                if m_pos[0] >= 90 and m_pos[0] <= 210 and m_pos[1] >= 300 \
                and m_pos[1] <= 340:
                    return True
    return False

def score(board):
    if is_winner(board, 'X'):
        return 10
    elif is_winner(board, 'O'):
        return -10
    else:
        return 0
    
def is_game_over(board):
    if is_winner(board, 'X') or is_winner(board, 'O') or is_board_full(board):
        return True
    else:
        return False
        
def switch_turn(symbol):
    if symbol == 'X':
        return 'O'
    else:
        return 'X'
    
def find_possible_moves(board,symbol):
    moves = []
    for i in range(len(board)) :
        if is_space_free(board, i) and i > 0:
            moves.append(i)
    return moves

def minimax(board, symbol):
    score_list = []
    board_copy = board.copy()
    if is_game_over(board_copy):
        return score(board_copy),0
    symbol = switch_turn(symbol)
    moves = find_possible_moves(board_copy, symbol)
    for move in moves:
        make_move(board_copy, symbol, move)
        score_list.append(minimax(board_copy, symbol)[0])
        
    print(score_list)
    if symbol == 'O':
        return min(score_list),moves[score_list.index(min(score_list))]
    else:
        return max(score_list),moves[score_list.index(max(score_list))]
        
def run():
    
    board = [' '] * 10
    #player_letter, computer_letter = input_player_letter()
    player_letter = 'O'
    computer_letter = 'X'
    turn = who_goes_first()
    display_message('init')
    is_playing = True
    while is_playing:
        draw_board(board)
        display_message('it\'s '+turn+'\'s turn.')     
        base.fill((255, 255, 255))
        draw(board)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False
                return is_playing
          
        
        if turn == 'player':
            base.blit( yourturn_img, (65,10) )
            base.blit( letter_img,(45,60) )
            pygame.display.update()
            move = get_player_move(board)
            if move == False:
                is_playing = False
                return is_playing
            #move = 1
            make_move(board, player_letter, move)
        
            if is_winner(board, player_letter): #檢查有沒有贏
                draw_board(board)
                draw(board)
                display_message('win')
                if restart_button_down('win'):
                    is_playing = False
                    return True
                else:
                    is_playing = False
                    return is_playing
                                                    
            elif is_board_full(board): #檢查棋盤是不是滿了
                display_message('draw')
                draw(board)
                if restart_button_down('draw'):
                    is_playing = False
                    return True
                else:
                    is_playing = False
                    return is_playing
            else:                       #輪到電腦
                turn = 'computer'
        else:
            # AI 1: random choose
            # AI 2: stragetic move
            base.blit( computerturn_img, (65,10) )
            base.blit( letter_img,(45,60) )
            pygame.display.update()
            time.sleep(1)
            #x = minimax(board, 'O')[1]
            move = get_computer_move(board, computer_letter, player_letter)
            #move = minimax(board, 'O')[1]
            make_move(board, computer_letter, move)
                
            if is_winner(board, computer_letter):  #檢查有沒有贏
                draw_board(board)
                draw(board)
                display_message('lose')
                if restart_button_down('lose'):
                    is_playing = False
                    return True
                else:
                    is_playing = False
                    return is_playing
            elif is_board_full(board):  #檢查棋盤是不是滿了
                display_message('draw')
                draw(board)
                if restart_button_down('draw'):
                    is_playing = False
                    return True
                else:
                    is_playing = False
                    return is_playing           
            else:
                turn = 'player'         #輪到玩家
                
        pygame.display.update()
    #return is_playing

pygame.init()
WEIGHT = 300
HEIGHT = 400
base = pygame.display.set_mode((WEIGHT, HEIGHT))
bg_img = pygame.image.load('background.png')
o_img = pygame.image.load('O.png')
x_img = pygame.image.load('X.png')
win_img = pygame.image.load('win.png')
lose_img = pygame.image.load('lose.png')
draw_img = pygame.image.load('draw.png')
start_img = pygame.image.load('start1.png')
restart_img = pygame.image.load('restart.png')
yourturn_img = pygame.image.load('yourturn.png')
computerturn_img = pygame.image.load('computerturn.png')
letter_img = pygame.image.load('letter.png')
tictactoe_img = pygame.image.load('tictactoe.png')
base.fill((255, 255, 255))
base.blit( bg_img, (0,50) )
base.blit( start_img,(90,280) )
base.blit( tictactoe_img,(0,50) )
pygame.display.update()



RUN = True
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos() 
            if 90 < m_pos[0] and  m_pos[0] < 210 and 280 < m_pos[1] and m_pos[1] < 320:
                RUN = run()
                if( RUN == True ):
                    base.fill((255, 255, 255))
                    base.blit( bg_img, (0,50) )
                    base.blit( start_img,(90,280) )
                    base.blit( tictactoe_img,(0,50) )
                    pygame.display.update()
    pygame.display.update()
    #draw()
pygame.quit()  # 退出pygame
