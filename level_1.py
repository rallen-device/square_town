from asyncio import constants
from threading import local
import pygame
from objects import Square, Guard, NPC
import constants
from enum import Enum
from levels_objects import Level


class Level1States(Enum):
    """Holds the states for level 1
    """
    START = 0
    INTRO = 1
    TALKING_0 = 2
    TALKING_1 = 3
    GUARD0 = 4
    GUARD1 = 5

class Level1(Level):

    def __init__(self, screen: pygame.Surface, bg: tuple, player: Square) -> None:
        """Inits level 1
        """
        super().__init__(screen, bg, player, 'Level 1')
        self.reset()

    def reset(self) -> None:
        """Resets the level
        """
        super().reset()
        scared_person = NPC(400, 100, constants.PLAYER_SZIE, 180, constants.GREY, constants.TORCH_COLOUR, (400, 400, 400, 400), 1.5)
        self.player.position.y = 100
        self.player.position.x = 100
        self.player.direction.direction = 180
        self.scared_person = scared_person
        self.npcs = [self.scared_person]
        self.squares = [scared_person, self.player]
        self.scared_person.start_actions()
        self.state = Level1States.START

    def draw(self) -> None:
        """Draws level 1
        """
        super().draw_bg()
        super().draw()

        local_state = self.state
        if self.state == Level1States.START:
            self.scared_person.talk('Hey, you! Come over here!', 5)
            self.state = Level1States.INTRO
        elif self.state == Level1States.INTRO:
            if self.scared_person.get_speech() == "":
                self.scared_person.talk("Come over here!", 5)
            if self.scared_person.aura_rect.colliderect(self.player):
                self.state = Level1States.TALKING_0
        elif self.state == Level1States.TALKING_0:
            if self.state != self.prev_state:
                self.scared_person.talk('Weird folk with round edges have started appearing', 5)
            if self.scared_person.get_speech() == "":
                self.state = Level1States.TALKING_1
        elif self.state == Level1States.TALKING_1:
            if self.state != self.prev_state:
                self.scared_person.talk('Be careful. Here comes one now!', 3)
            if self.scared_person.get_speech() == "":
                self.state = Level1States.GUARD0
        elif self.state == Level1States.GUARD0:
            if self.state != self.prev_state:
                self.guard = Guard(0, 500, constants.PLAYER_SZIE, 0, constants.RED, constants.TORCH_COLOUR, (0, 0, constants.WIDTH, constants.HEIGHT), 0.4)
                self.baddies.append(self.guard)
                self.guard.start_actions()
                self.guard.talk("All hail the round edged man", 10)
                self.npcs.append(self.guard)
                self.squares.append(self.guard)
            if self.guard.get_speech() == "":
                self.state = Level1States.GUARD1
        elif self.state == Level1States.GUARD1:
            if self.state != self.prev_state:
                self.scared_person.talk("Bloody freaks, coming to square town with their round edges", 10)
            if self.scared_person.get_speech() == "":
                self.finished = True

        elif self.state == Level1States.NULL:
            self.state = Level1States.GUARD

        self.prev_state = local_state
