# Este módulo simula el comportamiento de la librería RPi.GPIO
# para permitir que el código se ejecute en sistemas que no son Raspberry Pi.

BCM = 11
OUT = 1
HIGH = 1
LOW = 0
PWM = object()

def setmode(mode):
    print("GPIO: Modo de numeración configurado.")

def setup(pins, mode):
    if isinstance(pins, int):
        pins = [pins]
    print(f"GPIO: Pines {pins} configurados como salida.")

def output(pins, value):
    if isinstance(pins, int):
        pins = [pins]
    state = "HIGH" if value == HIGH else "LOW"
    print(f"GPIO: Pines {pins} ajustados a {state}.")

def cleanup():
    print("GPIO: Configuración limpia.")

def PWM(pin, frequency):
    print(f"GPIO: PWM iniciado en el Pin {pin} con frecuencia {frequency} Hz.")
    return _PWM_Mock()

class _PWM_Mock:
    def start(self, duty_cycle):
        print(f"PWM: Iniciar con ciclo de trabajo de {duty_cycle}%.")

    def ChangeDutyCycle(self, duty_cycle):
        print(f"PWM: Ciclo de trabajo cambiado a {duty_cycle}%.")

    def stop(self):
        print("PWM: Detenido.")