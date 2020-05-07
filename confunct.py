# -*- coding: utf-8 -*-
"""
Created on Mon May  4 23:29:13 2020
Functions directory for game of life
@author: Carlos
"""

import pygame
from pygame.locals import *
import numpy as np

BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)

#set-up functions
def generateStates(size,cellSize,linewidth):
    #generate a 2d array of states of the cells with the size of display, of the cell side and the width of lines
    #we use a system  where from coordinate zero it goes line,cell,line,cell...line,cell starting in line and
    #ending in cell. We need to divide the screen in divisions of size cell+1line and use floor to make sure it
    #stays within the screen in case it is a bit to big
    arraySize = (np.int(np.floor(size[0]/(cellSize+linewidth))),np.int(np.floor(size[1]/(cellSize+linewidth))))
    states = np.zeros(arraySize) #states of zeroes means that they all with no live neighbors
    
    '''states = np.round(np.random.rand(arraySize[0],arraySize[1]))#random case'''
    
    return states
def buildGrid(states,cellSize,linewidth,COLOUR = YELLOW, background = BLACK):
    #use the states array, cellsize and linewidth to draw a grid on to the screen
    size = (np.size(states,0)*(cellSize+linewidth),np.size(states,1)*(cellSize+linewidth))
    grid = pygame.Surface(size)
    grid.fill(background)
    
    for i in range(np.size(states,0)):
        pygame.draw.line(grid,COLOUR,((i*(cellSize+linewidth),0)),(i*(cellSize+linewidth),size[1]),linewidth)
    for j in range(np.size(states,1)):
        pygame.draw.line(grid,COLOUR,(0,(j*(cellSize+linewidth))),(size[0],(j*(cellSize+linewidth))),linewidth)
        
    return grid
def generateColliders(states,cellSize,linewidth):
    #defines the boundaries of cells in the grid to determine whether they have been mouse-clicked
    #collider is a set of tuples of four integer (top left corner x,y - bottom right corner x,y)
    colliders = {}
    for i in range(np.size(states,0)):
        for j in range(np.size(states,1)):
            #the colliders will include the cell and some of the grid.
            #From testing ive seen that this feels better for the user because
            #if colliders only include the cells one often clicks on the grid
            #obtaining no response
            minx = i*(cellSize+linewidth)
            miny = j*(cellSize+linewidth)
            colliders[i,j] = (minx,miny,minx+cellSize+linewidth,miny+cellSize+linewidth)
    
    return colliders

#dynamics function
def update_click(states,colliders,mousepos):
    states = states
    # check for every cell wether the mouse is on it
    for i in range(np.size(states,0)):
        for j in range(np.size(states,1)):
            if mousepos[0]>colliders[i,j][0] and mousepos[1]>colliders[i,j][1]:
                if mousepos[0]<colliders[i,j][2] and mousepos[1]<colliders[i,j][3]:
                    if states[i,j] == 1:
                        states [i,j] = 0
                    else:
                        states [i,j] = 1
                
                    
    return states

def calc_states(states,rules = 'Classic'):
    
    #expand the states array with boundary layers set to be dead
    lineBound = np.zeros((1,np.size(states,1)))
    columnBound = np.zeros((2+np.size(states,0),1))
    full = np.concatenate((lineBound,states,lineBound))
    full = np.concatenate((columnBound,full,columnBound),axis=1)
    #determine the number of living neighbours by adding nearby states
    newfull = np.zeros((np.size(full,0),np.size(full,1)))
    '''print(states)
    print('full:')
    print(full)'''
    for i in range(1,np.size(full,0)-1):
        for j in range (1,np.size(full,1)-1):
            newfull[i,j] = full[i-1,j] + full[i-1,j-1] + full[i-1,j+1] + full[i,j+1] + full[i,j-1] + full[i+1,j] + full[i+1,j-1] + full[i+1,j+1]
            #get number of neighbors
    '''print('new full')
    print(newfull)'''
    #the new array is taken back to the same size as states to compare wether the cell
    #was alive previously
    newStates = states
    newcut = newfull[:-1,:-1]
    newcut = newcut[(range(1,np.size(newcut,0))),:]
    newcut = newcut[:,(range(1,np.size(newcut,1)))]
    '''print('new cut:')
    print(newcut)'''
    #each cell is checked with conditions to set to living(1) or dead(0) 
    for i in range(np.size(states,0)):
        for j in range (np.size(states,1)):
            if newcut[i,j] < 2 or newcut[i,j] > 3:
                newStates[i,j] = 0
            elif rules == 'Classic' and (newcut[i,j] == 2 and states[i,j] == 0):
                newStates[i,j] = 0
            else:
                newStates[i,j] = 1
    return newStates
def render_cells(states,grid, cell,cellSize,linewidth, COLOUR = WHITE, background = BLACK):
    #draw the cells on to the display
    for i in range(np.size(states,0)):
        for j in range(np.size(states,1)):
            cell.topleft = (i*cellSize+(i+1)*linewidth,j*cellSize+(j+1)*linewidth)
            if states[i,j] == 1:
                pygame.draw.rect(grid,COLOUR,cell)
            if states[i,j] == 0:
                pygame.draw.rect(grid,background,cell)
    return grid