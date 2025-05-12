from gpiozero import LED, Button
from time import sleep

button = Button(3)
red = LED(2)

while True:
	red.off()	
