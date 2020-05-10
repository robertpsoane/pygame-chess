import pygame
from chessFunc import ChessGame as cg

class textString:

    def __init__(self,screen,screenX,screenY,size,text,colour = (255,255,255)):
        pygame.init() 
        self.screen = screen
        self.width = screenX
        self.height = screenY
        self.y = screenY
        self.x = int(round(screenX/2))
        if text == 'def':
            self.text = '>>'
        else:
            self.text = text
        self.font = pygame.font.Font("Fonts/printer.ttf",size)
        self.surf, self.rect = self.text_objects(self.text,self.font,colour)
        self.rect.center = (self.x,self.y)
    
    def text_objects(self,text,font,colour):
        textSurface = font.render(text,True,colour)
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
            self.rect.center = (self.x,self.y)

class startMenu():

    def __init__(self,screen,t1,t2,t3,t4):
        self.state = 'null'
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        self.screen = screen
        self.play = True

    def display(self):
        self.screen.blit(self.t1.surf,self.t1.rect)
        self.screen.blit(self.t2.surf,self.t2.rect)
        self.screen.blit(self.t3.surf,self.t3.rect)
        self.screen.blit(self.t4.surf,self.t4.rect)


    def do(self,k):
        if k == '1':
            cg('w')
        elif k == '2':
            cg('b')
        elif k == '4':
            self.play = False
        elif k = '3':
            print('Online play isnt functional')
