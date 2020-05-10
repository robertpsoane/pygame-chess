# -*- coding: utf-8 -*-
"""
Chess v0.3

All pieces understand basic moves

Next:
    - Play as black, option, new game

Future plans:
    - Undo Function
    - Options - play as black, new game

Distant future:
    - Online

Created on Fri Apr 24 14:04:36 2020

@author: Robert Soane
"""

# Importing pygame
import pygame
import Board
import Pieces
import Mechanics


GameName = 'Chess'

# Setting up basic colour variables
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

# Defining Screen size
SIDE_SIZE = 700
screen_size = SIDE_SIZE, SIDE_SIZE


# Setting up display and clock
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption(GameName)

# COnverting from cartesian to chess coordinates
team = 'b'
gridPositions = Board.define_board_positions(SIDE_SIZE, screen, team)

# Initialising pieces
pieces_sprites = Pieces.load_pieces(gridPositions["size"])

# Creating white and black groups
white_pieces = pygame.sprite.Group()
black_pieces = pygame.sprite.Group()

sprites = Pieces.initial_setup_board(
    screen, white_pieces, black_pieces, gridPositions, pieces_sprites
    )

# Setting up chess board
chessBoard = Board.board(gridPositions, screen, gridPositions)

# Setting up turns
tcount = Mechanics.turns()

# Setting up text
textSize = int(round(SIDE_SIZE/30))
textHeight = int(round(SIDE_SIZE - textSize))

# Setting up instructions text
instructString = 'm:menu'
instructionsText = Mechanics.Text(screen,SIDE_SIZE,0,0,textSize,instructString)
instructionsText.rect.center = (int(round(SIDE_SIZE/2)),textSize)

# Setting up output text
communicator = Mechanics.Communication(screen,SIDE_SIZE,0,textHeight,textSize,'def')

# adding communicator to chessboard
chessBoard.communicator = communicator

# Defining frame-rate and running loop
fps = 60
run_me = True

# Main game loop
while communicator.run_me:
    # Limit frame rate
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            communicator.run_me = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Detecting mouse selection of pieces
            # Run mouseCLick function
            chessBoard.mouseClick(event, sprites, tcount)
        
        if event.type == pygame.KEYDOWN:
            # Detecting key press
            communicator.keyboardInput(event.unicode)

    # Clear screen
    screen.fill(black)

    # Remake Board
    chessBoard.display()
    white_pieces.draw(screen)
    black_pieces.draw(screen)
    communicator.display()
    instructionsText.display()

    # Display everything on screen
    pygame.display.flip()

# Quit game
