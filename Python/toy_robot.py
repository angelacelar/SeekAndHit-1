from functools import wraps

from simulation_field import TableTop, Position


class ToyRobot():
    """ToyRobot
    A moving object on the TableTop field with a position.
    Each ToyRobot has an unique id.
    """

    def __init__(self):
        self.position = None

    def set_position(self, x, y, direction):
        """set_position
        Set the position of the robot.
        If the position is not valid according to the TableTop no position is set.

        :param x: x value
        :param y: y value
        :param direction: direction value
        """

        if TableTop.is_valid_position(x, y, direction):
            self.position = Position(x, y, direction)

    def _validate_position_initialized(f):
        """_validate_position_initialized
        Helper decorator which checks if ToyRobot instance has a position.
        A position is needed to execute commands move and rotate_right/rotate_left.

        :param f:
        """

        @wraps(f)
        def wrapper(inst, *args, **kwargs):
            toy_robot_instance = inst
            if not toy_robot_instance.position:
                return
            return f(inst, *args, **kwargs)
        return wrapper

    @_validate_position_initialized
    def move(self):
        """move
        Move the robot in the specified direction.
        If the next position of the robot would result in an incorrect position outside the
        TableTop field, the movement is ignored.
        """

        direction_value = TableTop.direction_values[self.position.direction]
        temp_x = self.position.x + direction_value['x']
        temp_y = self.position.y + direction_value['y']

        if temp_x in TableTop.valid_range and temp_y in TableTop.valid_range:
            self.position.x = temp_x
            self.position.y = temp_y

    def _calculate_rotation(self, leap):
        """_calculate_rotation
        Given the leap calculate the next direction of the robot.

        :param leap: 1 for clockwise or -1 for counter-clockwise
        """

        possible_directions = list(TableTop.direction_values.keys())
        new_direction = possible_directions[
            (possible_directions.index(self.position.direction) + leap + len(
                possible_directions)) % len(possible_directions)
        ]

        return new_direction

    @_validate_position_initialized
    def rotate_left(self):
        """rotate_left
        Rotate the robot to the left. Set the direction accordingly.
        """

        self.position.direction = self._calculate_rotation(-1)

    @_validate_position_initialized
    def rotate_right(self):
        """rotate_right
        Rotate the robot to the right. Set the direction accordingly.
        """

        self.position.direction = self._calculate_rotation(1)

    @_validate_position_initialized
    def report(self):
        """report
        Return the current position of the robot

        :return: string with current position of 'X,Y,F' format
        """

        return '{},{},{}'.format(self.position.x, self.position.y, self.position.direction)
