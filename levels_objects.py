from asyncio import constants
from threading import local
import pygame
from objects import Square, Guard, NPC
import constants
from enum import Enum
import level_1
import sys

class Level():

    def __init__(self, screen: pygame.Surface, bg: tuple, player: Square, name: str) -> None:
        """Init for level generic class
        """
        self.screen = screen
        self.bg = bg
        self.player = player
        self.name = name
        self.reset()

    def reset(self) -> None:
        """Resets the object to the initial state
        """
        self.font = pygame.font.SysFont(None, 25)
        self.npcs = []
        self.squares = []
        self.baddies = []
        self.finished = False

    def draw_bg(self) -> None:
        """Draw background
        """
        self.screen.fill(self.bg)

    def draw(self) -> None:
        """Draws the generic things
        """
        for square in self.squares:
            for rect_dict in square.get_rectangles():
                pygame.draw.rect(self.screen, rect_dict['colour'], rect_dict['rectangle'], border_radius=rect_dict['radius'])
        for npc in self.npcs:
            speech = npc.get_speech()
            if speech != "":
                text = self.font.render(speech, True, npc.body_colour)
                text_rect = text.get_rect(
                    centerx = npc.position.x,
                    centery = npc.position.y - npc.size
                )
                self.screen.blit(text, text_rect)
        for baddie in self.baddies:
            for baddie_rect in baddie.get_rectangles():
                for player_rect in self.player.get_rectangles():
                    if player_rect['rectangle'].colliderect(baddie_rect['rectangle']):
                        self.player.dead()
                        return


class DeadScreen(Level):
    """Object for the player has died screen, will restart current level for now
    """

    def __init__(self, screen: pygame.Surface, bg: tuple, player: Square) -> None:
        super().__init__(screen, bg, player, '')

    def draw(self) -> None:
        """Draws the dead screen
        """
        super().draw_bg()
        super().draw()
        text = self.font.render('You are dead, press X to try again', True, constants.WHITE)
        text_rect = text.get_rect(
            center = (
                constants.WIDTH / 2,
                constants.HEIGHT / 2
            )
        )
        self.screen.blit(text, text_rect)


class Levels():
    """Holds the levels objects and increments through the levels
    """

    def __init__(self, screen: pygame.Surface, player: Square) -> None:
        """Inits the Levels object
        """
        self.screen = screen
        self.player = player
        self.levels = [
            level_1.Level1(self.screen, constants.BACKGROUND_COLOR, self.player)
        ]
        self.dead_level = DeadScreen(self.screen, constants.BACKGROUND_COLOR, self.player)
        self.num_levels = len(self.levels)
        self.current_level = 0

    def get_current_level(self) -> Level:
        """Retrusn the current level object

        Returns:
            Level: object of the current level
        """
        if self.player.is_fully_dead():
            print('fully dead')
            sys.exit() 
        if self.player.is_dead():
            return self.dead_level
        return self.levels[self.current_level]

    def check_status(self) -> None:
        """Checks the status of a level, whether it has finished
        whether the player has died etc...
        """
        if self.get_current_level().finished:
            self.current_level += 1

    def not_dead(self) -> None:
        """Sets the level back to initial state and revivesthe player
        """
        if self.player.is_dead():
            self.player.not_dead()
            self.get_current_level().reset()

    def get_button_pushes(self) -> None:
        """Gets the button pushes
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    self.player.direction.look_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.direction.look_right()
                elif event.key == pygame.K_UP:
                    self.player.move_forward()
                elif event.key == pygame.K_DOWN:
                    self.player.move_backward()
                elif event.key == pygame.K_t:
                    self.player.torch.toggle()
                elif event.key == pygame.K_i:
                    self.player.toggle_invisible()
                elif event.key == pygame.K_x:
                    self.not_dead()
