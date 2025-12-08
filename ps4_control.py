"""
Control PS4 (DualShock4) usando pygame.
Conecta el mando por USB o Bluetooth y ejecuta:
  venv\Scripts\Activate.ps1
  python ps4_control.py

Joystick izquierdo: movimiento/giro.
Botón OPTIONS (o botón 9) para salir; botón Círculo (ej. 1) para detener.
"""
import time
import pygame
import sys
from control_motores import init_gpio, set_mosfet_state, set_side_speeds, stop_all_wheels, cleanup_gpio

DEADZONE = 0.15
SCALE = 100
POLL_DELAY = 0.02

def _dead(v):
    return 0.0 if abs(v) < DEADZONE else v

def _mix(throttle, turn):
    left = throttle + turn
    right = throttle - turn
    m = max(abs(left), abs(right), 1.0)
    left = left / m
    right = right / m
    return int(left * SCALE), int(right * SCALE)

def main():
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("No se detectó joystick. Conecta el mando y vuelve a intentar.")
        return

    js = pygame.joystick.Joystick(0)
    js.init()
    print("Joystick:", js.get_name(), "axes:", js.get_numaxes(), "buttons:", js.get_numbuttons())

    init_gpio()
    set_mosfet_state("ON")
    try:
        running = True
        while running:
            pygame.event.pump()
            # Ajusta ejes si tu controlador reporta índices distintos
            ax_x = _dead(js.get_axis(0))
            ax_y = _dead(js.get_axis(1))
            throttle = -ax_y
            turn = ax_x
            left, right = _mix(throttle, turn)
            set_side_speeds(left, right)
            print(f"\rIzquierda: {left: 4d}, Derecha: {right: 4d} \n")

            # Salir con botón OPTIONS (index 9 en muchos drivers)
            if js.get_numbuttons() > 9 and js.get_button(9):
                running = False
            # Detener con botón Círculo (ejemplo índice 1)
            if js.get_numbuttons() > 1 and js.get_button(1):
                stop_all_wheels()

            time.sleep(POLL_DELAY)
    except KeyboardInterrupt:
        pass
    finally:
        print("\nDeteniendo motores y limpiando GPIO...")
        stop_all_wheels()
        set_mosfet_state("OFF")
        cleanup_gpio()
        js.quit()
        pygame.quit()

if __name__ == "__main__":
    main()