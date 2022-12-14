import pygame
from threading import Thread
import time
import constants

class ObjectPosition():
    """Stores the position of an object
    """

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'X: {self.x}, Y: {self.y}'


class Direction():
    """Direction of an object
    """
    MAX = 360
    MIN = 0
    JUMP = 90

    def __init__(self, direction: int) -> None:
        self.direction = direction

    def look_right(self) -> None:
        """Turns direction in the left direction
        """
        self.direction = (self.direction - self.JUMP) % self.MAX
        
    def look_left(self) -> None:
        """Turns direction in the right direction
        """
        self.direction = (self.direction + self.JUMP) % self.MAX


def get_angle_multiplier(angle: int, x_or_not_y: bool) -> float:
    """Returns the angle multiplier

    Args:
        angle (int): _description_

    Returns:
        float: _description_
    """
    if not x_or_not_y:
        angle = (angle + 90) % 360

    return (abs(angle - 180) - 90) / 90


class Square():
    """Stores the details of a square
    """

    def __init__(self, x: int, y: int, size: int, direction: int, body_colour: tuple, torch_colour: tuple) -> None:
        """Inits a square

        Args:
            position (ObjectPosition): position of the square
            size (int): size of the square (always a square so only 1 int needed)
            direction (Direction): direction of the square
        """
        self.position = ObjectPosition(x, y)
        self.size = size
        self.direction = Direction(direction)
        self.torch = Torch(50, 2, 2, self)
        self.torch.enable = False
        self.rect = None
        self.aura_rect = None
        self.body_colour = body_colour
        self.torch_colour = torch_colour
        self.invisible = 0
        self.max_invisible = constants.MAX_INVISIBLE
        self.border_radius = 0
        self.dead_flag = False
        self.lives = constants.NUM_LIVES
        self.update_rectangle()
        Thread(target=self.invisible_counter, daemon=True).start()

    def update_rectangle(self) -> None:
        """Updates the rectangle object
        """
        self.rect = pygame.Rect(self.position.x  - (self.size / 2) , self.position.y - (self.size / 2), self.size, self.size)
        self.aura_rect = self.rect.inflate(constants.PLAYER_SZIE*2, constants.PLAYER_SZIE*2)

    def move_forward(self) -> None:
        """Moves the square backwards 
        """
        self.position.x = self.position.x + ((self.size / 2) * get_angle_multiplier(self.direction.direction, True))
        self.position.y = self.position.y + ((self.size / 2) * get_angle_multiplier(self.direction.direction, False))
        self.update_rectangle()

    def move_backward(self) -> None:
        """Moves the square backwards
        """
        self.position.x = self.position.x - ((self.size / 2) * get_angle_multiplier(self.direction.direction, True))
        self.position.y = self.position.y - ((self.size / 2) * get_angle_multiplier(self.direction.direction, False))
        self.update_rectangle()

    def get_rectangles(self) -> list:
        """Returns a list of dictionaries of the rectangles required for drawing along with their colour

        Returns:
            list: list of dctionary of colours and rectangles
        """
        dictionary = []
        if self.invisible == 0 or self.invisible == 2 or self.invisible == 4:
            body_colour = self.body_colour
            if self.invisible != 0:
                body_colour = [element * 0.5 for element in self.body_colour]
            dictionary.append({'colour': body_colour, 'rectangle': self.rect, 'radius': self.border_radius})
            rotating_colour = self.torch_colour
            for rectangle in self.torch.get_rectangles():
                rotating_colour = [element * 0.99 for element in rotating_colour]
                dictionary.append({'colour': rotating_colour, 'rectangle': rectangle, 'radius': 0})
        return dictionary

    def toggle_invisible(self) -> None:
        """Toggles the invisbility
        """
        if self.invisible == 0:
            self.invisible = self.max_invisible
        else:
            self.invisible = 0

    def invisible_counter(self) -> None:
        """Counts the invisible timer down and the max inivislbe timer up
        """
        while True:
            if self.invisible > 0:
                self.max_invisible -= 1
                self.invisible = self.max_invisible
            else:
                if self.max_invisible < constants.MAX_INVISIBLE:
                    self.max_invisible += 1
            time.sleep(0.2)
    
    def get_invisble(self) -> int:
        """Gets the invisible value
        """
        return self.invisible

    def dead(self) -> None:
        """Kills the square for whatever reason, decrements a life and sets the 
        dead flag True
        """
        self.dead_flag = True
        if self.lives > 0:
            self.lives -= 1

    def is_dead(self) -> bool:
        """Checks if the square is dead
        """
        return self.dead_flag

    def not_dead(self) -> None:
        """Revives the player
        """
        self.dead_flag = False

    def is_fully_dead(self) -> bool:
        """Checks if the player is fully dead, i.e. they have no lives left

        Returns:
            bool: True if fully dead, False if still going
        """
        if self.lives == 0:
            return True
        return False


