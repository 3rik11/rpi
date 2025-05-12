# The upper resistor is 330 and the lower is 470 but i just used 2 220s Circit https://www.dropbox.com/scl/fi/r4cwejtbq8dqblupzv6wv/wiring-uds.png?rlkey=nab4q01nk7q2mgoh6qp4bqal5&st=icq7u8c1&dl=0
from gpiozero import DistanceSensor, LED

led = LED(18)
ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.05, max_distance=5)

while True:
	ultrasonic.wait_for_in_range()
	print("STOP MOVING")
	led.on()
	ultrasonic.wait_for_out_of_range()
	print("MOVE")
	led.off()
