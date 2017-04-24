import random
import pygame
import sys
from pygame.locals import *
import time

Snakespeed= 25
Window_Width= 900
Window_Height= 600
Cell_Size = 20 #Width and height of the cells
assert Window_Width % Cell_Size == 0, "Window width must be a multiple of cell size."     #Ensuring that the cells fit perfectly in the window. eg if cell size was 10     and window width or windowheight were 15 only 1.5 cells would fit.
assert Window_Height % Cell_Size == 0, "Window height must be a multiple of cell size."  #Ensuring that only whole integer number of cells fit perfectly in the window.
Cell_W= int(Window_Width / Cell_Size) #Cell Width 
Cell_H= int(Window_Height / Cell_Size) #Cellc Height


White= (255,255,255)
Black= (0,0,0)
Red= (255,0,0) #Defining element colors for the program.
Green= (0,255,0)
DARKGreen= (0,155,0)
DARKGRAY= (40,40,40)
YELLOW= (255,255,0)
Red_DARK= (150,0,0)
BLUE= (0,0,255)
BLUE_DARK= (0,0,150)


BGCOLOR = BLUE_DARK # Background color
Inner = [Green,White]
Outer = [DARKGreen,YELLOW]
Color_new = [Green,White,DARKGreen,YELLOW,BLUE,BLUE_DARK]
UP = 'up'
DOWN = 'down'      # Defining keyboard keys.  
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # Syntactic sugar: index of the snake's head
def Background():
    pygame.init()                  
    img = pygame.image.load("Snake_play_back.jpg").convert()
    img = pygame.transform.scale(img, (800, 500))
    TheBoard.blit(img,(0, 0))     

def Background_Start():
    pygame.init()                  
    img = pygame.image.load("Snake_back.png").convert()
    img = pygame.transform.scale(img, (900, 600))
    TheBoard.blit(img,(0, 0))

import os, sys, math, pygame, pygame.font, pygame.image
from pygame.locals import *


def TheWall():
    global boundry
    boundry=[]
    for i in range(0,Window_Width):
        boundry.append((i,0))
        boundry.append((i,Window_Height-18))
    for i in range(0,Window_Height):
        boundry.append((0,i))
        boundry.append((Window_Width-18,i))

def TheWallDraw():
    for each in boundry:
        wallRect = pygame.Rect(each[0],each[1], Cell_Size-2, Cell_Size-2)
        pygame.draw.rect(TheBoard, DARKGreen, wallRect)
 

def main():
    global SnakespeedCLOCK, TheBoard, BASICFONT

    pygame.init()
    SnakespeedCLOCK = pygame.time.Clock()
    TheBoard = pygame.display.set_mode((Window_Width, Window_Height))
    BASICFONT = pygame.font.SysFont('boldenstein', 38)
    pygame.display.set_caption('Snake Game')
    Background_Start()

    StartGame()
    while True:
        TheWall()
        RunTheGame()
        GameOver()
        


