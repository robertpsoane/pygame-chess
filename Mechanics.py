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
import pygame
import pygame_menu

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

class Text:

    def __init__(self,screen,screenwidth,y,size,text):
        pygame.init() 
        self.screen = screen
        self.width = screenwidth
        self.y = y
        self.text = text
        chosenFont = pygame.font.Font("Fonts/jackinp.ttf",size)
        self.chosenFont = chosenFont
        self.surf, self.rect = self.text_objects(text,self.chosenFont)
        self.rect.center = ((self.width/2),y)


    def text_objects(self,text,font):
        textSurface = font.render(text,True,(255,255,255))
        return textSurface, textSurface.get_rect()

    def display(self):
        self.screen.blit(self.surf,self.rect)


def mainMenu(screen):
    return 1
