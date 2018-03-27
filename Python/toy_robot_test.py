import unittest
from toy_robot import ToyRobot, Position, find_first_place_command, parse_commands


class TestToyRobot(unittest.TestCase):
    def setUp(self):
        self.toy_robot = ToyRobot()
        self.toy_robot.set_position(0, 0, 'EAST')

    def test_set_position(self):
        self.assertEqual(self.toy_robot.position.x, 0)
        self.assertEqual(self.toy_robot.position.y, 0)
        self.assertEqual(self.toy_robot.position.direction, 'EAST')

        self.toy_robot.set_position(1, 1, 'WEST')
        self.assertEqual(self.toy_robot.position.x, 1)
        self.assertEqual(self.toy_robot.position.y, 1)
        self.assertEqual(self.toy_robot.position.direction, 'WEST')

    def test_rotate_left(self):
        self.toy_robot.rotate_left()
        self.assertEqual(self.toy_robot.position.direction, 'NORTH')

    def test_rotate_right(self):
        self.toy_robot.rotate_right()
        self.assertEqual(self.toy_robot.position.direction, 'SOUTH')

    def test_parse_commands(self):
        parse_commands((['test', 'TEST', 'move']), self.toy_robot)
        self.assertEqual(self.toy_robot.position.x, 0)
        self.assertEqual(self.toy_robot.position.y, 0)
        self.assertEqual(self.toy_robot.position.direction, 'EAST')

        parse_commands((['MOVE', 'MOVE', 'LEFT', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot.position.x, 2)
        self.assertEqual(self.toy_robot.position.y, 2)
        self.assertEqual(self.toy_robot.position.direction, 'NORTH')

        self.toy_robot.set_position(0, 0, 'EAST')
        parse_commands((['MOVE', 'MOVE', 'RIGHT', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot.position.x, 2)
        self.assertEqual(self.toy_robot.position.y, 0)
        self.assertEqual(self.toy_robot.position.direction, 'SOUTH')

        # test movement over the edge on x
        self.toy_robot.set_position(0, 0, 'NORTH')
        parse_commands((['RIGHT', 'MOVE', 'MOVE', 'MOVE', 'MOVE', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot.position.x, 4)
        self.assertEqual(self.toy_robot.position.y, 0)
        self.assertEqual(self.toy_robot.position.direction, 'EAST')

        # test movement over the edge on y
        self.toy_robot.set_position(0, 0, 'NORTH')
        parse_commands((['MOVE', 'MOVE', 'MOVE', 'MOVE', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot.position.x, 0)
        self.assertEqual(self.toy_robot.position.y, 4)
        self.assertEqual(self.toy_robot.position.direction, 'NORTH')

        # test movement over the edge if in 0 0
        self.toy_robot.set_position(0, 0, 'WEST')
        parse_commands((['LEFT', 'MOVE', 'MOVE', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot.position.x, 0)
        self.assertEqual(self.toy_robot.position.y, 0)
        self.assertEqual(self.toy_robot.position.direction, 'SOUTH')

        # test movement over the edge if in 0 0
        self.toy_robot.set_position(0, 0, 'EAST')
        parse_commands((['LEFT', 'LEFT', 'MOVE', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot.position.x, 0)
        self.assertEqual(self.toy_robot.position.y, 0)
        self.assertEqual(self.toy_robot.position.direction, 'WEST')

        # test movement over the edge if in 4 4
        self.toy_robot.set_position(4, 4, 'EAST')
        parse_commands((['MOVE', 'MOVE', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot.position.x, 4)
        self.assertEqual(self.toy_robot.position.y, 4)
        self.assertEqual(self.toy_robot.position.direction, 'EAST')

        # test movement over the edge if in 4 4
        self.toy_robot.set_position(4, 4, 'NORTH')
        parse_commands((['RIGHT', 'MOVE', 'MOVE', 'MOVE']), self.toy_robot)
        self.assertEqual(self.toy_robot.position.x, 4)
        self.assertEqual(self.toy_robot.position.y, 4)
        self.assertEqual(self.toy_robot.position.direction, 'EAST')

    def test_find_first_place_command(self):
        self.assertEqual(find_first_place_command(['PLACE']), [])
        self.assertEqual(find_first_place_command(['PLACE', 'TEST']), ['TEST'])
        self.assertEqual(find_first_place_command(
            ['PLACE', '1,2,EAST', 'PLACE', 'TEST']), ['TEST'])

    def test_set_initial_robot_position(self):
        is_valid = self.toy_robot.set_initial_robot_position(['TEST', '2'])
        self.assertEqual(is_valid, False)

        is_valid = self.toy_robot.set_initial_robot_position(['TEST', '2', '2'])
        self.assertEqual(is_valid, False)

        is_valid = self.toy_robot.set_initial_robot_position(['2', '2', '2'])
        self.assertEqual(is_valid, False)

        is_valid = self.toy_robot.set_initial_robot_position(['2', '2', 'EAST'])
        self.assertEqual(is_valid, True)

        self.assertEqual(self.toy_robot.position.x, 2)
        self.assertEqual(self.toy_robot.position.y, 2)
        self.assertEqual(self.toy_robot.position.direction, 'EAST')


class TestPosition(unittest.TestCase):
    def setUp(self):
        self.position = Position()

    def test_is_valid_position(self):
        is_valid = self.position.is_valid_position('1', '2', '2')
        self.assertEqual(is_valid, False)

        is_valid = self.position.is_valid_position('1', '1', 'test')
        self.assertEqual(is_valid, False)

        is_valid = self.position.is_valid_position('1', '1', 'EAST')
        self.assertEqual(is_valid, True)


if __name__ == '__main__':
    unittest.main()
