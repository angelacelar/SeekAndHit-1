from collections import OrderedDict


class TableTop():
    """TableTop
    Describes the simulation field (the environment)

    Attributes:
        direction_values - Contains the possible directions of an object and the specified
                           values of movement in that direaction
        valid_range -     Possible range of a 5x5 0-indexed field

    """

    direction_values = OrderedDict([
        ('NORTH', {'x': 0, 'y': 1}),
        ('EAST', {'x': 1, 'y': 0}),
        ('SOUTH', {'x': 0, 'y': -1}),
        ('WEST', {'x': -1, 'y': 0})
    ])

    valid_range = range(0, 5)

    @classmethod
    def is_valid_position(cls, x, y, direction):
        """is_valid_position
        Checks if the position (x, y) is in valid_range and direction is allowed value.

        :param x: x
        :param y: y
        :param direction: direction
        """

        if (x in cls.valid_range and y in cls.valid_range and
                direction in cls.direction_values):
            return True
        else:
            return False


class Position():
    """Position
    Represents a position of an object on the TableTop
    """

    def __init__(self, x, y, direction):
        self.direction = direction
        self.x = x
        self.y = y

    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.direction)
