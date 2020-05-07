# -*- coding: utf-8 -*-
"""
Created on Wed May  6 16:55:37 2020
functions and classes necessary for the UI
@author: Carlos
"""

import pygame
from pygame.locals import *
import numpy as np
import copy

import confunct as con

class Interface:
    def __init__(self):
        self.buttons = []
        self.colliders = []
    def drawButtons(self,surface):
        for i in range(np.size(self.buttons)):
            surface.blit(self.buttons[i].render(),self.buttons[i].position)
    def checkButtons(self,mousepos,gameState):
        for i in range(len(self.buttons)):
            if mousepos[0]>self.colliders[i][0] and mousepos[1]>self.colliders[i][1]:
                if mousepos[0]<self.colliders[i][2] and mousepos[1]<self.colliders[i][3]:
                    self.buttons[i].act(gameState)
                    self.buttons[i].lock()#with mousebuttonup it will be unlocked
                    self.buttons[i].pressed = True#with mousebuttonup it will be unlocked
                    return i

class Button:
    # a button object to make the UI buttons. Made it to try out how to make
    # object oriented programming
    def __init__(self,interface,position,width,height,image, use):
        self.position = position
        self.collider = (position[0],position[1],position[0]+width,position[1]+height)
        interface.colliders.append(self.collider)
        self.use = use
        self.buttonSurface = pygame.Surface((width,height))
        self.buttonSurface.blit(image,(0,0))
        self.locker = pygame.Surface((width,height),SRCALPHA)
        self.locker.fill((0,0,0,200))
        self.locked = False
        self.pressed = False
        interface.buttons.append(self)
    def lock(self):
        #grays out the button to lock it out
        self.locked = True
    def unlock(self):
        if self.pressed == False:
            self.locked = False
    def render(self):
        
        rendered = copy.copy(self.buttonSurface);
        if self.locked == True:
            rendered.blit(self.locker,(0,0))
        return rendered
    def act(self,gameState):
        if self.locked == False:
            if self.use == 'ruleVariant':
                gameState.rules = 'Variant'
            elif self.use == 'ruleClassic':
                gameState.rules = 'Classic'
            elif self.use == 'go':
                gameState.running = True
            elif self.use == 'stop':
                gameState.running = False
            elif self.use == 'step':
                gameState.doStep = True
                #by now im really missing a switch statement in python 
            elif self.use == 'clear':
                gameState.clear = True
            elif self.use == 'random':
                gameState.doRandom = True
                