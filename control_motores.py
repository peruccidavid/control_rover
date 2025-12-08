import sys
sys.path.append('.')

# Intentar usar RPi.GPIO; si falla use mock_rpi_gpio (para ejecutar en laptop)
try:
    import RPi.GPIO as GPIO
except Exception:
    import mock_rpi_gpio as GPIO

import time

# Pines (BCM)
ESC_1_PIN = 18 #RUEDA IZQUIERDA
ESC_2_PIN = 23 #RUEDA DERECHA
ESC_3_PIN = 24 #RUEDA IZQUIERDA
ESC_4_PIN = 25 #RUEDA DERECHA
ESC_5_PIN = 19 #RUEDA IZQUIERDA
ESC_6_PIN = 26 #RUEDA DERECHA

MOSFET_1_PIN = 17
MOSFET_2_PIN = 27
MOSFET_3_PIN = 22

PWM_FREQ = 50

# Variables que se inicializan en init_gpio()
GPIO_INITIALIZED = False
pwm_esc_1 = pwm_esc_2 = pwm_esc_3 = pwm_esc_4 = pwm_esc_5 = pwm_esc_6 = None

def _use_mock():
    import mock_rpi_gpio as GPIO_mock
    try:
        GPIO_mock.setmode(GPIO_mock.BCM)
    except Exception:
        pass
    return GPIO_mock

def init_gpio():
    """Inicializa GPIO y PWM. Llamar antes de usar las funciones de control."""
    global GPIO, pwm_esc_1, pwm_esc_2, pwm_esc_3, pwm_esc_4, pwm_esc_5, pwm_esc_6, GPIO_INITIALIZED

    if GPIO_INITIALIZED:
        return

    def _setup_pins(g):
        g.setmode(g.BCM)
        g.setwarnings(False)
        for pin in (ESC_1_PIN, ESC_2_PIN, ESC_3_PIN, ESC_4_PIN, ESC_5_PIN, ESC_6_PIN):
            g.setup(pin, g.OUT)
        for pin in (MOSFET_1_PIN, MOSFET_2_PIN, MOSFET_3_PIN):
            g.setup(pin, g.OUT)

    try:
        _setup_pins(GPIO)
    except Exception:
        GPIO = _use_mock()
        _setup_pins(GPIO)

    # Crear PWM (fallback a Dummy si el módulo mock no implementa PWM)
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

    for pwm in (pwm_esc_1, pwm_esc_2, pwm_esc_3, pwm_esc_4, pwm_esc_5, pwm_esc_6):
        try:
            pwm.start(0)
        except Exception:
            pass

    GPIO_INITIALIZED = True

def set_mosfet_state(state):
    """Controla el estado de los 3 MOSFETs (ON/OFF)."""
    if not GPIO_INITIALIZED:
        init_gpio()
    level = GPIO.HIGH if state == "ON" else GPIO.LOW
    for pin in (MOSFET_1_PIN, MOSFET_2_PIN, MOSFET_3_PIN):
        GPIO.output(pin, level)

def _map_speed_to_pwm(value):
    """Mapea -100..100 a 0..100 para ChangeDutyCycle (ajustar si necesario)."""
    if value < -100: value = -100
    if value > 100: value = 100
    return (value + 100) / 2.0

def set_side_speeds(left, right):
    """Establece velocidad para lado izquierdo y derecho (-100..100)."""
    if not GPIO_INITIALIZED:
        init_gpio()
    pwm_left = _map_speed_to_pwm(left)
    pwm_right = _map_speed_to_pwm(right)
    for pwm in (pwm_esc_1, pwm_esc_3, pwm_esc_5):  # ruedas izquierdas
        try:
            pwm.ChangeDutyCycle(pwm_left)
        except Exception:
            pass
    for pwm in (pwm_esc_2, pwm_esc_4, pwm_esc_6):  # ruedas derechas
        try:
            pwm.ChangeDutyCycle(pwm_right)
        except Exception:
            pass

def set_all_wheels_speed(value):
    """Ajusta todas las ruedas al mismo valor (-100..100)."""
    set_side_speeds(value, value)

def stop_all_wheels():
    set_all_wheels_speed(0)

def cleanup_gpio():
    """Detiene PWM y limpia GPIO; seguro si no inicializado."""
    global GPIO_INITIALIZED
    if not GPIO_INITIALIZED:
        return
    for pwm in (pwm_esc_1, pwm_esc_2, pwm_esc_3, pwm_esc_4, pwm_esc_5, pwm_esc_6):
        try:
            pwm.stop()
        except Exception:
            pass
    try:
        GPIO.cleanup()
    except Exception:
        pass
    GPIO_INITIALIZED = False

# Bucle de prueba (solo si se ejecuta directamente)
def main():
    init_gpio()
    try:
        print("Prueba: adelante 50%")
        set_mosfet_state("ON")
        time.sleep(1)
        set_all_wheels_speed(50)
        time.sleep(3)
        print("Detener")
        stop_all_wheels()
        time.sleep(1)
        print("Atrás 50%")
        set_all_wheels_speed(-50)
        time.sleep(3)
        stop_all_wheels()
        set_mosfet_state("OFF")
    except KeyboardInterrupt:
        pass
    finally:
        cleanup_gpio()

if __name__ == "__main__":
    main()