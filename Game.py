"""
This is the main file of the project. It is used to handle user input and to display the game's GUI.
"""

# imports
import pygame as pg
import Engine

from utils import PIECES, IMAGES, SQUARE_SIZE, HEIGHT, WIDTH, DIMENSION, EMPTY_SQUARE, MAX_FPS


def init_images():
    """Initialize the IMAGES dictionary. Only needs to be called once, before the while loop."""
    for piece in PIECES:
        IMAGES[piece] = pg.transform.scale(pg.image.load("pieces/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def highlight_selection(screen, game_state, valid_positions, selected_square):
    """
    
    :param screen: 
    :param game_state: 
    :param valid_positions: 
    :param selected_square: 
    :return: 
    """
    if selected_square != ():
        row, col = selected_square
        if game_state.board[row][col][0] == ("w" if game_state.white_to_move else "b"):
            surface = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
            surface.set_alpha(100)
            surface.fill(pg.Color("light blue"))
            screen.blit(surface, (col*SQUARE_SIZE, row*SQUARE_SIZE))
            surface.fill(pg.Color("yellow"))
            for position in valid_positions:
                # print((position[1], position[0]))
                screen.blit(surface, (position[1]*SQUARE_SIZE, position[0]*SQUARE_SIZE))


def draw_board(screen):
    """Draw the squares that make up the chess board"""
    colors = [pg.Color("white"), pg.Color("dark gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            pg.draw.rect(screen, color, pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board):
    """
    Draw the pieces on top of the chess board
    :param screen:
    :param board:
    :return:
    """
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != EMPTY_SQUARE:  # check if we have a piece at this position
                screen.blit(IMAGES[piece], pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_state(screen, game_state, valid_positions, selected_square):
    """

    :param screen:
    :param game_state:
    :param valid_positions:
    :param selected_square:
    :return:
    """
    draw_board(screen)
    highlight_selection(screen, game_state, valid_positions, selected_square)
    draw_pieces(screen, game_state.board)


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pg.Color("white"))
    clock = pg.time.Clock()
    game_state = Engine.GameState()
    init_images()
    selected_square = ()  # Tuple used to record the position a player clicked (row, column). Starts empty.
    player_move = []  # List of two tuples that represent the starting square and the final square of a move.
    valid_positions = []
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()  # [X, Y] coordinates of a mouse click in the game window.
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                if selected_square == (row, col):  # player clicked the same square twice
                    selected_square = ()  # deselect the square
                    player_move = []  # reset the move
                else:
                    selected_square = (row, col)
                    player_move.append(selected_square)
                if len(player_move) == 2:  # the player has clicked to different squares and thus picked a move
                    if game_state.check_valid_move(player_move):
                        game_state.register_move(player_move)
                        print(game_state.moves_log)
                    selected_square = ()  # reset the selected_square tuple
                    player_move = []  # reset the player_move list
                    # print(game_state.board)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    game_state.undo_move()
        if selected_square != ():
            valid_moves = game_state.get_valid_moves()
            for valid_moves_index in range(len(valid_moves) - 1, -1, -1):
                if valid_moves[valid_moves_index][0] == selected_square:
                    valid_positions.append(valid_moves[valid_moves_index][1])
        draw_state(screen, game_state, valid_positions,
                   selected_square)
        valid_positions = []
        clock.tick(MAX_FPS)
        pg.display.flip()


if __name__ == "__main__":
    main()
