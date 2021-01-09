"""
This is the main file of the project. It is used to handle user input and to display the game's GUI.
"""

# imports
import pygame as pg
import Engine

from utils import PIECES, IMAGES, SQUARE_SIZE, HEIGHT, WIDTH, DIMENSION, EMPTY_SQUARE, MAX_FPS


def init_images():
    """Initialize the IMAGES dictionary."""
    for piece in PIECES:
        IMAGES[piece] = pg.transform.scale(pg.image.load("pieces/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def draw_board(screen):
    """Draw the squares that make up the chess board"""
    colors = [pg.Color("white"), pg.Color("dark gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            pg.draw.rect(screen, color, pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board):
    """Draw the pieces on top of the chess board"""
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != EMPTY_SQUARE:  # check if we have a piece at this position
                screen.blit(IMAGES[piece], pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_state(screen, game_state):
    draw_board(screen)
    draw_pieces(screen, game_state.board)


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pg.Color("white"))
    clock = pg.time.Clock()
    game_state = Engine.GameState()
    init_images()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        draw_state(screen, game_state)
        clock.tick(MAX_FPS)
        pg.display.flip()


if __name__ == "__main__":
    main()
