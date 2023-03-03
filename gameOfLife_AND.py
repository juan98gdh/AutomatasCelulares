import pygame
import numpy as np
import signal
import sys
import time


def signal_handler(sig, frame):
    print('\n[+] Exit with succcess...')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

xCells, yCells = 100, 100

cellWidth = width / xCells
cellHeight = height / yCells


# celdas con valor 1 = vivas, valor 0 = muertas
gameState = np.zeros((xCells, yCells))

pause = True


gameState[10, 15] = 1
gameState[11, 15] = 1
gameState[10, 16] = 1
gameState[11, 16] = 1

gameState[14, 15] = 1
gameState[15, 15] = 1
gameState[15, 14] = 1
gameState[15, 16] = 1
gameState[10, 15] = 1
gameState[17, 15] = 1
gameState[16, 17] = 1
gameState[16, 13] = 1

gameState[18, 12] = 1
gameState[19, 12] = 1
gameState[20, 13] = 1
gameState[21, 14] = 1
gameState[21, 15] = 1
gameState[21, 16] = 1
gameState[20, 17] = 1
gameState[19, 18] = 1
gameState[18, 18] = 1

gameState[26, 17] = 1
gameState[29, 17] = 1
gameState[30, 17] = 1
gameState[31, 17] = 1
gameState[31, 16] = 1
gameState[30, 15] = 1

gameState[35, 15] = 1
gameState[35, 16] = 1
gameState[37, 15] = 1
gameState[38, 14] = 1
gameState[38, 13] = 1
gameState[38, 12] = 1
gameState[39, 14] = 1
gameState[39, 13] = 1
gameState[39, 12] = 1
gameState[37, 11] = 1
gameState[35, 11] = 1
gameState[35, 10] = 1

gameState[44, 14] = 1
gameState[45, 14] = 1
gameState[44, 13] = 1
gameState[45, 13] = 1

# NEGADOR
gameState[36, 24] = 1
gameState[36, 23] = 1
gameState[37, 23] = 1
gameState[37, 25] = 1
gameState[38, 25] = 1
gameState[39, 25] = 1
gameState[39, 26] = 1


while True:

    newGameState = np.copy(gameState)

    screen.fill(bg)

    pressKey = pygame.event.get()

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_r]:
        newGameState = np.zeros((xCells, yCells))
        # print("Reset")
    if pressed[pygame.K_SPACE]:
        # print("Pause")
        pause = not pause
    if pressed[pygame.K_q]:
        print('\n[+] Exit with succcess...')
        sys.exit(0)

    # for event in pressKey:
    #    if event.type == pygame.KEYDOWN:
    #        pause = not pause

    click = pygame.mouse.get_pressed()

    if sum(click) > 0:
        posX, posY = pygame.mouse.get_pos()
        cellx, celly = int(np.floor(posX / cellWidth)
                           ), int(np.floor(posY / cellHeight))
        newGameState[cellx, celly] = not click[2]

    for y in range(yCells):
        for x in range(xCells):

            if not pause:

                living_neighbours = gameState[(x + 1) % xCells, (y + 1) % yCells] + \
                    gameState[(x + 1) % xCells, (y - 1) % yCells] + \
                    gameState[(x - 1) % xCells, (y + 1) % yCells] + \
                    gameState[(x - 1) % xCells, (y - 1) % yCells] + \
                    gameState[(x) % xCells, (y - 1) % yCells] + \
                    gameState[(x) % xCells, (y + 1) % yCells] + \
                    gameState[(x - 1) % xCells, (y) % yCells] + \
                    gameState[(x + 1) % xCells, (y) % yCells]

                # # Reglas # #
                # Regla 1, Una celula muerta, revive cin 3 celulas vecinas vivas
                if gameState[x, y] == 0 and living_neighbours == 3:
                    newGameState[x, y] = 1

                # Regla 2, Una celula viva con menos de 2 o mas de 3 vecinas vivas, muere
                elif gameState[x, y] == 1 and (living_neighbours < 2 or living_neighbours > 3):
                    newGameState[x, y] = 0

            poly = [(x * cellWidth, y * cellHeight),
                    ((x + 1) * cellWidth, y * cellHeight),
                    ((x + 1) * cellWidth, (y + 1) * cellHeight),
                    (x * cellWidth, (y + 1) * cellHeight)]

            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    gameState = np.copy(newGameState)
    time.sleep(0.05)
    pygame.display.flip()
