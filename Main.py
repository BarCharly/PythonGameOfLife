# -*- coding: utf-8 -*-
"""
Created on Mon May  4 23:20:15 2020

Last build Thu May  7 10:19 2020

Conways game of life made with pygame library
@author: Carlos
"""

import pygame
import sys
from pygame.locals import *
import numpy as np

import confunct as con
import conUI as UI

pygame.init()

#File Loading
headerImg = pygame.image.load('header.png')
variantImg = pygame.image.load('variantButton.png')
classicImg = pygame.image.load('classicButton.png')
goImg = pygame.image.load('goButton.png')
stopImg = pygame.image.load('stopButton.png')
stepImg = pygame.image.load('stepButton.png')
randomImg = pygame.image.load('randomButton.png')
clearImg = pygame.image.load('clearButton.png')

#Variables definition
BLACK = (0,0,0)
DARK = (35, 35, 38)
LGRAY = (200, 200, 200)
DGRAY = (150, 150, 150)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
OCEAN = (1, 11, 167)
CERULEAN = (0,123,167)
CYAN = (0, 219, 167)
NAVY = (0, 0, 128)
FOAM = (223, 224, 235)


cellSize = 16
LINEWIDTH = 2

#the gameState object is a set describes general conditions of the game 
class GameState:
    def __init__(self,running,rules,doStep,doRandom,clear):
        self.running = running
        self.rules = rules
        self.doStep = doStep
        self.doRandom = doRandom
        self.clear = clear
        self.buttonPressed = False
        
gameState = GameState(False,'Classic',False,False, False);


cellColour = CYAN

#set up FPS count
FPS = 10 #will be set to 6 for my rules as it is to fast for them
fpsClock = pygame.time.Clock()
#create display window
background = OCEAN
screensize = (1000,600)#width of screen must be 200 or more pixels
DISPLAYSURF = pygame.display.set_mode(screensize)
size = (screensize[0]-200,screensize[1])
pygame.display.set_caption('Game of Life')
DISPLAYSURF.fill(background)

#create states array,prep grid and generate colliders 
states = con.generateStates(size,cellSize,LINEWIDTH)
grid = con.buildGrid(states,cellSize,LINEWIDTH,CERULEAN,background)
colliders = con.generateColliders(states,cellSize,LINEWIDTH)
DISPLAYSURF.blit(grid,(0,0))
#define the life square
cell = pygame.Rect(0,0,cellSize,cellSize)
#create UI buttons
interface = UI.Interface();
variantButton = UI.Button(interface,(screensize[0]-187,screensize[1]-96),176,44,variantImg,'ruleVariant')
classicButton = UI.Button(interface,(screensize[0]-187,screensize[1]-56),176,44,classicImg,'ruleClassic')
goButton = UI.Button(interface,(screensize[0]-189,200),89,70,goImg,'go')
stopButton = UI.Button(interface,(screensize[0]-95,200),89,70,stopImg,'stop')
clearButton = UI.Button(interface,(screensize[0]-46,280),40,30,clearImg,'clear')
randomButton = UI.Button(interface,(screensize[0]-86,280),40,30,randomImg,'random')
stepButton = UI.Button(interface,(screensize[0]-189,280),40,30,stepImg,'step')
#create mode display text
fontObj = pygame.font.Font('freesansbold.ttf',16)
modeSurface = fontObj.render('Mode: %s'.format(gameState.rules),True,BLACK,(0,0,0,0))


#Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            if event.key == K_SPACE and gameState.running == False:
                gameState.doStep = True
            elif event.key == K_RETURN and gameState.running == False:
                gameState.running = True
            elif event.key == K_RETURN and gameState.running == True:
                gameState.running = False
            elif event.key == K_x and gameState.running == False:
                gameState.clear = True
            elif event.key == K_r and gameState.running == False:
                gameState.doRandom = True
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mousepos = pygame.mouse.get_pos()
                if gameState.running == False:
                    states = con.update_click(states,colliders,mousepos)
                lockedButton = interface.checkButtons(mousepos,gameState)
                if type(lockedButton) == int:
                    gameState.buttonPressed = True
        elif event.type == MOUSEBUTTONUP and gameState.buttonPressed == True:
            if event.button == 1:
                interface.buttons[lockedButton].unlock()#when pressed the button is greyed out
                interface.buttons[lockedButton].pressed = False
                gameState.buttonPressed = False
    
    if gameState.running == False:
        cellColour = CYAN
        background = OCEAN
        goButton.unlock()
        stopButton.lock()
        clearButton.unlock()
        stepButton.unlock()
        randomButton.unlock()
    elif gameState.running == True:
        states = con.calc_states(states,gameState.rules)
        cellColour = FOAM
        background = NAVY
        stopButton.unlock()
        goButton.lock()
        clearButton.lock()
        stepButton.lock()
        randomButton.lock()
        
    if gameState.doStep == True:
        states = con.calc_states(states,gameState.rules)
        gameState.doStep = False
    if gameState.doRandom == True:
        states[:,:] =  np.round(np.random.rand(np.size(states,0),np.size(states,1)));
        gameState.doRandom = False
    if gameState.clear == True:
        states[:,:] = 0
        gameState.clear = False
    if gameState.rules == 'Classic':
        classicButton.lock()
        variantButton.unlock()
        FPS = 10
    elif gameState.rules == 'Variant':
        variantButton.lock()
        classicButton.unlock()
        FPS = 6
    
    grid = con.render_cells(states,grid,cell,cellSize,LINEWIDTH,cellColour,background)
    DISPLAYSURF.blit(grid,(0,0))
    #draw the UI
    pygame.draw.rect(DISPLAYSURF,DGRAY,(screensize[0]-200,0,200,screensize[1]))
    pygame.draw.line(DISPLAYSURF,DARK,(screensize[0]-200,0),(screensize[0]-200,screensize[1]),5)
    DISPLAYSURF.blit(headerImg,(screensize[0]-195,0))
    interface.drawButtons(DISPLAYSURF)
    #display the current mode
    modeSurface = fontObj.render('Mode: {}'.format(gameState.rules),True,BLACK)
    modeRect = modeSurface.get_rect()
    modeRect.topleft = (screensize[0]-187,screensize[1]-116)
    DISPLAYSURF.blit(modeSurface,modeRect)
    
    pygame.display.update()
    
    #size = pygame.display.get_surface().get_size() #check new size in case window has been resized
    if gameState.running == False:
        FPS = 30 #we dont need to keep them down when there is no simulation happening
    fpsClock.tick(FPS)
    
