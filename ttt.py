import pygame
from pygame.locals import *


# Creating the constants
BOARDWIDTH = 3  # number of columns in the board
BOARDHEIGHT = 3 # number of rows in the board
TILESIZE = 100
WINDOWWIDTH = 480
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)

BGCOLOR = WHITE
TILECOLOR = GREEN
TEXTCOLOR = DARKTURQUOISE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = BLACK

BLANK = 10
PLAYER_O = 11
PLAYER_X = 21


PLAYER_O_WIN = PLAYER_O * 3
PLAYER_X_WIN = PLAYER_X * 3

CONT_GAME         = 10
DRAW_GAME         = 20
QUIT_GAME         = 30

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

choice = 0


def check_win_game(board):
    def check_draw_game():
        return sum(board)%10 == 9

    def check_horizontal(player):
        for i in [0, 3, 6]:
            if sum(board[i:i+3]) == 3 * player:
                return player

    def check_vertical(player):
        for i in range(3):
            if sum(board[i::3]) == 3 * player:
                return player

    def check_diagonals(player):
        if (sum(board[0::4]) == 3 * player) or (sum(board[2:7:2]) == 3 * player):
            return player

    for player in [PLAYER_X, PLAYER_O]:
        if any([check_horizontal(player), check_vertical(player), check_diagonals(player)]):
            return player

    return DRAW_GAME if check_draw_game() else CONT_GAME


def unit_score(winner, depth):
    if winner == DRAW_GAME:
        return 0
    else:
        return 10 - depth if winner == PLAYER_X else depth - 10


def get_available_step(board):
    return [i for i in range(9) if board[i] == BLANK]


def minmax(board, depth):
    global choice
    result = check_win_game(board)
    if result != CONT_GAME:
        return unit_score(result, depth)

    depth += 1
    scores = []
    steps = []

    for step in get_available_step(board):
        score = minmax(update_state(board, step, depth), depth)
        scores.append(score)
        steps.append(step)

    if depth % 2 == 1:
        max_value_index = scores.index(max(scores))
        choice = steps[max_value_index]
        return max(scores)
    else:
        min_value_index = scores.index(min(scores))
        choice = steps[min_value_index]
        return min(scores)


def update_state(board, step, depth):
    board = list(board)
    board[step] = PLAYER_X if depth % 2 else PLAYER_O
    return board


def update_board(board, step, player):
    board[step] = player


def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(3):
        for tiley in range(3):
            if board[tilex*3+tiley] != BLANK:
                drawTile(tilex, tiley, board[tilex*3+tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def makeText(text, color, bgcolor, top, left):
    '''Create the Surface and Rect objects for some text.'''
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawTile(tilex, tiley, symbol, adjx=0, adjy=0):
    '''
    Draw a tile at board coordinates tilex and tiley, optionally a few
    pixels over (determined by adjx and adjy).
    '''
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(symbol_to_str(symbol), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def symbol_to_str(symbol):
    if symbol == PLAYER_O:
        return 'O'
    elif symbol == PLAYER_X:
        return 'X'


def getSpotClicked(x, y):
    '''From the x & y pixel coordinates, get the x & y board coordinates.'''
    for tileX in range(3):
        for tileY in range(3):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return None


def board_to_step(spotx, spoty):
    return spotx * 3 + spoty


def check_move_legal(coords, board):
    step = board_to_step(*coords)
    return board[step] == BLANK

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, NEW_SURF, NEW_RECT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Tic-Tac-Toe')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    NEW_SURF, NEW_RECT = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    board = [BLANK] * 9
    game_over = False
    x_turn = True
    msg = "TIC_TAC_TOE"
    drawBoard(board, msg)
    pygame.display.update()

    while True:
        coords = None
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                coords = getSpotClicked(event.pos[0], event.pos[1])
                if not coords and NEW_RECT.collidepoint(event.pos):
                    board = [BLANK] * 9
                    game_over = False
                    msg = "TIC_TAC_TOE"
                    drawBoard(board, msg)
                    pygame.display.update()
                    
                
        if coords and check_move_legal(coords, board) and not game_over:
            
            next_step = board_to_step(*coords)
            update_board(board, next_step, PLAYER_X)
            drawBoard(board, msg)
            pygame.display.update()
            minmax(board, 0)
            update_board(board, choice, PLAYER_O)

            result = check_win_game(board)
            game_over = (result != CONT_GAME)

            if result == PLAYER_X:
                msg = "X wins!"
            elif result == PLAYER_O:
                msg = "O wins!"
            elif result == DRAW_GAME:
                msg = "Draw game"

            drawBoard(board, msg)
            pygame.display.update()


if __name__ == '__main__':
    main()
