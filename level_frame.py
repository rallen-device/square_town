import pygame
import constants
from objects import Square
from levels_objects import Levels


class LevelFrame():
    """Draws the frame for each level
    """

    def __init__(self, screen: pygame.Surface, player: Square, levels: Levels) -> None:
        """Inits the variables for the frame
        """
        self.screen = screen
        self.player = player
        self.levels = levels
        self.font = pygame.font.SysFont(None, 50)

    def draw(self) -> None:
        """Draws the frame
        """
        pygame.draw.rect(self.screen,
        constants.FRAME_COLOR, 
        (
            0,
            constants.PLAY_HEIGHT,
            constants.WIDTH,
            constants.HEIGHT - constants.PLAY_HEIGHT
            )
        )
        thingy_color = constants.YELLOW
        if self.player.invisible:
            thingy_color = constants.BLUE
        pygame.draw.rect(
            self.screen,
            thingy_color,
            (
                (constants.WIDTH / 2) + constants.FRAME_PADDING,
                constants.PLAY_HEIGHT + constants.FRAME_PADDING,
                ((constants.WIDTH / 2) - (constants.FRAME_PADDING * 2)) * (self.player.max_invisible / constants.MAX_INVISIBLE),
                constants.HEIGHT - constants.PLAY_HEIGHT - (constants.FRAME_PADDING * 2)
            )
        )
        text = self.font.render(self.levels.get_current_level().name, True, constants.WHITE)
        text_rect = text.get_rect(
            left = constants.FRAME_PADDING,
            centery = constants.PLAY_HEIGHT + ((constants.HEIGHT - constants.PLAY_HEIGHT) / 2)
        )
        self.screen.blit(text, text_rect)
        for index in range(constants.NUM_LIVES):
            if self.player.lives > index:
                pygame.draw.rect(
                    self.screen,
                    self.player.body_colour,
                    (
                        (constants.WIDTH / 4) + index * 60,
                        constants.PLAY_HEIGHT + constants.FRAME_PADDING,
                        50,
                        constants.HEIGHT - constants.PLAY_HEIGHT - (constants.FRAME_PADDING * 2)
                    )
                )
