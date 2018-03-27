import unittest
from toy_robot import ToyRobot, move_to_begining_of_commands, parse_commands, proper_positioning


class TestToyRobot(unittest.TestCase):
    def setUp(self):
        self.toy_robot = ToyRobot()
        self.toy_robot.set_position(0, 0, 'EAST')

    def test_set_position(self):
        self.assertEqual(self.toy_robot._position['x'], 0)
        self.assertEqual(self.toy_robot._position['y'], 0)
        self.assertEqual(self.toy_robot._position['direction'], 'EAST')

        self.toy_robot.set_position(1, 1, 'WEST')
        self.assertEqual(self.toy_robot._position['x'], 1)
        self.assertEqual(self.toy_robot._position['y'], 1)
        self.assertEqual(self.toy_robot._position['direction'], 'WEST')

    def test_is_valid_position(self):
        is_valid = self.toy_robot.is_valid_position('1', '2', '2')
        self.assertEqual(is_valid, False)

        is_valid = self.toy_robot.is_valid_position('1', '1', 'test')
        self.assertEqual(is_valid, False)

        is_valid = self.toy_robot.is_valid_position('1', '1', 'EAST')
        self.assertEqual(is_valid, True)

    def test_rotate_left(self):
        self.toy_robot.rotate_left()
        self.assertEqual(self.toy_robot._position['direction'], 'NORTH')

    def test_rotate_right(self):
        self.toy_robot.rotate_right()
        self.assertEqual(self.toy_robot._position['direction'], 'SOUTH')

    def test_parse_commands(self):
        parse_commands((['test', 'TEST', 'move']), self.toy_robot)
        self.assertEqual(self.toy_robot._position['x'], 0)
        self.assertEqual(self.toy_robot._position['y'], 0)
        self.assertEqual(self.toy_robot._position['direction'], 'EAST')

        parse_commands((['MOVE', 'MOVE', 'LEFT', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot._position['x'], 2)
        self.assertEqual(self.toy_robot._position['y'], 2)
        self.assertEqual(self.toy_robot._position['direction'], 'NORTH')

        self.toy_robot.set_position(0, 0, 'EAST')
        parse_commands((['MOVE', 'MOVE', 'RIGHT', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot._position['x'], 2)
        self.assertEqual(self.toy_robot._position['y'], 0)
        self.assertEqual(self.toy_robot._position['direction'], 'SOUTH')

        # test movement to the edge
        self.toy_robot.set_position(0, 0, 'NORTH')
        parse_commands((['RIGHT', 'MOVE', 'MOVE', 'MOVE', 'MOVE', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot._position['x'], 4)
        self.assertEqual(self.toy_robot._position['y'], 0)
        self.assertEqual(self.toy_robot._position['direction'], 'EAST')

        # test movement to the edge
        self.toy_robot.set_position(0, 0, 'NORTH')
        parse_commands((['MOVE', 'MOVE', 'MOVE', 'MOVE', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot._position['x'], 0)
        self.assertEqual(self.toy_robot._position['y'], 4)
        self.assertEqual(self.toy_robot._position['direction'], 'NORTH')

        # test movement over the edge if in 0 0
        self.toy_robot.set_position(0, 0, 'WEST')
        parse_commands((['LEFT', 'MOVE', 'MOVE', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot._position['x'], 0)
        self.assertEqual(self.toy_robot._position['y'], 0)
        self.assertEqual(self.toy_robot._position['direction'], 'SOUTH')

        # test movement over the edge if in 0 0
        self.toy_robot.set_position(0, 0, 'EAST')
        parse_commands((['LEFT', 'LEFT', 'MOVE', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot._position['x'], 0)
        self.assertEqual(self.toy_robot._position['y'], 0)
        self.assertEqual(self.toy_robot._position['direction'], 'WEST')

        # test movement over the edge if in 4 4
        self.toy_robot.set_position(4, 4, 'EAST')
        parse_commands((['MOVE', 'MOVE', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot._position['x'], 4)
        self.assertEqual(self.toy_robot._position['y'], 4)
        self.assertEqual(self.toy_robot._position['direction'], 'EAST')

        # test movement over the edge if in 4 4
        self.toy_robot.set_position(4, 4, 'NORTH')
        parse_commands((['RIGHT', 'MOVE', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot._position['x'], 4)
        self.assertEqual(self.toy_robot._position['y'], 4)
        self.assertEqual(self.toy_robot._position['direction'], 'EAST')

    def test_move_to_begining_of_commands(self):
        self.assertEqual(move_to_begining_of_commands(['PLACE']), [])
        self.assertEqual(move_to_begining_of_commands(['PLACE', 'TEST']), ['TEST'])
        self.assertEqual(move_to_begining_of_commands(
            ['PLACE', '1,2,EAST', 'PLACE', 'TEST']), ['TEST'])

    def test_proper_positioning(self):
        is_valid = proper_positioning(['TEST', '2'], self.toy_robot)
        self.assertEqual(is_valid, False)

        is_valid = proper_positioning(['TEST', '2', '2'], self.toy_robot)
        self.assertEqual(is_valid, False)

        is_valid = proper_positioning(['2', '2', '2'], self.toy_robot)
        self.assertEqual(is_valid, False)

        is_valid = proper_positioning(['2', '2', 'EAST'], self.toy_robot)
        self.assertEqual(is_valid, True)

        self.assertEqual(self.toy_robot._position['x'], 2)
        self.assertEqual(self.toy_robot._position['y'], 2)
        self.assertEqual(self.toy_robot._position['direction'], 'EAST')


if __name__ == '__main__':
    unittest.main()
