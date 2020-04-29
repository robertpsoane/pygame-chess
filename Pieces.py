# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:52:28 2020

@author: Robert Soane
"""
import pygame
from spritesheet import SpriteSheet
from chessboard_data import coordconversion as coordcon
from chessboard_data import wbt as wb


TRANS = (63,72,204)

###### Data about initial pieces setup ######
initialSetup = {
        
        "wp1" : ["A","2","pawn"],
        "wp2" : ["B","2","pawn"],
        "wp3" : ["C","2","pawn"],
        "wp4" : ["D","2","pawn"],
        "wp5" : ["E","2","pawn"],
        "wp6" : ["F","2","pawn"],
        "wp7" : ["G","2","pawn"],
        "wp8" : ["H","2","pawn"],
        "wr1" : ["A","1","rook"],
        "wr2" : ["H","1","rook"],
        "wn1" : ["B","1","knight"],
        "wn2" : ["G","1","knight"],
        "wb1" : ["C","1","bishop"],
        "wb2" : ["F","1","bishop"],
        "wqu" : ["D","1","queen"],
        "wki" : ["E","1","king"],        
        "bp1" : ["A","7","pawn"],
        "bp2" : ["B","7","pawn"],
        "bp3" : ["C","7","pawn"],
        "bp4" : ["D","7","pawn"],
        "bp5" : ["E","7","pawn"],
        "bp6" : ["F","7","pawn"],
        "bp7" : ["G","7","pawn"],
        "bp8" : ["H","7","pawn"],
        "br1" : ["A","8","rook"],
        "br2" : ["H","8","rook"],
        "bn1" : ["B","8","knight"],
        "bn2" : ["G","8","knight"],
        "bb1" : ["C","8","bishop"],
        "bb2" : ["F","8","bishop"],
        "bqu" : ["D","8","queen"],
        "bki" : ["E","8","king"]
        
        }

white_setup_keys = ["wp1","wp2","wp3","wp4","wp5","wp6","wp7","wp8","wr1","wr2","wn1","wn2","wb1","wb2","wqu","wki"]
black_setup_keys = ["bp1","bp2","bp3","bp4","bp5","bp6","bp7","bp8","br1","br2","bn1","bn2","bb1","bb2","bqu","bki"]



### Chesspiece class ###
class Chesspiece(pygame.sprite.Sprite):
    
    def __init__(self, screen, pos, images,pref):
        # Declaring self to be a sprite
        pygame.sprite.Sprite.__init__(self)
        
        # initialPosition = starting position of piece from initialSetup dict
        # self.col = column in chess notation
        # self.row = row in chess notation
        # self.square = position in chess notation
        # self.pref = unique 3-letter piece reference
        # self.team  = 'w' or 'b'
        # self.hasMoved = boolean telling whether piece has moved from initial position
        initialPosition = initialSetup[pref]
        self.col = initialPosition[0]
        self.row = initialPosition[1]
        self.square = self.col+self.row
        self.pref = pref
        self.team = pref[0]
        self.hasMoved = False

        # self.image = image of piece
        # self.rect = set-up rect for piece
        # self.screen = screen piece is on
        imref = pref[0]+"_"+initialPosition[2]
        self.image = images[imref]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos[self.col],pos[self.row]]
        self.screen = screen
        
        # self.squareSize is size of individual square in pixels
        # self.grid is the cartesian coords of the chess notation
        self.squareSize = pos["size"]
        self.grid = pos
        self.possibleMoves = []
        
    def display(self):
        self.screen.blit(self.image,self.rect)

    def select(self,turnCounter):
        colour = self.pref[0]
        deselectedPosX = self.rect.topleft[0]
        deselectedPosY = self.rect.topleft[1]
        change = self.squareSize/7
        turnCounter.pieceSelection = self.pref
        if colour == "w":
            self.rect.topleft = [deselectedPosX,deselectedPosY-change]
        else:
            self.rect.topleft = [deselectedPosX,deselectedPosY+change]
    
    def deselect(self,turnCounter):
        colour = self.pref[0]
        deselectedPosX = self.rect.topleft[0]
        deselectedPosY = self.rect.topleft[1]
        change = self.squareSize/7
        turnCounter.pieceSelection = "null"
        if colour == "w":
            self.rect.topleft = [deselectedPosX,deselectedPosY+change]
        else:
            self.rect.topleft = [deselectedPosX,deselectedPosY-change]

    def move(self,target):
        moveX = self.grid[target[0]]
        moveY = self.grid[target[1]]
        self.rect.topleft = [moveX,moveY]
        self.square = target
        self.col = target[0]
        self.row = target[1]
        self.hasMoved = True
    
    def taken(self):
        self.kill()

    def isMoveLegal(self,map,target,sprites,board):
        # Checks whether move is legal or not.
        # Checks whether target square is on the list returned from 
        # legal moves function, then produces a provisional map 
        # of the board and checks whether king would be left in check
        # if target is on the list of possible moves, and king not in check,
        # returns True.  Else, returns False.
        
        moves = self.legalMoves(map)
        inMoves = target in moves
        if inMoves == True:
            # Setting up potential future map
            furureMap = map
            futureMap[target[0]][target[1]] = self.pref
            futureMap[self.col][self.row] = 'null'
            teamKingCoords = sprites[self.team+'ki'].square
            check = self.isCheck(futureMap,teamKingCoords,teamKingCoords)
            if check == False:
                return True
            else:
                return False
        else:
            return False

    def isCheck(self,map,currentKingSquare,querySquare):
        # Given a map, returns a boolean as to whether the king would be
        # in check at the query square.  If currentKingSquare = querySquare,
        # determines whether king is currently in check
        team = self.team

        # Moving king to square being queried
        if currentKingSquare != querySquare:
            remap = map
            remap[currentKingSquare[0]][currentKingSquare[1]] = 'null'
            remap[querySquare[0]][querySquare[1]] = team+'ki'
        else:
            remap = map
         #Algorith similar to directionalSearch


    def directionalSearch(self, map, direction, square, recurse):
        # Recursive function to find all possible spaces moving 
        # directly in a specific direction.
        # Iterates once in that direction, checks next space is
        # on the board, then checks if the space is empty or
        # contains a piece of the opposite team
        possibleDirections = {
            'north': (0,1),
            'north-east': (1,1),
            'east': (1,0),
            'south-east': (1,-1),
            'south': (0, -1),
            'south-west': (-1,-1),
            'west': (-1, 0),
            'north-west': (-1, 1),
            'k1': (1,2),
            'k2': (2,1),
            'k3': (2,-1),
            'k4': (1,-2),
            'k5': (-1,-2),
            'k6': (-2,-1),
            'k7': (-1,2),
            'k8': (-2,1)
        }
        x = square[0]
        y = square[1]
        iterativeVector = possibleDirections[direction]

        # Iterating once in given direction
        x = coordcon["l2n"][x]
        x += iterativeVector[0]
        y = int(y)
        y += iterativeVector[1]
           
        # Checking still on board
        if y < 9 and x < 9 and y > 0 and x > 0:
            y = str(y)
            x = coordcon["n2l"][str(x)]
            testSquare = x+y
            # checking square is empty or opposite team
            if self.emptyOrOtherTeam(map,testSquare) is True:
                self.possibleMoves.append(testSquare)
                if recurse is True:
                    self.directionalSearch(map, direction, testSquare,recurse)

 
    def emptyOrOtherTeam(self, map, square):
        # returns true if square is empty or occupied by a member of 
        # the other team, else reutrns false
        squareStatus = map[square[0]][square[1]]
        team = self.team
        if squareStatus == 'null':
            return True
        elif squareStatus[0] != team:
            return True
        else:
            return False


class King(Chesspiece):
    
    def __init__(self,screen,pos,sprites,pref):
        Chesspiece.__init__(self,screen,pos,sprites,pref)
        self.directions = [
            'north',
            'north-east',
            'east',
            'south-east',
            'south',
            'south-west',
            'west',
            'north-west'
            ]

    def legalMoves(self,map):
        directions = self.directions
        position = self.square
        self.possibleMoves = []
        for direction in directions:
            self.directionalSearch(map, direction, position, recurse = False)
        return self.possibleMoves            


class Queen(Chesspiece):
    
    def __init__(self,screen,pos,sprites,pref):
        Chesspiece.__init__(self,screen,pos,sprites,pref)
        self.directions = [
            'north',
            'north-east',
            'east',
            'south-east',
            'south',
            'south-west',
            'west',
            'north-west'
            ]

    def legalMoves(self,map):
        directions = self.directions
        position = self.square
        self.possibleMoves = []
        for direction in directions:
            self.directionalSearch(map, direction, position, recurse = True)
        return self.possibleMoves


class Bishop(Chesspiece):
    
    def __init__(self,screen,pos,sprites,pref):
        Chesspiece.__init__(self,screen,pos,sprites,pref)
        self.directions = [
            'north-east',
            'south-east',
            'south-west',
            'north-west'
            ]

    def legalMoves(self,map):
        directions = self.directions
        position = self.square
        self.possibleMoves = []
        for direction in directions:
            self.directionalSearch(map, direction, position, recurse = True)
        return self.possibleMoves
        

class Knight(Chesspiece):
    
    def __init__(self,screen,pos,sprites,pref):
        Chesspiece.__init__(self,screen,pos,sprites,pref)
        self.directions = [
            'k1',
            'k2',
            'k3',
            'k4',
            'k5',
            'k6',
            'k7',
            'k8'
            ]

    def legalMoves(self,map):
        directions = self.directions
        position = self.square
        self.possibleMoves = []
        for direction in directions:
            self.directionalSearch(map, direction, position, recurse = False)
        return self.possibleMoves


class Rook(Chesspiece):
    
    def __init__(self,screen,pos,sprites,pref):
        Chesspiece.__init__(self,screen,pos,sprites,pref)
        self.directions = [
            'north',
            'east',
            'south',
            'west',
            ]

    def legalMoves(self,map):
        directions = self.directions
        position = self.square
        self.possibleMoves = []
        for direction in directions:
            self.directionalSearch(map, direction, position, recurse = True)
        return self.possibleMoves


class Pawn(Chesspiece):
    
    def __init__(self,screen,pos,sprites,pref):
        Chesspiece.__init__(self,screen,pos,sprites,pref)

    def legalMoves(self,map):
        # Tests for legal moves case by case
        # Recalling current position of pawn
        position = self.square
        self.possibleMoves = []

        # Converting coords to integers
        x = coordcon['l2n'][position[0]]
        y = int(position[1])
        # Pawn team determines which direction it can move in
        if self.team == 'w':
            # 1 step forward
            y += 1
            if y < 9:
                targetX = position[0]
                targetY = str(y)
                targetSqr = targetX+targetY
                if map[targetX][targetY] == 'null':
                    self.possibleMoves.append(targetSqr)
                # Checking diagonal taking
                if x - 1 > 0:
                    targetX = coordcon['n2l'][str(x-1)]
                    targetSqr = targetX+targetY
                    targetPiece = map[targetX][targetY]
                    if targetPiece[0] == 'b':
                        self.possibleMoves.append(targetSqr)
                if x + 1 < 9:
                    targetX = coordcon['n2l'][str(x+1)]
                    targetSqr = targetX+targetY
                    targetPiece = map[targetX][targetY]
                    if targetPiece[0] == 'b':
                        self.possibleMoves.append(targetSqr)
            # First move 2 steps
            if self.hasMoved == False:
                y += 1
                targetX = position[0]
                targetY = str(y)
                targetSqr = targetX+targetY
                if map[targetX][targetY] == 'null':
                    self.possibleMoves.append(targetSqr)
            

        elif self.team == 'b':
            # 1 step forward
            y -= 1
            if y > 0:
                targetX = position[0]
                targetY = str(y)
                targetSqr = targetX+targetY
                if map[targetX][targetY] == 'null':
                    self.possibleMoves.append(targetSqr)
                # Checking diagonal taking
                if x - 1 > 0:
                    targetX = coordcon['n2l'][str(x-1)]
                    targetSqr = targetX+targetY
                    targetPiece = map[targetX][targetY]
                    if targetPiece[0] == 'w':
                        self.possibleMoves.append(targetSqr)
                if x + 1 < 9:
                    targetX = coordcon['n2l'][str(x+1)]
                    targetSqr = targetX+targetY
                    targetPiece = map[targetX][targetY]
                    if targetPiece[0] == 'w':
                        self.possibleMoves.append(targetSqr)
            # First move 2 steps
            if self.hasMoved == False:
                y -= 1
                targetX = position[0]
                targetY = str(y)
                targetSqr = targetX+targetY
                if map[targetX][targetY] == 'null':
                    self.possibleMoves.append(targetSqr)

        return self.possibleMoves
        
        
### function loading pieces pictures 
def load_pieces(square_size):
    # Loading sprite sheet
    ss = SpriteSheet('Sprites/Pieces_trans.png')
    
    # Storing each image in directory
    # Kings
    w_king = pygame.transform.scale(ss.image_at((0,0,200,200)),(square_size,square_size))
    w_king.set_colorkey(TRANS)
    b_king = pygame.transform.scale(ss.image_at((0,200,200,200)),(square_size,square_size))
    b_king.set_colorkey(TRANS)
    
    # Queens
    w_queen = pygame.transform.scale(ss.image_at((200,0,200,200)),(square_size,square_size))
    w_queen.set_colorkey(TRANS)
    b_queen = pygame.transform.scale(ss.image_at((200,200,200,200)),(square_size,square_size))
    b_queen.set_colorkey(TRANS)
    
    # Bishops
    w_bishop = pygame.transform.scale(ss.image_at((400,0,200,200)),(square_size,square_size))
    w_bishop.set_colorkey(TRANS)
    b_bishop = pygame.transform.scale(ss.image_at((400,200,200,200)),(square_size,square_size))
    b_bishop.set_colorkey(TRANS)
    
    # Knights
    w_knight = pygame.transform.scale(ss.image_at((600,0,200,200)),(square_size,square_size))
    w_knight.set_colorkey(TRANS)
    b_knight = pygame.transform.scale(ss.image_at((600,200,200,200)),(square_size,square_size))
    b_knight.set_colorkey(TRANS)
    
    # Rook
    w_rook = pygame.transform.scale(ss.image_at((800,0,200,200)),(square_size,square_size))
    w_rook.set_colorkey(TRANS)
    b_rook = pygame.transform.scale(ss.image_at((800,200,200,200)),(square_size,square_size))
    b_rook.set_colorkey(TRANS)
    
    # Pawn
    w_pawn = pygame.transform.scale(ss.image_at((1000,0,200,200)),(square_size,square_size))
    w_pawn.set_colorkey(TRANS)
    b_pawn = pygame.transform.scale(ss.image_at((1000,200,200,200)),(square_size,square_size))
    b_pawn.set_colorkey(TRANS)
    
    pieces = {
            
            "w_king" : w_king,
            "b_king" : b_king,
            "w_queen" : w_queen,
            "b_queen" : b_queen,
            "w_bishop" : w_bishop,
            "b_bishop" : b_bishop,
            "w_knight" : w_knight,
            "b_knight" : b_knight,
            "w_rook" : w_rook,
            "b_rook" : b_rook,
            "w_pawn" : w_pawn,
            "b_pawn" : b_pawn
            
            }
    
    return pieces

# Placing sprites on board
def initial_setup_board(screen,whitegroup,blackgroup,pos,images):
    sprite_dict = {}
    # Queens
    sprite_dict['wqu'] = Queen(screen,pos,images,'wqu')
    whitegroup.add(sprite_dict['wqu'])
    sprite_dict['bqu'] = Queen(screen,pos,images,'bqu')
    blackgroup.add(sprite_dict['bqu'])
    
    #Kings
    sprite_dict['wki'] = King(screen,pos,images,'wki')
    whitegroup.add(sprite_dict['wki'])
    sprite_dict['bki'] = King(screen,pos,images,'bki')
    blackgroup.add(sprite_dict['bki'])

    #Bishop
    sprite_dict['wb1'] = Bishop(screen,pos,images,'wb1')
    whitegroup.add(sprite_dict['wb1'])
    sprite_dict['wb2'] = Bishop(screen,pos,images,'wb2')
    whitegroup.add(sprite_dict['wb2'])
    sprite_dict['bb1'] = Bishop(screen,pos,images,'bb1')
    blackgroup.add(sprite_dict['bb1'])
    sprite_dict['bb2'] = Bishop(screen,pos,images,'bb2')
    blackgroup.add(sprite_dict['bb2'])
    
    #Knight
    sprite_dict['wn1'] = Knight(screen,pos,images,'wn1')
    whitegroup.add(sprite_dict['wn1'])
    sprite_dict['wn2'] = Knight(screen,pos,images,'wn2')
    whitegroup.add(sprite_dict['wn2'])
    sprite_dict['bn1'] = Knight(screen,pos,images,'bn1')
    blackgroup.add(sprite_dict['bn1'])
    sprite_dict['bn2'] = Knight(screen,pos,images,'bn2')
    blackgroup.add(sprite_dict['bn2'])
    
    #Rook
    sprite_dict['wr1'] = Rook(screen,pos,images,'wr1')
    whitegroup.add(sprite_dict['wr1'])
    sprite_dict['wr2'] = Rook(screen,pos,images,'wr2')
    whitegroup.add(sprite_dict['wr2'])
    sprite_dict['br1'] = Rook(screen,pos,images,'br1')
    blackgroup.add(sprite_dict['br1'])
    sprite_dict['br2'] = Rook(screen,pos,images,'br2')
    blackgroup.add(sprite_dict['br2'])
    
    #Pawns
    white_pawn_keys = ["wp1","wp2","wp3","wp4","wp5","wp6","wp7","wp8"]
    black_pawn_keys = ["bp1","bp2","bp3","bp4","bp5","bp6","bp7","bp8"]
    
    for key in white_pawn_keys:
        sprite_dict[key] = Pawn(screen,pos,images,key)
        whitegroup.add(sprite_dict[key])
        
    for key in black_pawn_keys:
        sprite_dict[key] = Pawn(screen,pos,images,key)
        blackgroup.add(sprite_dict[key])
        
    return sprite_dict