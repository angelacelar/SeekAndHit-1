from collections import OrderedDict


class InputException(Exception):
    pass


class TableTop(object):
    direction_values = OrderedDict([
        ('NORTH', {'x': 0, 'y': 1}),
        ('EAST', {'x': 1, 'y': 0}),
        ('SOUTH', {'x': 0, 'y': -1}),
        ('WEST', {'x': -1, 'y': 0})
    ])

    valid_range = range(0, 5)


class Position(object):
    direction = None
    x = None
    y = None

    def __init__(self, direction='EAST', x=0, y=0):
        self.direction = direction
        self.x = int(x)
        self.y = int(y)

    def is_valid_position(self, x, y, direction):
        if (int(x) in TableTop.valid_range and int(y) in TableTop.valid_range and
                direction in TableTop.direction_values):
            return True
        else:
            return False


class ToyRobot(object):
    position = Position()

    def set_position(self, x, y, direction):
        self.position.x = x
        self.position.y = y
        self.position.direction = direction

    def change_position(self):
        direction_value = TableTop.direction_values[self.position.direction]
        temp_x = self.position.x + direction_value['x']
        temp_y = self.position.y + direction_value['y']

        if temp_x in TableTop.valid_range and temp_y in TableTop.valid_range:
            self.position.x = temp_x
            self.position.y = temp_y

    def _calculate_rotation(self, direction, leap):
        possible_directions = TableTop.direction_values.keys()
        return possible_directions[(possible_directions.index(direction) + leap + len(
            possible_directions)) % len(possible_directions)]

    def rotate_left(self):
        self.position.direction = self._calculate_rotation(self.position.direction, -1)

    def rotate_right(self):
        self.position.direction = self._calculate_rotation(self.position.direction, 1)

    def report(self):
        print self.position.x, self.position.y, self.position.direction

    def set_initial_robot_position(self, positioning):
        if (len(positioning) == 3 and positioning[0].isdigit() and positioning[1].isdigit() and
                self.position.is_valid_position(positioning[0], positioning[1], positioning[2])):

            self.set_position(int(positioning[0]), int(positioning[1]), positioning[2])

            return True
        return False


def find_first_place_command(commands):
        places_command = [index for index, c in enumerate(commands) if c == 'PLACE']

        if len(places_command) and len(commands) > 1:
            index_last_place_command = places_command[-1]

            return commands[index_last_place_command + 1:]
        return []


def parse_commands(commands, toy_robot):
    for command in commands:
        if command == 'LEFT':
            toy_robot.rotate_left()
        elif command == 'RIGHT':
            toy_robot.rotate_right()
        elif command == 'MOVE':
            toy_robot.change_position()
        elif command == 'REPORT':
            toy_robot.report()


def main(text):
    toy_robot = ToyRobot()
    commands = find_first_place_command(text.split())

    if len(commands):
        positioning_command = commands[0].split(',')

        if toy_robot.set_initial_robot_position(positioning_command):
            parse_commands(commands[1:], toy_robot)
        else:
            raise InputException('Toy robot begin position command is not valid.')
    else:
        raise InputException("You didn't issue PLACE command")


if __name__ == '__main__':
    command_text = raw_input("Please, type your commands: ")
    main(command_text)
