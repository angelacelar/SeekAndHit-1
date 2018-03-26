class InputException(Exception):
    pass

class ToyRobot:
    _position = {
        'x': None,
        'y': None,
        'direction': None
    }
    _valid_range = range(0, 4)
    _direction_names = ['NORTH', 'EAST', 'SOUTH', 'WEST']

    def _set_position(self, x, y, direction):
        self._position = {
            'x': x,
            'y': y,
            'direction': direction
        }

    def is_valid_position(self, x, y, direction):
        if (x.isdigit() and int(x) in self._valid_range and y.isdigit() and int(y) in self._valid_range and
                direction in self._direction_names):
            self._set_position(int(x),int(y), self._direction_names.index(direction))
            return True
        else:
            return False

    def move_robot(self):
        if self._position['direction'] == 0:
            if self._position['y'] < 4:
                self._position['y'] += 1
        elif self._position['direction'] == 1:
            if self._position['x'] < 4:
                self._position['x'] += 1
        elif self._position['direction'] == 2:
            if self._position['y'] > 0:
                self._position['y'] -= 1
        elif self._position['direction'] == 3:
            if self._position['x'] > 0:
                self._position['x'] -= 1

    def rotate_left(self):
        self._position['direction'] = ((self._position['direction'] - 1) + 4) % 4

    def rotate_right(self):
        self._position['direction'] = (self._position['direction'] + 1) % 4

    def report(self):
        print self._position['x'], self._position['y'], self._direction_names[self._position['direction']]


def parse_input(command):
    if command == 'LEFT':
        toy_robot.rotate_left()
    elif command == 'RIGHT':
        toy_robot.rotate_right()
    elif command == 'MOVE':
        toy_robot.move_robot()
    elif command == 'REPORT':
        toy_robot.report()


def main():
    test = raw_input("Please, type your commands: ")
    commands = test.split()

    last_set_places = [index for index, c in enumerate(commands) if c == 'PLACE']

    # check if there is PLACE command, and if there are commands after PLACE
    if len(last_set_places) and len(commands) > 1:
        index_last_set_place = last_set_places[-1]

        # set command after PLACE command to starting command
        commands = commands[index_last_set_place+1:]
        positioning_command = commands[0].split(',')

        if len(positioning_command) == 3 and toy_robot.is_valid_position(positioning_command[0], positioning_command[1], positioning_command[2]):
            for command in commands[1:]:
                parse_input(command)
        else:
            raise InputException, 'Toy robot begin position command is not valid.'
    else:
        raise InputException, "You didn't issue PLACE command"

toy_robot = ToyRobot()
main()
