# -*- coding: utf-8 -*-
"""
Board - Set of functions to manipulate chess board
Created on Fri Apr 24 14:17:59 2020

@author: Robert Soane
"""
import pygame
import numpy
from chessboard_data import cb_init as cb
import Pieces

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

    def boardMapUpdate(self,initial,new):
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
        moveLegality = sprites[sourcePieceSelection].isMoveLegal(self.set,targetSquare,sprites)

        # If standard legal move
        if moveLegality == True:
            
            # Checking for possible Pawn Upgrade
            if (targetSquare[1] == '8' and tcount.pieceSelection[0:2] == 'wp') or (targetSquare[1] == '1' and tcount.pieceSelection[0:2] == 'bp'):
                # Pawn Upgrade
                # Adding move to history
                moveCode = sourceSquare+targetSquare
                tcount.gameRecord.append(moveCode)
                # Updating board map
                self.boardMapUpdate(sourceSquare,targetSquare)
                
                # Removing pawn from board
                pawn = tcount.pieceSelection
                pawnSprite = sprites[pawn]
                pawnGroup = pawnSprite.tgroup
                pawnSprite.taken()
                
                # Setting up queen code
                queenCode = pawn[0] + 'q' + pawn[2]
                self.set[targetSquare[0]][targetSquare[1]] = queenCode
                Pieces.initialSetup[queenCode] = [targetSquare[0],targetSquare[1],"queen"]

                # Placing queen on board
                sprites[queenCode] = Pieces.Queen(pawnSprite.screen,pawnSprite.pos,pawnSprite.images,queenCode,pawnGroup,pawnGroup)
                pawnGroup.add(sprites[queenCode])

                if takeAttempt == True:
                    # Taking black piece
                    sprites[targetPieceSelection].taken()
                    tcount.gameRecord.append(targetPieceSelection)
                    
                # Deselecting previous selection from board
                tcount.pieceSelection = 'null'
                self.squareSelection = 'null'
                return True

            else:
                # Adding move to history
                moveCode = sourceSquare+targetSquare
                tcount.gameRecord.append(moveCode)
                # Updating board map
                self.boardMapUpdate(sourceSquare,targetSquare)
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
        else:
            specialMove = self.checkSpecialMove(sourceSquare, targetSquare, targetPieceSelection, sprites, tcount)
            if specialMove is True:
                return True
            else:
                return False

    
    def checkSpecialMove(self,source,target,targetPiece,sprites,tcount):
        map = self.set
        sourcePiece = tcount.pieceSelection
        sourcePieceSprite = sprites[sourcePiece]
        # First check - checking for attempted castling
        # If attempting to move a king, that hasn't moved that isn't in check
        if sourcePiece[1] == 'k' and sourcePieceSprite.hasMoved is False and sourcePieceSprite.isCheck(map,source,source) is False:
            king = sourcePieceSprite
            # Only possible special move is castling
            # Case by case, starting with white
            if sourcePiece[0] == 'w':
                # Checking king side castle, and rook hasn't moved
                if target == 'G1' and sprites['wr2'].hasMoved is False:
                    rookSprite = sprites['wr2']
                    # Checking F1 has is vacant and not in check
                    if map['F']['1'] == 'null' and sourcePieceSprite.isCheck(map,source,'F1') is False:
                        # Checking G1 has is vacant and not in check
                        if map['G']['1'] == 'null' and sourcePieceSprite.isCheck(map,source,'G1') is False:
                            # Now can castle, kings side
                            # Adding move to history
                            moveCode = 'OO-w'
                            tcount.gameRecord.append(moveCode)
                            # Updating board map
                            map['E']['1'] = 'null'
                            map['H']['1'] = 'null'
                            map['F']['1'] = 'wr2'
                            map['G']['1'] = 'wki'
                            # Moving sprite
                            king.move(target)
                            rookSprite.move('F1')
                            # Deselecting previous selection from board
                            tcount.pieceSelection = 'null'
                            self.squareSelection = 'null'
                            return True
                if target == 'C1' and sprites['wr1'].hasMoved is False:
                    rookSprite = sprites['wr1']
                    # Checking F1 has is vacant and not in check
                    if map['D']['1'] == 'null' and sourcePieceSprite.isCheck(map,source,'D1') is False:
                        # Checking G1 has is vacant and not in check
                        if map['C']['1'] == 'null' and sourcePieceSprite.isCheck(map,source,'C1') is False:
                            # Now can castle, Queen side
                            # Adding move to history
                            moveCode = 'OOOw'
                            tcount.gameRecord.append(moveCode)
                            # Updating board map
                            map['E']['1'] = 'null'
                            map['A']['1'] = 'null'
                            map['D']['1'] = 'wr1'
                            map['C']['1'] = 'wki'
                            # Moving sprite
                            king.move(target)
                            rookSprite.move('D1')
                            # Deselecting previous selection from board
                            tcount.pieceSelection = 'null'
                            self.squareSelection = 'null'
                            return True
            else:
                # Checking king side castle, and rook hasn't moved
                if target == 'G8' and sprites['br2'].hasMoved is False:
                    rookSprite = sprites['br2']
                    # Checking F1 has is vacant and not in check
                    if map['F']['8'] == 'null' and sourcePieceSprite.isCheck(map,source,'F8') is False:
                        # Checking G1 has is vacant and not in check
                        if map['G']['8'] == 'null' and sourcePieceSprite.isCheck(map,source,'G8') is False:
                            # Now can castle, kings side
                            # Adding move to history
                            moveCode = 'OO-b'
                            tcount.gameRecord.append(moveCode)
                            # Updating board map
                            map['E']['8'] = 'null'
                            map['H']['8'] = 'null'
                            map['F']['8'] = 'br2'
                            map['G']['8'] = 'bki'
                            # Moving sprite
                            king.move(target)
                            rookSprite.move('F8')
                            # Deselecting previous selection from board
                            tcount.pieceSelection = 'null'
                            self.squareSelection = 'null'
                            return True
                if target == 'C8' and sprites['br1'].hasMoved is False:
                    rookSprite = sprites['br1']
                    # Checking F1 has is vacant and not in check
                    if map['D']['8'] == 'null' and sourcePieceSprite.isCheck(map,source,'D8') is False:
                        # Checking G1 has is vacant and not in check
                        if map['C']['8'] == 'null' and sourcePieceSprite.isCheck(map,source,'C8') is False:
                            # Now can castle, Queen side
                            # Adding move to history
                            moveCode = 'OOOw'
                            tcount.gameRecord.append(moveCode)
                            # Updating board map
                            map['E']['8'] = 'null'
                            map['A']['8'] = 'null'
                            map['D']['8'] = 'br1'
                            map['C']['8'] = 'wki'
                            # Moving sprite
                            king.move(target)
                            rookSprite.move('D8')
                            # Deselecting previous selection from board
                            tcount.pieceSelection = 'null'
                            self.squareSelection = 'null'
                            return True
        elif sourcePiece[1] == 'p':
            # Checking for possible En Passant
            history = tcount.gameRecord
            previousMove = history[len(history) - 1]
            if sourcePiece[0] == 'w' and source[1] == '5':
                if target[0] == previousMove[0] and previousMove[3] == source[1] and previousMove[1] == '7':
                    previousPiece = map[previousMove[2]][previousMove[3]]
                    if previousPiece[0] == 'b' and previousPiece[1] == 'p':
                        # Generating false board map to check if en passant would cause check
                        previousMoveEnd = previousMove[2:4]
                        takingPiece = map[source[0]][source[1]]
                        checkMap = map.copy()
                        checkMap[previousMoveEnd[0]][previousMoveEnd[1]] = 'null'
                        checkMap[source[0]][source[1]] = 'null'
                        checkMap[target[0]][target[1]] = takingPiece
                        kingCoords = sprites['wki'].square
                        checkCheck = sprites['wki'].isCheck(checkMap,kingCoords,kingCoords)
                        if checkCheck is False:
                            self.enPassant(sprites,takingPiece,source,target,previousMoveEnd,previousPiece,tcount)
                            return True
            if sourcePiece[0] == 'b' and source[1] == '4':
                if target[0] == previousMove[0] and previousMove[3] == source[1] and previousMove[1] == '2':
                    previousPiece = map[previousMove[2]][previousMove[3]]
                    if previousPiece[0] == 'w' and previousPiece[1] == 'p':
                        # Generating false board map to check if en passant would cause check
                        previousMoveEnd = previousMove[2:4]
                        takingPiece = map[source[0]][source[1]]
                        checkMap = map.copy()
                        checkMap[previousMoveEnd[0]][previousMoveEnd[1]] = 'null'
                        checkMap[source[0]][source[1]] = 'null'
                        checkMap[target[0]][target[1]] = takingPiece
                        kingCoords = sprites['bki'].square
                        checkCheck = sprites['bki'].isCheck(checkMap,kingCoords,kingCoords)
                        if checkCheck is False:
                            self.enPassant(sprites,takingPiece,source,target,previousMoveEnd,previousPiece,tcount)
                            return True

    def enPassant(self,sprites,attackingPiece,attackingSource,attackingTarget,defendingPosition,defendingPiece,tcount):
        # Adding move to history
        moveCode = attackingSource + attackingTarget
        tcount.gameRecord.append(moveCode)
        # Updating board map
        self.set[defendingPosition[0]][defendingPosition[1]] = 'null'
        self.set[attackingSource[0]][attackingSource[1]] = 'null'
        self.set[attackingTarget[0]][attackingTarget[1]] = attackingPiece

        # Moving sprites
        sprites[attackingPiece].move(attackingTarget)
        sprites[defendingPiece].taken()
        # Deselecting previous selection from board
        tcount.pieceSelection = 'null'
        self.squareSelection = 'null'
                            
                


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
