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

width, height = 1400, 700
screen = pygame.display.set_mode((width, height))

bg = 0, 0, 0
screen.fill(bg)

cells = 1000

xCells, yCells = cells, cells // 2

cellWidth = width / xCells
cellHeight = height / yCells


# celdas con valor 1 = vivas, valor 0 = muertas
gameState = np.zeros((xCells, yCells))

pause = False

# some rules : 222 (full pyramid), 158 (dotted pyramid), 150 (fractal)
# 110 (half pyramid), 90 (fractal), 99 (colored pyramid), 45 (), 30 (half random), 22 (fractal)
bin_rule = list(np.binary_repr(161, width=8))
bin_rule.reverse()


gameState[int(np.ceil(xCells / 2)) - 1, 0] = 1

for y in range(yCells):
    for x in range(xCells):
        poly = [(x * cellWidth, y * cellHeight),
                ((x + 1) * cellWidth, y * cellHeight),
                ((x + 1) * cellWidth, (y + 1) * cellHeight),
                (x * cellWidth, (y + 1) * cellHeight)]

        if gameState[x, y] == 0:  # grey color (125, 125, 125)
            pygame.draw.polygon(screen, (0, 0, 0), poly, 1)
        else:
            pygame.draw.polygon(screen, (255, 255, 255), poly, 0)


# print(gameState[0, ])

# variable contador
y = 0

while True:

    newGameState = np.copy(gameState)
    pressKey = pygame.event.get()

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:
        print("Pause")
        pause = not pause
    if pressed[pygame.K_q]:
        print('\n[+] Exit with succcess...')
        sys.exit()

    click = pygame.mouse.get_pressed()

    if sum(click) > 0:
        posX, posY = pygame.mouse.get_pos()
        cellx, celly = int(np.floor(posX / cellWidth)
                           ), int(np.floor(posY / cellHeight))
        newGameState[cellx, celly] = not click[2]

    for x in range(xCells):

        if not pause:

            num = str(str(int(gameState[(x - 1) % xCells, y])) +
                      str(int(gameState[x, y])) + str(int(gameState[(x + 1) % xCells, y])))
            # int(num, 2) (para convertir de binario a decimal)
            index = int(num, 2)
            # newGameState[x, (y + 1) % yCells] = rules[2][index]
            newGameState[x, (y + 1) % yCells] = bin_rule[index]

        poly = [(x * cellWidth, y * cellHeight),
                ((x + 1) * cellWidth, y * cellHeight),
                ((x + 1) * cellWidth, (y + 1) * cellHeight),
                (x * cellWidth, (y + 1) * cellHeight)]

        if newGameState[x, y] == 1:
            pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
            # np.random.randint(256)

    # np.floor(yCells / 2)
    if y == yCells - 1:
        pause = True

    if not pause:
        y = (y + 1)

    gameState = np.copy(newGameState)
    time.sleep(0.01)
    pygame.display.flip()
