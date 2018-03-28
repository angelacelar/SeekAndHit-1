import unittest
from toy_robot import (
    ToyRobot
)
from simulation import (
    Simulation
)
from simulation_field import (
    TableTop
)
from input_parser import (
    get_commands_from_input,
    parse_place_command,
    InputException
)


class SimulationTest(unittest.TestCase):

    def test_simulation_test_case(self):
        simulation = Simulation('PLACE 0,0,NORTH MOVE REPORT')
        self.assertEqual(simulation.output_texts, ['0,1,NORTH'])

    def test_simulation_test_case_2(self):
        simulation = Simulation('PLACE 0,0,NORTH LEFT REPORT')
        self.assertEqual(simulation.output_texts, ['0,0,WEST'])

    def test_simulation_test_case_3(self):
        simulation = Simulation('PLACE 1,2,EAST MOVE MOVE LEFT MOVE REPORT')
        self.assertEqual(simulation.output_texts, ['3,3,NORTH'])

    def test_simulation_multiple_report(self):
        simulation = Simulation('PLACE 1,2,EAST MOVE REPORT MOVE LEFT MOVE REPORT')
        self.assertEqual(simulation.output_texts, ['2,2,EAST', '3,3,NORTH'])

    def test_simulation_test_case_4(self):
        simulation = Simulation('PLACE 0,0,EAST MOVE MOVE RIGHT MOVE MOVE REPORT')
        self.assertEqual(simulation.output_texts, ['2,0,SOUTH'])

    def test_simulation_movement_over_edge_x(self):
        simulation = Simulation('PLACE 0,0,NORTH RIGHT MOVE MOVE MOVE MOVE MOVE MOVE REPORT')
        self.assertEqual(simulation.output_texts, ['4,0,EAST'])

    def test_simulation_movement_over_edge_y(self):
        simulation = Simulation('PLACE 0,0,NORTH MOVE MOVE MOVE MOVE MOVE MOVE REPORT')
        self.assertEqual(simulation.output_texts, ['0,4,NORTH'])

    def test_simulation_movement_over_edge_x_and_y(self):
        simulation = Simulation('PLACE 0,0,WEST MOVE LEFT MOVE MOVE MOVE REPORT')
        self.assertEqual(simulation.output_texts, ['0,0,SOUTH'])

        simulation = Simulation('PLACE 0,0,EAST LEFT LEFT MOVE MOVE MOVE REPORT')
        self.assertEqual(simulation.output_texts, ['0,0,WEST'])

    def test_simulation_movement_over_edge_x_and_y_north_east_corner(self):
        simulation = Simulation('PLACE 4,4,EAST MOVE LEFT MOVE MOVE MOVE MOVE REPORT')
        self.assertEqual(simulation.output_texts, ['4,4,NORTH'])

        simulation = Simulation('PLACE 4,4,NORTH MOVE RIGHT MOVE MOVE MOVE REPORT')
        self.assertEqual(simulation.output_texts, ['4,4,EAST'])

    def test_simulation_with_multiple_place_commands(self):
        simulation = Simulation('PLACE 4,4,EAST MOVE LEFT MOVE REPORT PLACE 1,2,WEST MOVE MOVE MOVE REPORT')
        self.assertEqual(simulation.output_texts, ['4,4,NORTH', '0,2,WEST'])

        simulation = Simulation('PLACE 4,4,EAST MOVE LEFT MOVE REPORT PLACE 1,2,WEST MOVE MOVE MOVE')
        self.assertEqual(simulation.output_texts, ['4,4,NORTH'])


class TestToyRobotWithoutPosition(unittest.TestCase):
    def setUp(self):
        self.toy_robot = ToyRobot()

    def test_commands_while_position_is_not_set(self):
        self.toy_robot.move()
        self.toy_robot.rotate_right()
        self.toy_robot.rotate_left()
        self.assertIsNone(self.toy_robot.position)


class TestToyRobotPosition(unittest.TestCase):
    def setUp(self):
        self.toy_robot = ToyRobot()
        self.toy_robot.set_position(0, 0, 'EAST')

    def test_rotate_left(self):
        self.toy_robot.rotate_left()
        self.assertEqual(self.toy_robot.position.direction, 'NORTH')

    def test_rotate_right(self):
        self.toy_robot.rotate_right()
        self.assertEqual(self.toy_robot.position.direction, 'SOUTH')

    def test_set_position(self):
        self.assertEqual(self.toy_robot.position.x, 0)
        self.assertEqual(self.toy_robot.position.y, 0)
        self.assertEqual(self.toy_robot.position.direction, 'EAST')


class TestToyRobotMovement(unittest.TestCase):
    def setUp(self):
        self.toy_robot = ToyRobot()
        self.toy_robot.set_position(0, 0, 'EAST')

    def test_move_and_rotate(self):
        self.toy_robot.move()
        self.toy_robot.move()
        self.toy_robot.rotate_left()
        self.toy_robot.move()
        self.toy_robot.move()
        self.assertEqual(self.toy_robot.position.x, 2)
        self.assertEqual(self.toy_robot.position.y, 2)
        self.assertEqual(self.toy_robot.position.direction, 'NORTH')


class TestGetCommandsFromInput(unittest.TestCase):
    def test_other_commands_ignored_before_place(self):
        commands = get_commands_from_input('MOVE RIGHT PLACE 3,1,NORTH')
        self.assertEqual(commands, ['PLACE 3,1,NORTH'])

    def test_multiple_place_commands(self):
        commands = get_commands_from_input('PLACE 3,1,NORTH  MOVE PLACE 4,5,NORTH')
        self.assertEqual(commands, ['PLACE 3,1,NORTH', 'MOVE', 'PLACE 4,5,NORTH'])


class TestParsePlaceCommand(unittest.TestCase):
    def test_valid_format(self):
        self.assertEqual(parse_place_command('PLACE 3,1,NORTH'), (3, 1, 'NORTH'))

    def test_invalid_format_space_after_comma(self):
        with self.assertRaises(InputException) as ctx:
            parse_place_command('PLACE 3,1, NORTH')
        self.assertEqual(ctx.exception.args[0], 'Toy robot begin position command is not valid.')

    def test_invalid_format_wrong_order(self):
        with self.assertRaises(InputException) as ctx:
            parse_place_command('PLACE NORTH,1,2')
        self.assertEqual(ctx.exception.args[0], 'Toy robot begin position command is not valid.')

    def test_invalid_format_missing_arguments(self):
        with self.assertRaises(InputException) as ctx:
            parse_place_command('PLACE ')
        self.assertEqual(ctx.exception.args[0], 'Toy robot begin position command is not valid.')


class TestTableTop(unittest.TestCase):

    def test_is_valid_position(self):
        is_valid = TableTop.is_valid_position(1, 2, '2')
        self.assertEqual(is_valid, False)

        is_valid = TableTop.is_valid_position(1, 1, 'test')
        self.assertEqual(is_valid, False)

        is_valid = TableTop.is_valid_position(1, 1, 'EAST')
        self.assertEqual(is_valid, True)

        is_valid = TableTop.is_valid_position(1, 1, 'NORTHEAST')
        self.assertEqual(is_valid, False)

        is_valid = TableTop.is_valid_position('TEST', 2, 2)
        self.assertEqual(is_valid, False)

        is_valid = TableTop.is_valid_position(2, 2, 2)
        self.assertEqual(is_valid, False)


if __name__ == '__main__':
    unittest.main()
