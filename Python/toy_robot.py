from collections import OrderedDict


class InputException(Exception):
    pass


class ToyRobot:
    _position = {'direction': None, 'x': None, 'y': None}
    direction_values = OrderedDict([
        ('NORTH', {'x': 0, 'y': 1}),
        ('EAST', {'x': 1, 'y': 0}),
        ('SOUTH', {'x': 0, 'y': -1}),
        ('WEST', {'x': -1, 'y': 0})
    ])

    _valid_range = range(0, 5)

    def set_position(self, x, y, direction):
        self._position = {'direction': direction, 'x': x, 'y': y}

    def is_valid_position(self, x, y, direction):
        if (int(x) in self._valid_range and int(y) in self._valid_range and
                direction in self.direction_values):

            return True
        else:
            return False

    def move_robot(self):
        direction_value = self.direction_values[self._position['direction']]
        temp_x = self._position['x'] + direction_value['x']
        temp_y = self._position['y'] + direction_value['y']

        if temp_x in self._valid_range and temp_y in self._valid_range:
            self._position['x'] = temp_x
            self._position['y'] = temp_y

    def calculate_rotation(self, direction, leap):
        possible_directions = self.direction_values.keys()
        return possible_directions[(possible_directions.index(direction) + leap + len(possible_directions)) % len(possible_directions)]

    def rotate_left(self):
        self._position['direction'] = self.calculate_rotation(self._position['direction'], -1)

    def rotate_right(self):
        self._position['direction'] = self.calculate_rotation(self._position['direction'], 1)

    def report(self):
        print self._position['x'], self._position['y'], self._position['direction']


def move_to_begining_of_commands(commands):
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
            toy_robot.move_robot()
        elif command == 'REPORT':
            toy_robot.report()


def proper_positioning(positioning, toy_robot):
    if (len(positioning) == 3 and positioning[0].isdigit() and positioning[1].isdigit() and
            toy_robot.is_valid_position(positioning[0], positioning[1], positioning[2])):

        toy_robot.set_position(int(positioning[0]), int(positioning[1]), positioning[2])

        return True
    return False


def main(text):
    toy_robot = ToyRobot()
    commands = move_to_begining_of_commands(text.split())

    if len(commands):
        positioning_command = commands[0].split(',')

        if proper_positioning(positioning_command, toy_robot):
            parse_commands(commands[1:], toy_robot)
        else:
            raise InputException('Toy robot begin position command is not valid.')
    else:
        raise InputException("You didn't issue PLACE command")


if __name__ == '__main__':
    command_text = raw_input("Please, type your commands: ")
    main(command_text)
