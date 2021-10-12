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
    move = ' '
    while move not in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] or \
    not is_space_free(board, int(move)):
        display_message('What is your next move? (1-9)')
        move = input()
    return int(move)

def make_move(board, letter, move):
    board[move] = letter

def random_choose(board):
    """Returns a valid move from the passed list on the passed board.
    Returns None if there is no valid move."""
    print('computer is thinking...')
    time.sleep(0.5)
    #1.先下會贏的
    #2.避免被結束
        #如果我是玩家，我會下哪裡
    
    possible_moves = [] #找出還沒被下的位置
    # TODO: check valid locations and randomly pick one.


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

def display_message(msg):
    """display some texts."""
    print(msg)
        

board = [' '] * 10
player_letter, computer_letter = input_player_letter()
turn = who_goes_first()
display_message('init')
is_playing = True

while is_playing:
    draw_board(board)
    display_message('it\'s '+turn+'\'s turn.')
    if turn == 'player':
        move = get_player_move(board)
        make_move(board, player_letter, move)

        if is_winner(board, player_letter): #檢查有沒有贏
            draw_board(board)
            display_message('win')
            is_playing = False
            
        elif is_board_full(board): #檢查棋盤是不是滿了
            display_message('draw')
            break
        
        else:                       #輪到電腦
            turn = 'computer'
    else:
        # AI 1: random choose
        # AI 2: stragetic move
        move = get_computer_move(board, computer_letter, player_letter)
        make_move(board, computer_letter, move)
        
        if is_winner(board, computer_letter):  #檢查有沒有贏
            draw_board(board)
            display_message('lose')
            is_playing = False
            
        elif is_board_full(board):  #檢查棋盤是不是滿了
            display_message('draw')
            break
        
        else:
            turn = 'player'         #輪到玩家

