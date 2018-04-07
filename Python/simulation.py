from toy_robot import ToyRobot
from input_parser import get_commands_from_input, parse_place_command


class Simulation():
    """Simulation
    Represents one simulation in which for a given text one toy_robot is created and
    does the commands specified.
    After executing all the commands the results of each REPORT command are outputed to stdout.
    """

    def __init__(self, command_text):
        self.commands = get_commands_from_input(command_text)
        self.output_texts = []
        self.toy_robot = ToyRobot()
        self.movement_dict = {
            'LEFT': self.toy_robot.rotate_left,
            'RIGHT': self.toy_robot.rotate_right,
            'MOVE': self.toy_robot.move
        }
        self.execute_commands()
        self.output_results()

    def execute_commands(self):
        """execute_commands
        For each command in self.commands call the appropriate ToyRobot action
        """

        for command in self.commands:
            if command in self.movement_dict:
                self.movement_dict[command]()
            elif command == 'REPORT':
                report = self.toy_robot.report()
                if report:
                    self.output_texts.append(report)
            elif command.startswith('PLACE'):
                try:
                    x, y, direction = parse_place_command(command)
                    self.toy_robot.set_position(x, y, direction)
                except InputException:
                    '''Exception
                    Silently ignore it to continue robot movement
                    '''
                    continue

    def output_results(self):
        """output_results
        Output all the texts available in self.output_texts which were filled
        in execute_commands
        """

        for output_text in self.output_texts:
            print(output_text)


if __name__ == '__main__':
    commands_text = input('Please, type your commands: ')
    Simulation(commands_text)
