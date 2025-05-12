# The upper resistor is 330 and the lower is 470 but i just used 2 220s Circit https://www.dropbox.com/scl/fi/r4cwejtbq8dqblupzv6wv/wiring-uds.png?rlkey=nab4q01nk7q2mgoh6qp4bqal5&st=icq7u8c1&dl=0
from gpiozero import DistanceSensor
ultrasonic = DistanceSensor(echo=12, trigger=7, threshold_distance=0.1, max_distance=12)

while True:
	print(ultrasonic.distance)