def RunTheGame():
    # Set a random start point.
    startx = random.randint(5, Cell_W - 6)
    starty = random.randint(5, Cell_H - 6)
    Coordinates = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the food in a random place.
    food = PlaceFood()
    pygame.init()                  
    img = pygame.image.load("Snake_play_back.jpg").convert()
    img = pygame.transform.scale(img, (900, 600))
    Snakespeed = 20

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT ) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT ) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP ) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN ) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the Snake has hit itself or the edge
        if Coordinates[HEAD]['x'] == -1 or Coordinates[HEAD]['x'] == Cell_W-1 or     Coordinates[HEAD]['y'] == -1 or Coordinates[HEAD]['y'] == Cell_H-1:
            return # game over 
        for SnakeBody in Coordinates[1:]:
            if SnakeBody['x'] == Coordinates[HEAD]['x'] and SnakeBody['y'] == Coordinates[HEAD]    ['y']: 
                return # game over

        # check if Snake has eaten a food
        if Coordinates[HEAD]['x'] == food['x'] and Coordinates[HEAD]['y'] == food['y']:
            # don't remove worm's tail segment
            food = PlaceFood() # set a new food somewhere
        else:
            del Coordinates[-1] # remove worm's tail segment
        if direction == UP:
            newHead = {'x': Coordinates[HEAD]['x'], 'y': Coordinates[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': Coordinates[HEAD]['x'], 'y': Coordinates[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': Coordinates[HEAD]['x'] - 1, 'y': Coordinates[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': Coordinates[HEAD]['x'] + 1, 'y': Coordinates[HEAD]['y']}
        Coordinates.insert(0, newHead)
        TheBoard.blit(img,(0, 0)) 
        drawSnake(Coordinates)
        drawfood(food)
        drawScore(len(Coordinates) - 3)
        TheWallDraw()
        pygame.display.update()
        for i in range(3):
            Snakespeed += 1
            SnakespeedCLOCK.tick(Snakespeed)
        
        



def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to start a New Game.', True, BLUE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (Window_Width - 590, Window_Height-100)
    TheBoard.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def StartGame():
    titleFont = pygame.font.SysFont('ThunderCats-Ho!', 70)
    Second = pygame.font.SysFont('FreestyleScript',30)
    titleSurf1 = titleFont.render('Hungry', True, random.choice(Color_new), Black)
    titleSurf2 = titleFont.render('Snake',True,random.choice(Color_new),Black)
    inst = Second.render('Instructions:', True, BLUE)
    instRect = inst.get_rect()
    instRect.topleft = (Window_Width - 180, Window_Height-200)
    play = Second.render('Press Arrow Keys to', True, BLUE)
    playmove = Second.render('move the Hungry Snake', True, BLUE)
    playmoveRect = playmove.get_rect()
    playRect = play.get_rect()
    playRect.topleft = (Window_Width - 220, Window_Height-150)
    playmoveRect.topleft = (Window_Width - 220, Window_Height-110)
    TheBoard.blit(play, playRect)
    TheBoard.blit(playmove, playmoveRect)
    TheBoard.blit(inst, instRect)
    
    degrees1 = 0
    degrees2 = 0
    while True:
        
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect1.center = ((Window_Width / 2)-310, (Window_Height / 2)-195)
        rotatedRect2.center = ((Window_Width / 2)+310, (Window_Height / 2)-195)
        TheBoard.blit(rotatedSurf1, rotatedRect1)
        TheBoard.blit(rotatedSurf2, rotatedRect2)
        
        drawPressKeyMsg()
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        SnakespeedCLOCK.tick(Snakespeed)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame
    
def terminate():
    pygame.quit()
    sys.exit()


def PlaceFood():
    return {'x': random.randint(10, Cell_W - 5), 'y': random.randint(10, Cell_H - 5)}


def GameOver():
    gameOverFont = pygame.font.SysFont('boldenstein', 110)
    gameSurf = gameOverFont.render('Game', True, YELLOW)
    overSurf = gameOverFont.render('Over', True, YELLOW)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.topleft = (Window_Width / 2 - 300, 100)
    overRect.topleft = (Window_Width / 2+250, 100)

    TheBoard.blit(gameSurf, gameRect)
    TheBoard.blit(overSurf, overRect)
    pygame.display.update()
    pygame.time.wait(500)
    time.sleep(0.5)
    main()

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, White)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (Window_Width - 120, 20)
    TheBoard.blit(scoreSurf, scoreRect)


def drawSnake(Coordinates):
    for coord in Coordinates:
        x = coord['x'] * Cell_Size
        y = coord['y'] * Cell_Size
        wormSegmentRect = pygame.Rect(x, y, Cell_Size, Cell_Size)
        pygame.draw.circle(TheBoard, BLUE, (x+5,y+5), 15)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, Cell_Size - 8, Cell_Size - 8)
        pygame.draw.circle(TheBoard, Red , (x+4,y+4), 8)



def drawfood(coord):
    x = coord['x'] * Cell_Size
    y = coord['y'] * Cell_Size
    pygame.draw.circle(TheBoard, Red, (x,y), 10)







if __name__ == '__main__':
    try:
        main()
    except SystemExit:
            pass
