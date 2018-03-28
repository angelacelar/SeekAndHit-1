"""
Utility functions related to user input
"""
import re


class InputException(Exception):
    """InputException
    Custom exception class which is raise when user input is of incorrect format.
    """
    pass


def get_commands_from_input(input_text):
    """get_commands_from_input
    Transforms the input text from the user to individual commands.

    User commands can be of type 'PLACE X,Y,F MOVE LEFT RIGHT REPORT'

    :param input_text: String of text containing multiple commands
    :return: list of commands after first PLACE command. Commands returned are of strings.
    """
    input_regex = re.compile(r'PLACE\s*?\S+|MOVE|REPORT|LEFT|RIGHT')
    commands = input_regex.findall(input_text)

    try:
        index_first_place_command = next(
            index for index, c in enumerate(commands) if c.startswith('PLACE'))
    except StopIteration:
        raise InputException('You didn\'t issue a PLACE command')

    return commands[index_first_place_command:]


def parse_place_command(command):
    """parse_place_command
    Validates that the PLACE command has good format and returns the X,Y,F values.

    :param command: String command of format 'PLACE X,Y,F'
    :return: tuple (x, y, F)
    """
    command_subparts = command.split(' ')
    if len(command_subparts) != 2:
        raise InputException('Toy robot begin position command is not valid.')
    command_coordinates = command_subparts[1].split(',')
    if len(command_coordinates) != 3:
        raise InputException('Toy robot begin position command is not valid.')
    x, y, direction = command_coordinates
    if not x or not x.isdigit() or not y or not y.isdigit() or not direction:
        raise InputException('Toy robot begin position command is not valid.')
    return int(x), int(y), direction
