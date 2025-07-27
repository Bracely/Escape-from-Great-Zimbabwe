import pygame
import constants
from character import Character

pygame.init()

#commented this 

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))


pygame.display.set_caption("Escape from Great Zimbabwe")

#player or character

player = Character(100, 100)
#ah huh test
#main Game loop

run = True

while run:

    #draw player
    player.draw(screen)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
