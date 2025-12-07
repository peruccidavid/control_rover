# filepath: /control_rover/control_rover/src/control_motores.py
# Bloque de simulación - Comentar o eliminar cuando se ejecute en el Pi
import sys
sys.path.append('.')

try:
    import RPi.GPIO as GPIO
except Exception:
    import mock_rpi_gpio as GPIO

import time

ESC_1_PIN = 18
ESC_2_PIN = 23
ESC_3_PIN = 24
ESC_4_PIN = 25
ESC_5_PIN = 19
ESC_6_PIN = 26

MOSFET_1_PIN = 17
MOSFET_2_PIN = 27
MOSFET_3_PIN = 22

def _use_mock():
    import mock_rpi_gpio as GPIO_mock
    GPIO_mock.setmode(GPIO_mock.BCM)
    return GPIO_mock

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in [ESC_1_PIN, ESC_2_PIN, ESC_3_PIN, ESC_4_PIN, ESC_5_PIN, ESC_6_PIN]:
        GPIO.setup(pin, GPIO.OUT)
    for pin in [MOSFET_1_PIN, MOSFET_2_PIN, MOSFET_3_PIN]:
        GPIO.setup(pin, GPIO.OUT)
except RuntimeError:
    GPIO = _use_mock()
    for pin in [ESC_1_PIN, ESC_2_PIN, ESC_3_PIN, ESC_4_PIN, ESC_5_PIN, ESC_6_PIN]:
        GPIO.setup(pin, GPIO.OUT)
    for pin in [MOSFET_1_PIN, MOSFET_2_PIN, MOSFET_3_PIN]:
        GPIO.setup(pin, GPIO.OUT)

PWM_FREQ = 50 
try:
    pwm_esc_1 = GPIO.PWM(ESC_1_PIN, PWM_FREQ)
    pwm_esc_2 = GPIO.PWM(ESC_2_PIN, PWM_FREQ)
    pwm_esc_3 = GPIO.PWM(ESC_3_PIN, PWM_FREQ)
    pwm_esc_4 = GPIO.PWM(ESC_4_PIN, PWM_FREQ)
    pwm_esc_5 = GPIO.PWM(ESC_5_PIN, PWM_FREQ)
    pwm_esc_6 = GPIO.PWM(ESC_6_PIN, PWM_FREQ)
except Exception:
    GPIO = _use_mock()
    if not hasattr(GPIO, "PWM"):
        class _DummyPWM:
            def __init__(self, pin, freq): pass
            def start(self, duty): pass
            def ChangeDutyCycle(self, duty): pass
            def stop(self): pass
        GPIO.PWM = _DummyPWM
    pwm_esc_1 = GPIO.PWM(ESC_1_PIN, PWM_FREQ)
    pwm_esc_2 = GPIO.PWM(ESC_2_PIN, PWM_FREQ)
    pwm_esc_3 = GPIO.PWM(ESC_3_PIN, PWM_FREQ)
    pwm_esc_4 = GPIO.PWM(ESC_4_PIN, PWM_FREQ)
    pwm_esc_5 = GPIO.PWM(ESC_5_PIN, PWM_FREQ)
    pwm_esc_6 = GPIO.PWM(ESC_6_PIN, PWM_FREQ)

pwm_esc_1.start(0)
pwm_esc_2.start(0)
pwm_esc_3.start(0)
pwm_esc_4.start(0)
pwm_esc_5.start(0)
pwm_esc_6.start(0)

def set_mosfet_state(state):
    level = GPIO.HIGH if state == "ON" else GPIO.LOW
    for pin in [MOSFET_1_PIN, MOSFET_2_PIN, MOSFET_3_PIN]:
        GPIO.output(pin, level)

def set_all_wheels_speed(duty_cycle):
    if duty_cycle < -100:
        duty_cycle = -100
    if duty_cycle > 100:
        duty_cycle = 100
    pwm_value = (duty_cycle + 100) / 2.0
    for pwm in [pwm_esc_1, pwm_esc_2, pwm_esc_3, pwm_esc_4, pwm_esc_5, pwm_esc_6]:
        pwm.ChangeDutyCycle(pwm_value)

def stop_all_wheels():
    set_all_wheels_speed(0)

def cleanup_gpio():
    pwm_esc_1.stop()
    pwm_esc_2.stop()
    pwm_esc_3.stop()
    pwm_esc_4.stop()
    pwm_esc_5.stop()
    pwm_esc_6.stop()
    GPIO.cleanup()

def move_forward():
    set_all_wheels_speed(100)

def move_backward():
    set_all_wheels_speed(-100)

def turn_right():
    set_all_wheels_speed(100)
    time.sleep(0.5)
    stop_all_wheels()

def turn_left():
    set_all_wheels_speed(100)
    time.sleep(0.5)
    stop_all_wheels()

try:
    print("Control del rover iniciado. Usa las teclas de flecha para controlar el movimiento.")
    while True:
        command = input("Ingresa 'w' para adelante, 's' para atrás, 'a' para izquierda, 'd' para derecha, 'x' para detener: ")
        if command == 'w':
            move_forward()
        elif command == 's':
            move_backward()
        elif command == 'a':
            turn_left()
        elif command == 'd':
            turn_right()
        elif command == 'x':
            stop_all_wheels()
except KeyboardInterrupt:
    print("Control detenido por el usuario.")
finally:
    cleanup_gpio()