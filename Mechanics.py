# -*- coding: utf-8 -*-
"""
turns.turn can hold one of 4 values:
    w - white to move
    q - white to finish move
    b - black to move
    v - black to complete move


Created on Sat Apr 25 15:35:32 2020

@author: Robert Soane
"""


class turns:

    def __init__(self):
        self.turn = "w"
        self.turncounter = 0
        self.pieceSelection = "null"
        self.turnOptions = ['w', 'q', 'b', 'v']
        self.gameRecord = []

    def change(self,cinp):
        previousTurn = self.turn
        if cinp == 'w' and previousTurn == 'v':
            self.turncounter += 1
        self.turn = cinp
