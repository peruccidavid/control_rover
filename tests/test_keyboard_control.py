# filepath: /home/comprotic/Documents/control_rover/tests/test_keyboard_control.py
# ...existing code...
import unittest
from unittest.mock import patch

class Dummy:
    pass

class TestKeyboardControlImports(unittest.TestCase):
    @patch('src.control_motores.init_gpio', return_value=None)
    def test_import_keyboard_control(self, _):
        # simplemente asegurar que el módulo se puede importar y las funciones existen
        import importlib, sys
        sys.path.insert(0, 'src')
        kc = importlib.import_module('keyboard_control')
        self.assertTrue(hasattr(kc, 'main'))

if __name__ == '__main__':
    unittest.main()
