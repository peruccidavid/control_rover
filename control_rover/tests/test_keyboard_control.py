import unittest
from unittest.mock import patch, MagicMock
from src.keyboard_control import RoverController

class TestRoverController(unittest.TestCase):

    @patch('src.keyboard_control.RoverController.move_forward')
    def test_move_forward(self, mock_move_forward):
        controller = RoverController()
        controller.handle_key_press('up')
        mock_move_forward.assert_called_once()

    @patch('src.keyboard_control.RoverController.turn_right')
    def test_turn_right(self, mock_turn_right):
        controller = RoverController()
        controller.handle_key_press('right')
        mock_turn_right.assert_called_once()

    @patch('src.keyboard_control.RoverController.turn_left')
    def test_turn_left(self, mock_turn_left):
        controller = RoverController()
        controller.handle_key_press('left')
        mock_turn_left.assert_called_once()

    @patch('src.keyboard_control.RoverController.stop')
    def test_stop(self, mock_stop):
        controller = RoverController()
        controller.handle_key_press('down')
        mock_stop.assert_called_once()

    @patch('src.keyboard_control.RoverController.reverse')
    def test_reverse(self, mock_reverse):
        controller = RoverController()
        controller.handle_key_press('down')
        mock_reverse.assert_called_once()

if __name__ == '__main__':
    unittest.main()