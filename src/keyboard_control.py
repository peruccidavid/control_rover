# filepath: /home/comprotic/Documents/control_rover/src/keyboard_control.py
# ...existing code...
"""
Control simple por teclado usando curses.
Flechas: arriba=adelante a toda velocidad, abajo=retroceso a toda velocidad,
derecha=girar 45° derecha, izquierda=girar 45° izquierda, espacio=detener, q=salir.
Ejecutar: python3 src/keyboard_control.py
"""
import curses
import time
from control_motores import init_gpio, set_mosfet_state, set_side_speeds, set_all_wheels_speed, stop_all_wheels, cleanup_gpio

# parámetros de giro (ajustar durante pruebas)
TURN_45_LEFT = (60, 20)   # (left_speed, right_speed)
TURN_45_RIGHT = (20, 60)

FULL_FORWARD = 100
FULL_REVERSE = -100

def main(stdscr):
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.addstr(0,0,"Control por teclado: ↑ adelante, ↓ atrás, ← 45° izq, → 45° der, espacio detener, q salir")
    init_gpio()
    set_mosfet_state("ON")
    try:
        while True:
            key = stdscr.getch()
            if key == curses.KEY_UP:
                set_all_wheels_speed(FULL_FORWARD)
                stdscr.addstr(2,0,"Adelante a toda velocidad   ")
            elif key == curses.KEY_DOWN:
                set_all_wheels_speed(FULL_REVERSE)
                stdscr.addstr(2,0,"Retroceso a toda velocidad ")
            elif key == curses.KEY_LEFT:
                left, right = TURN_45_LEFT
                set_side_speeds(left, right)
                stdscr.addstr(2,0,"Giro 45° izquierda          ")
            elif key == curses.KEY_RIGHT:
                left, right = TURN_45_RIGHT
                set_side_speeds(left, right)
                stdscr.addstr(2,0,"Giro 45° derecha           ")
            elif key == ord(' '):
                stop_all_wheels()
                stdscr.addstr(2,0,"Detenido                   ")
            elif key in (ord('q'), ord('Q')):
                break
            time.sleep(0.05)
    finally:
        stop_all_wheels()
        set_mosfet_state("OFF")
        cleanup_gpio()

if __name__ == "__main__":
    curses.wrapper(main)
# ...existing code...
