#Raspberry-py
#Esempio per gestire input e output (GPIO)
import RPi.GPIO
GPIO.setmode(GPIO,BCM)
GPIO.setup(7,GPIO.IN)
GPIO.setup(8,GPIO.OUT)
input_value=GPIO.input(7)
GPIO.output(8,True)

