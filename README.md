# filepath: /home/comprotic/Documents/control_rover/README.md
# ...existing code...
Proyecto de prueba para controlar un rover (simulación).

Estructura:
- src/: código fuente (control_motores.py, keyboard_control.py)
- tests/: tests básicos

Cómo ejecutar (desde la raíz del proyecto):
  python3 src/keyboard_control.py

Nota: el controlador por teclado usa curses (Linux). En Raspberry Pi el módulo RPi.GPIO se usará;
en PC se hace fallback a mock_rpi_gpio si está disponible.
