import pygame

columnAmount, rowAmount = 20, 20
tileSize = 40

pygame.init()
bg = (0, 0, 0)
tileColor = (230, 230, 230)
speedColor = (50, 230, 50)
jumpColor = (50, 50, 250)
bounceColor = (250, 50, 50)
winColor = (182, 196, 77)
width, height = int(columnAmount * tileSize), int(rowAmount * tileSize)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Map Maker')
clicked = False
camera = 0
speed = 1
move = 0
mode = 1
# map = [[0 for _ in range(columnAmount)] for _ in range(rowAmount)]

map = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


def printMap():
    map[0].append(1)
    print('[', map[0], ',')
    map[0].pop(-1)
    for row in range(1, len(map)):
        map[row].append(1)
        if row <= len(map) - 2:
            print(map[row], ',')
        else:
            print(map[row], ']')
        map[row].pop(-1)


run = True

if __name__ == '__main__':
    while run:
        screen.fill(bg)
        if camera // tileSize > len(map[0]) - columnAmount:
            for i in range(len(map)):
                if i < rowAmount - 1:
                    map[i].append(0)
                else:
                    map[i].append(1)

        for row in range(rowAmount):
            for column in range(len(map[0]) - 1):
                if map[row][column] == 1:
                    pygame.draw.rect(screen, tileColor,
                                     (column * tileSize - camera, row * tileSize, tileSize - 1, tileSize - 1))
                elif map[row][column] == 2:
                    pygame.draw.rect(screen, speedColor,
                                     (column * tileSize - camera, row * tileSize, tileSize - 1, tileSize - 1))
                elif map[row][column] == 3:
                    pygame.draw.rect(screen, jumpColor,
                                     (column * tileSize - camera, row * tileSize, tileSize - 1, tileSize - 1))
                elif map[row][column] == 4:
                    pygame.draw.rect(screen, bounceColor,
                                     (column * tileSize - camera, row * tileSize, tileSize - 1, tileSize - 1))
                elif map[row][column] == 5:
                    pygame.draw.rect(screen, winColor,
                                     (column * tileSize - camera, row * tileSize, tileSize - 1, tileSize - 1))

        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                run = False
            if even.type == pygame.MOUSEBUTTONDOWN:
                clicked = even.button
            if even.type == pygame.MOUSEBUTTONUP:
                clicked = 0

            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_RETURN:
                    printMap()
                if even.key == pygame.K_d:
                    move = speed
                if even.key == pygame.K_a:
                    move = -speed

                if even.key == pygame.K_1:
                    mode = 1
                if even.key == pygame.K_2:
                    mode = 2
                if even.key == pygame.K_3:
                    mode = 3
                if even.key == pygame.K_4:
                    mode = 4
                if even.key == pygame.K_5:
                    mode = 5
                if even.key == pygame.K_6:
                    mode = 6
                if even.key == pygame.K_7:
                    mode = 7
                if even.key == pygame.K_8:
                    mode = 8
                if even.key == pygame.K_9:
                    mode = 9
                if even.key == pygame.K_RIGHT:
                    speed += 1
                if even.key == pygame.K_LEFT:
                    speed -= 1

            if even.type == pygame.KEYUP:
                if even.key in [pygame.K_d, pygame.K_a]:
                    move = 0

            if clicked != 0:
                a = mode
                if clicked == 3:
                    mode = 0
                pos = pygame.mouse.get_pos()
                try:
                    map[pos[1] // tileSize][(pos[0] + camera) // tileSize] = mode
                except:
                    printMap(map)
                mode = a

        camera += move
        if camera < 0:
            camera = 0

        pygame.display.update()