class Torch():
    """Holds the torch class
    """

    def __init__(self, levels: int, length: int, increase: int, parent: Square) -> None:
        self.levels = levels
        self.length = length
        self.increase = increase
        self.parent = parent
        self.rectangles = []
        self.enable = True
        self.get_rectangles()

    def get_rectangles(self) -> list:
        """Returns the rectangles to draw the torch

        Returns:
            list: list of pygame.rect
        """
        direction = self.parent.direction.direction
        parent_x = self.parent.position.x
        parent_y = self.parent.position.y
        parent_size = self.parent.size
        self.rectangles = []
        if not self.enable:
            return self.rectangles
        for index in range(0, self.levels):
            rect = pygame.Rect(0, 0, 0 ,0)
            if direction == 90 or direction == 270:
                rect.width = parent_size + (self.increase * index)
                rect.height = self.length
                rect.centerx = parent_x
                if direction == 90:
                    rect.centery = (parent_y - (parent_size / 2)) - ((index + 1) * self.length / 2)
                elif direction == 270:
                    rect.centery = (parent_y + (parent_size / 2)) + ((index + 1) * self.length / 2)
            elif direction == 0 or direction == 180:
                rect.height = parent_size + (self.increase * index)
                rect.width = self.length
                rect.centery = parent_y
                if direction == 180:
                    rect.centerx = (parent_x - (parent_size / 2)) - ((index + 1) * self.length / 2)
                elif direction == 0:
                    rect.centerx = (parent_x + (parent_size / 2)) + ((index + 1) * self.length / 2)
            self.rectangles.append(rect)
        return self.rectangles

    def toggle(self) -> None:
        """Toggles the torch
        """
        self.enable = not self.enable

class NPC(Square):
    """Object for an NPC"""

    def __init__(self, x: int, y: int, size: int, direction: int, body_colour: tuple, torch_colour: tuple, bounding_box: tuple, interval: int) -> None:
        """Inits the NPC

        Args:
            x (int): _description_
            y (int): _description_
            size (int): _description_
            direction (int): _description_
            body_colour (tuple): _description_
            torch_colour (tuple): _description_
            bounding_box (tuple): _description_
            interval (int): _description_
        """
        super().__init__(x, y, size, direction, body_colour, torch_colour)
        self.bounding_box = pygame.Rect(bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3])
        self.interval = interval
        self.cancel_actions = False
        self.torch.enable = False
        self.speech = ""
        self.speech_countdown = 0

    def actions(self) -> None:
        """Moves the NPC around, controls their speech timer
        """
        while not self.cancel_actions:
            self.move_forward()
            if not self.bounding_box.contains(self.rect):
                self.direction.look_right()
                self.direction.look_right()
            if self.speech_countdown > 0:
                self.speech_countdown -= 1
            else:
                self.speech = ""

            time.sleep(self.interval)
     
    def start_actions(self) -> None:
        """Starts the patrol
        """
        self.cancel_actions = False
        Thread(target=self.actions, daemon=True).start()

    def stop_actions(self) -> None:
        """Stops the patrol
        """
        self.cancel_actions = True

    def talk(self, sentence: str, time: int) -> None:
        """Sets a speech box for an NPC

        Args:
            sentence (str): speech which they will say
            time (int): for how long they speak
        """
        self.speech = sentence
        self.speech_countdown = time

    def get_speech(self) -> str:
        """Returns the current speech

        Returns:
            str: current speech sentence
        """
        return self.speech


class Guard(NPC):
    """Object for a guard
    """

    def __init__(self, x: int, y: int, size: int, direction: int, body_colour: tuple, torch_colour: tuple, bounding_box: tuple, interval: int) -> None:
        """Inits the guard
        """
        super().__init__(x, y, size, direction, body_colour, torch_colour, bounding_box, interval)
        self.torch.enable = True
        self.border_radius = 15
