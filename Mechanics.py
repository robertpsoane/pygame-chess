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

    def __init__(self,screen,screenwidth,x,y,size,text):
        pygame.init() 
        self.screen = screen
        self.width = screenwidth
        self.y = y
        self.x = x
        if text == 'def':
            self.text = '>>'
        else:
            self.text = text
        chosenFont = pygame.font.Font("Fonts/printer.ttf",size)
        self.chosenFont = chosenFont
        self.surf, self.rect = self.text_objects(self.text,self.chosenFont)
        self.rect.topleft = (self.x,self.y)
        


    def text_objects(self,text,font):
        textSurface = font.render(text,True,(255,255,255))
        return textSurface, textSurface.get_rect()

    def display(self):
        self.screen.blit(self.surf,self.rect)
    
    def updateText(self,message):
        length = len(message)
        if length > 40:
            raise ValueError('Text can take max of 40 characters')
        else:
            centering = (40 - length)
            if centering % 2 == 1:
                # Odd number of characters
                beforeSpace = int(centering-1/2)
                afterSpace = int((centering-1/2)+1)
            else:
                beforeSpace = int(centering/2)
                afterSpace = int(centering/2)
            

            string = '>> '+message
            self.text = string
            self.surf, self.rect = self.text_objects(self.text,self.chosenFont)
            self.rect.topleft = (self.x,self.y)


class Communication(Text):

    def __init__(self,screen,screenwidth,x,y,size,text):
        Text.__init__(self,screen,screenwidth,x,y,size,text)
        self.state = 'null'
        self.run_me = True


    def keyboardInput(self,inputKey):
        state = self.state
        if inputKey == 'm' and state == 'null':
            self.mainMenu()
        elif inputKey == 'q' and state == 'menu':
            self.quitGame()
        elif inputKey == 't' and state == 'menu':
            self.changeTeam()
        elif inputKey == 'b' and state == 'menu':
            self.back()

    def mainMenu(self):
        self.updateText('q:quit b:back')
        self.state = 'menu'
    
    def quitGame(self):
        self.run_me = False

    def changeTeam(self):
        pass

    def back(self):
        self.updateText('')
        self.state = 'null'
