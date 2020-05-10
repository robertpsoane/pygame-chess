# -*- coding: utf-8 -*-
"""
Chess v1

Needs online play
    - Online

Created on Fri Apr 24 14:04:36 2020

@author: Robert Soane
"""

# Importing pygame
import pygame
import startMenu
from chessFunc import ChessGame as cg

# Setting up basic colour variables
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

# Defining Screen size
screen_size = screen_width, screen_height = 700, 700      
        
# Setting up display and clock
clientScreen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption('Chess Client')

# Defining menu

Title = startMenu.textString(clientScreen,screen_width,screen_height/5,50,'Chess',green)

text = ['1: Play as White','2: Play as Black','3: Play Online','4: Quit']
nOptions = len(text)
divisor = nOptions+2
text1 = startMenu.textString(clientScreen,screen_width,2*screen_height/divisor,30,text[0])
text2 = startMenu.textString(clientScreen,screen_width,3*screen_height/divisor,30,text[1])
text3 = startMenu.textString(clientScreen,screen_width,4*screen_height/divisor,30,text[2])
text4 = startMenu.textString(clientScreen,screen_width,5*screen_height/divisor,30,text[3])

menuController = startMenu.startMenu(clientScreen,text1,text2,text3,text4)

# Defining frame-rate and running loop
fps = 60

while menuController.play:
    # Limit frame rate
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menuController.play = False
        
        if event.type == pygame.KEYDOWN:
            menuController.do(event.unicode)
    
    # Clear screen
    clientScreen.fill(black)
    
    Title.display()
    menuController.display()

    #Display everything on screen
    pygame.display.flip()
    
# Quit game