import pygame


columnAmount, rowAmount = 32,18
tileSize = 40

pygame.init()
bg = (0, 0, 0)
tileColor = (230, 230, 230)
width, height = int(columnAmount * tileSize), int(rowAmount * tileSize)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Map Maker')

map = [[0 for column in range(columnAmount)] for row in range(rowAmount)]

run = True

while run:
    screen.fill(bg)

    for row in range(rowAmount):
        for column in range(columnAmount):
            if map[row][column] == 1:
                pygame.draw.rect(screen, tileColor, (column * tileSize, row * tileSize, tileSize - 1, tileSize - 1))

    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            self.run = False
        if even.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if even.button == 1:
                map[pos[1] // tileSize][pos[0] // tileSize] = 1
            if even.button == 3:
                map[pos[1] // tileSize][pos[0] // tileSize] = 0

        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_RETURN:
                for row in map:
                    print(row)

    pygame.display.update()