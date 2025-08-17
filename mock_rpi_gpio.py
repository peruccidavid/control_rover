import sys

# Este módulo simula el comportamiento de la librería RPi.GPIO
# para permitir que el código se ejecute en sistemas que no son Raspberry Pi.

class GPIO_Mock:
    BCM = 11
    OUT = 1
    HIGH = 1
    LOW = 0
    PUD_OFF = 0

    def setmode(self, mode):
        print("GPIO: Modo de numeración configurado.")

    def setup(self, pins, mode):
        if isinstance(pins, int):
            pins = [pins]
        print(f"GPIO: Pines {pins} configurados como salida.")

    def output(self, pins, value):
        if isinstance(pins, int):
            pins = [pins]
        state = "HIGH" if value == self.HIGH else "LOW"
        print(f"GPIO: Pines {pins} ajustados a {state}.")

    def cleanup(self):
        print("GPIO: Configuración limpia.")

    def PWM(self, pin, frequency):
        print(f"GPIO: PWM iniciado en el Pin {pin} con frecuencia {frequency} Hz.")
        return self.PWM_Mock()

    class PWM_Mock:
        def start(self, duty_cycle):
            print(f"PWM: Iniciar con ciclo de trabajo de {duty_cycle}%.")

        def ChangeDutyCycle(self, duty_cycle):
            print(f"PWM: Ciclo de trabajo cambiado a {duty_cycle}%.")

        def stop(self):
            print("PWM: Detenido.")

# Sobreescribir el módulo RPi.GPIO en el entorno de prueba
sys.modules['RPi.GPIO'] = GPIO_Mock()