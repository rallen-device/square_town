from calendar import leapdays
import sys
import pygame
import time
from objects import Guard, Square
import constants
import level_1
import level_frame
import levels_objects

pygame.init()


screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

game_over = False

player = Square(100, 100, constants.PLAYER_SZIE, 180, constants.GREY, constants.TORCH_COLOUR)
levels = levels_objects.Levels(screen, player)
frame = level_frame.LevelFrame(screen, player, levels)

while not game_over:

    levels.get_button_pushes()
    levels.get_current_level().draw()
    frame.draw()
    pygame.display.update()

time.sleep(1)
