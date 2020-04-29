# -*- coding: utf-8 -*-
"""
Board - Set of functions to manipulate chess board
Created on Fri Apr 24 14:17:59 2020

@author: Robert Soane
"""
import pygame
import numpy
from chessboard_data import cb_init as cb

Bwhite = 255, 218, 115
Bblack = 110, 80, 0


# class board
class board:

    def __init__(self, Pos, screen, grid):
        self.Pos = Pos
        self.screen = screen
        self.grid = grid
        self.set = cb
        self.squareSelection = 'null'

    def display(self):
        P = self.Pos
        s = P["size"]

        rows = ["1", "2", "3", "4", "5", "6", "7", "8"]
        columns = ["A", "B", "C", "D", "E", "F", "G", "H"]
        for x in range(0, 8):
            for y in range(0, 8):
                colour_indicator = (x+y) % 2
                if colour_indicator == 0:
                    col = Bblack
                elif colour_indicator == 1:
                    col = Bwhite

                pygame.draw.rect(
                    self.screen, col, (P[columns[x]], P[rows[y]], s, s)
                    )

    # Functions which deal with a screen press
    def mouseClick(self, click, sprites, tcount):
        pos = click.pos
        if self .checkClickInBoard(pos):
            # Converting from cartesian coordinates to chess board space reference
            square = self.detectSpace(pos)

            # Finding out what piece (if any) is on this space
            status = self.spaceStatus(square)

            # Implements action of click
            self.implementAction(square, sprites, status, tcount)

    
    # Returns which space in pos is pointing at
    def detectSpace(self, pos):
        grid = self.grid
        x = pos[0]
        y = pos[1]
        border = grid["border"]
        screensize = grid["screensize"]
        spacesize = grid["size"]

        # Changing reference frame to top left of board
        x -= border
        y -= border

        x_int = int(numpy.floor(x/spacesize))
        y_int = int(numpy.floor(y/spacesize))

        # Converting to chess board references
        rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
        cols = ["8", "7", "6", "5", "4", "3", "2", "1"]
        row = rows[x_int]
        col = cols[y_int]

        ref = row + col
        return ref
    
    # Checks whether mouse click was in the board
    def checkClickInBoard(self, pos):
        grid = self.grid
        x = pos[0]
        y = pos[1]
        border = grid["border"]
        screensize = grid["screensize"]
        outerlim = screensize - border

        if x > border and x < outerlim and y > border and y < outerlim:
            return True

    # Returns status of space - whether space is empty, or if occupied which piece
    # it is occupied by
    def spaceStatus(self, square):
        return self.set[square[0]][square[1]]

    def boardSetUpdate(self,initial,new):
        self.set[new[0]][new[1]] = self.set[initial[0]][initial[1]]
        self.set[initial[0]][initial[1]] = 'null'

    def implementAction(self, square, sprites, pieceKey, tcount):
        # square - chess coordinates for position clicked
        # sprites - dictionary of all sprites
        # pieceKey - 3 letter unique reference key of piece
        # tcount - turn counter from mechanics module
        
        turnPosition = tcount.turn
        
        if turnPosition == 'w':
            # White's turn to select a piece
            if pieceKey[0] == 'w':
                # White has selected a white piece
                sprites[pieceKey].select(tcount)
                tcount.change('q')
                # Updating board with selected square
                self.squareSelection = square
        elif turnPosition == 'q':
            # White has already selected a piece, now turn to place the piece
            if pieceKey[0] == 'w':
                # White has changed mind to another white piece
                # Deselecting previous selection
                sprites[tcount.pieceSelection].deselect(tcount)
                # Selecting new selection and udating board with selected square
                sprites[pieceKey].select(tcount)
                self.squareSelection = square

            if pieceKey == 'null':
                # White moves piece
                if self.movePiece(self.squareSelection, square, pieceKey, sprites, tcount,False) == True:
                    # Updating turn count
                    tcount.change("b")

            if pieceKey[0] == 'b':
                # White has attempted to take a black piece
                if self.movePiece(self.squareSelection, square, pieceKey, sprites, tcount,True) == True:
                    # Updating turn count
                    tcount.change("b")

        elif turnPosition == 'b':
            # Black's turn to select a piece
            if pieceKey[0] == 'b':
                # Black has selected a black piece
                sprites[pieceKey].select(tcount)
                tcount.change('v')
                # Updating board with selected square
                self.squareSelection = square
        elif turnPosition == 'v':
            # Black has already selected a piece, now turn to place the piece
            if pieceKey[0] == 'b':
                # Black has changed mind to another black piece
                # Deselecting previous selection
                sprites[tcount.pieceSelection].deselect(tcount)
                # Selecting new selection and udating board with selected square
                sprites[pieceKey].select(tcount)
                self.squareSelection = square
            if pieceKey == 'null':
                # Black moves piece
                if self.movePiece(self.squareSelection, square, pieceKey, sprites, tcount, False) == True:
                    # Updating turn count
                    tcount.change("w")                    

            if pieceKey[0] == 'w':
                # Black has attempted to take a white piece
                if self.movePiece(self.squareSelection, square, pieceKey, sprites, tcount, True) == True:
                    # Updating turn count
                    tcount.change("w")

    def movePiece(self, sourceSquare, targetSquare, targetPieceSelection, sprites, tcount, takeAttempt):
        # sourceSquare - selected square
        # targetSquare - square where player is attempting to move
        # targetPieceSelection - piece or null key for target square
        # sprites - dictionary containing all pieces
        # tcount - object containing turns counter, game record, and selected piece to move
        # takeAttmpt - boolean whether player is attempting to take a piece or not
        
        # unique 3-letter key of selected piece to be moved
        sourcePieceSelection = tcount.pieceSelection
        
        # Checking legality of move
        moveLegality = sprites[sourcePieceSelection].isMoveLegal(self.set,targetSquare,sprites,self)

        if moveLegality == True:
            # Adding move to history
            moveCode = sourceSquare+targetSquare
            tcount.gameRecord.append(moveCode)
            # Updating board map
            self.boardSetUpdate(sourceSquare,targetSquare)
            # Moving sprite
            sprites[tcount.pieceSelection].move(targetSquare)

            if takeAttempt == True:
                # Taking black piece
                sprites[targetPieceSelection].taken()
                tcount.gameRecord.append(targetPieceSelection)
                
            # Deselecting previous selection from board
            tcount.pieceSelection = 'null'
            self.squareSelection = 'null'
            return True


# Function which sets up board coordinate system based on chosen screen size
def define_board_positions(side, screen):
    border = side/10
    square = (side-2*border)/8
    mid = square/2

    Pos = {
            "A": border,
            "8": border,
            "B": border+square,
            "7": border+square,
            "C": border+2*square,
            "6": border+2*square,
            "D": border+3*square,
            "5": border+3*square,
            "E": border+4*square,
            "4": border+4*square,
            "F": border+5*square,
            "3": border+5*square,
            "G": border+6*square,
            "2": border+6*square,
            "H": border+7*square,
            "1": border+7*square,
            "size": int(square),
            "border": int(border),
            "screensize": int(side),
            "mid": mid
            }

    return Pos
