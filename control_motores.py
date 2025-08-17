# Bloque de simulación - Comentar o eliminar cuando se ejecute en el Pi
# import sys
# sys.path.append('.')
# import mock_rpi_gpio
import RPi.GPIO as GPIO
import time

# Configuración de pines (usando el modo BCM)
# Asigna los pines GPIO según la configuración del manual de conexiones
# Ruedas Delanteras (Módulo 1)
ESC_1_PIN = 18  # Pin para la rueda 1 (ESC 1)
ESC_2_PIN = 23  # Pin para la rueda 2 (ESC 2)

# Ruedas Medias (Módulo 2)
ESC_3_PIN = 24  # Pin para la rueda 3 (ESC 3)
ESC_4_PIN = 25  # Pin para la rueda 4 (ESC 4)

# Ruedas Traseras (Módulo 3)
ESC_5_PIN = 19  # Pin para la rueda 5 (ESC 5)
ESC_6_PIN = 26  # Pin para la rueda 6 (ESC 6)

# Pines para el control de los MOSFETs
MOSFET_1_PIN = 17
MOSFET_2_PIN = 27
MOSFET_3_PIN = 22

# Inicializar pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup([ESC_1_PIN, ESC_2_PIN, ESC_3_PIN, ESC_4_PIN, ESC_5_PIN, ESC_6_PIN], GPIO.OUT)
GPIO.setup([MOSFET_1_PIN, MOSFET_2_PIN, MOSFET_3_PIN], GPIO.OUT)

# Configurar PWM para los ESCs
# Frecuencia de PWM recomendada para ESCs (ej. 50 Hz)
PWM_FREQ = 50 
pwm_esc_1 = GPIO.PWM(ESC_1_PIN, PWM_FREQ)
pwm_esc_2 = GPIO.PWM(ESC_2_PIN, PWM_FREQ)
pwm_esc_3 = GPIO.PWM(ESC_3_PIN, PWM_FREQ)
pwm_esc_4 = GPIO.PWM(ESC_4_PIN, PWM_FREQ)
pwm_esc_5 = GPIO.PWM(ESC_5_PIN, PWM_FREQ)
pwm_esc_6 = GPIO.PWM(ESC_6_PIN, PWM_FREQ)

# Iniciar PWM en ciclo de trabajo 0 (motor detenido)
pwm_esc_1.start(0)
pwm_esc_2.start(0)
pwm_esc_3.start(0)
pwm_esc_4.start(0)
pwm_esc_5.start(0)
pwm_esc_6.start(0)

# Funciones de control
def set_mosfet_state(state):
    """Controla el estado de los 3 MOSFETs (ON/OFF)."""
    if state == "ON":
        GPIO.output([MOSFET_1_PIN, MOSFET_2_PIN, MOSFET_3_PIN], GPIO.HIGH)
        print("MOSFETs activados.")
    else:
        GPIO.output([MOSFET_1_PIN, MOSFET_2_PIN, MOSFET_3_PIN], GPIO.LOW)
        print("MOSFETs desactivados.")

def set_all_wheels_speed(duty_cycle):
    """Ajusta la velocidad de todas las ruedas con el mismo ciclo de trabajo."""
    pwm_esc_1.ChangeDutyCycle(duty_cycle)
    pwm_esc_2.ChangeDutyCycle(duty_cycle)
    pwm_esc_3.ChangeDutyCycle(duty_cycle)
    pwm_esc_4.ChangeDutyCycle(duty_cycle)
    pwm_esc_5.ChangeDutyCycle(duty_cycle)
    pwm_esc_6.ChangeDutyCycle(duty_cycle)
    print(f"Velocidad de todas las ruedas ajustada a {duty_cycle}%")

def stop_all_wheels():
    """Detiene todos los motores."""
    set_all_wheels_speed(0)
    print("Todos los motores detenidos.")

def cleanup_gpio():
    """Limpia la configuración de los pines GPIO."""
    pwm_esc_1.stop()
    pwm_esc_2.stop()
    pwm_esc_3.stop()
    pwm_esc_4.stop()
    pwm_esc_5.stop()
    pwm_esc_6.stop()
    GPIO.cleanup()
    print("Configuración GPIO limpia.")

# Bucle principal de prueba
try:
    print("Modo de prueba de control de ruedas (simulación).")
    print("Activando MOSFETs y moviendo el Rover hacia adelante...")
    set_mosfet_state("ON")
    time.sleep(1) # Espera a que los ESCs se armen
    
    # Mover hacia adelante a 50% de velocidad
    set_all_wheels_speed(50)
    time.sleep(5) # Mover por 5 segundos
    
    # Detener y luego mover hacia atrás
    stop_all_wheels()
    time.sleep(2)
    
    print("Moviendo el Rover hacia atrás...")
    set_all_wheels_speed(-50) # Asumiendo un rango de -100 a 100
    time.sleep(5)
    
    # Detener y apagar MOSFETs
    stop_all_wheels()
    set_mosfet_state("OFF")

except KeyboardInterrupt:
    print("Prueba detenida por el usuario.")

finally:
    cleanup_gpio()