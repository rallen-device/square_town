import sys
import pygame
import time
from objects import MAX_INVISIBLE, Guard, Square

pygame.init()

WIDTH = 800
HEIGHT = 600
PLAY_HEIGHT = 550

RED = (255,90,10)
GREY = (100,100,100)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BACKGROUND_COLOR = (50,50,50)
TORCH_COLOUR = (60, 60, 60)

player_size = 50
player_pos = [WIDTH/2, HEIGHT-2*player_size]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False



player = Square(100, 100, 50, 90, YELLOW, TORCH_COLOUR)
guard0 = Guard(300, 300, 50, 0, RED, TORCH_COLOUR, (100, 100, 600, 600), 0.5)
guard0.start_patrol()
guard1 = Guard(300, 400, 50, 0, RED, TORCH_COLOUR, (100, 100, 600, 600), 0.4)
guard1.start_patrol()

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                player.direction.look_left()
            elif event.key == pygame.K_RIGHT:
                player.direction.look_right()
            elif event.key == pygame.K_UP:
                player.move_forward()
            elif event.key == pygame.K_DOWN:
                player.move_backward()
            elif event.key == pygame.K_t:
                player.torch.toggle()
            elif event.key == pygame.K_i:
                player.toggle_invisible()

    screen.fill(BACKGROUND_COLOR)
    for rect_dict in player.get_rectangles():
        pygame.draw.rect(screen, rect_dict['colour'], rect_dict['rectangle'])
    for rect_dict in guard0.get_rectangles():
        pygame.draw.rect(screen, rect_dict['colour'], rect_dict['rectangle'])
    for rect_dict in guard1.get_rectangles():
        pygame.draw.rect(screen, rect_dict['colour'], rect_dict['rectangle'])
    for player_rect in player.get_rectangles():
        for guard_rect in guard0.get_rectangles():
            if player_rect['rectangle'].colliderect(guard_rect['rectangle']):
                game_over = True
        for guard_rect in guard1.get_rectangles():
            if player_rect['rectangle'].colliderect(guard_rect['rectangle']):
                game_over = True
    thingy_color = YELLOW
    if player.invisible:
        thingy_color = BLUE
    pygame.draw.rect(screen, thingy_color, (0, PLAY_HEIGHT, WIDTH * (player.max_invisible / MAX_INVISIBLE), HEIGHT - PLAY_HEIGHT))
    pygame.display.update()

time.sleep(1)
