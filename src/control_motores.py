# filepath: /home/comprotic/Documents/control_rover/src/control_motores.py
# ...existing code...
import sys
sys.path.append('.')

# Intentar usar RPi.GPIO; si falla en import o en cualquier operación de inicialización,
# hacer fallback a mock_rpi_gpio para poder ejecutar en el PC/simulador.
try:
    import RPi.GPIO as GPIO
except Exception:
    import mock_rpi_gpio as GPIO

import time

# Configuración de pines (usando el modo BCM)
ESC_1_PIN = 18
ESC_2_PIN = 23
ESC_3_PIN = 24
ESC_4_PIN = 25
ESC_5_PIN = 19
ESC_6_PIN = 26

MOSFET_1_PIN = 17
MOSFET_2_PIN = 27
MOSFET_3_PIN = 22

PWM_FREQ = 50

# Inicialización con fallback a mock, sin ejecutar operaciones en import si posible.
def init_gpio():
    """Inicializa GPIO y PWM. Llamar una vez desde el programa que controle el rover."""
    def _use_mock():
        import mock_rpi_gpio as GPIO_mock
        GPIO_mock.setmode(GPIO_mock.BCM)
        return GPIO_mock

    global GPIO, pwm_esc_1, pwm_esc_2, pwm_esc_3, pwm_esc_4, pwm_esc_5, pwm_esc_6

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in [ESC_1_PIN, ESC_2_PIN, ESC_3_PIN, ESC_4_PIN, ESC_5_PIN, ESC_6_PIN]:
            GPIO.setup(pin, GPIO.OUT)
        for pin in [MOSFET_1_PIN, MOSFET_2_PIN, MOSFET_3_PIN]:
            GPIO.setup(pin, GPIO.OUT)
    except Exception:
        GPIO = _use_mock()
        for pin in [ESC_1_PIN, ESC_2_PIN, ESC_3_PIN, ESC_4_PIN, ESC_5_PIN, ESC_6_PIN]:
            GPIO.setup(pin, GPIO.OUT)
        for pin in [MOSFET_1_PIN, MOSFET_2_PIN, MOSFET_3_PIN]:
            GPIO.setup(pin, GPIO.OUT)

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

    # Iniciar PWM en 0
    for pwm in (pwm_esc_1, pwm_esc_2, pwm_esc_3, pwm_esc_4, pwm_esc_5, pwm_esc_6):
        pwm.start(0)

def set_mosfet_state(state):
    """Controla los 3 MOSFETs (state: 'ON' o 'OFF')."""
    level = GPIO.HIGH if state == "ON" else GPIO.LOW
    for pin in [MOSFET_1_PIN, MOSFET_2_PIN, MOSFET_3_PIN]:
        GPIO.output(pin, level)

def _map_speed_to_pwm(value):
    """Mapea -100..100 a 0..100 para ChangeDutyCycle (ajustable según ESC)."""
    if value < -100: value = -100
    if value > 100: value = 100
    return (value + 100) / 2.0

def set_side_speeds(left, right):
    """Establece velocidad para lado izquierdo y derecho (-100..100)."""
    pwm_left = _map_speed_to_pwm(left)
    pwm_right = _map_speed_to_pwm(right)
    for pwm in [pwm_esc_1, pwm_esc_3, pwm_esc_5]:  # ruedas izquierdas
        pwm.ChangeDutyCycle(pwm_left)
    for pwm in [pwm_esc_2, pwm_esc_4, pwm_esc_6]:  # ruedas derechas
        pwm.ChangeDutyCycle(pwm_right)

def set_all_wheels_speed(value):
    """Ajusta todas las ruedas al mismo valor (-100..100)."""
    set_side_speeds(value, value)

def stop_all_wheels():
    set_all_wheels_speed(0)

def cleanup_gpio():
    """Detiene PWM y limpia GPIO."""
    for pwm in (pwm_esc_1, pwm_esc_2, pwm_esc_3, pwm_esc_4, pwm_esc_5, pwm_esc_6):
        try:
            pwm.stop()
        except Exception:
            pass
    try:
        GPIO.cleanup()
    except Exception:
        pass
# ...existing code...
