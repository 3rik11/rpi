#Link to curcit https://www.dropbox.com/scl/fi/w75ce0v2d89dn9xzf6848/camjam1wiring.png?rlkey=fdz8pnqtzse20e47yjtmlxsvo&st=lqrbwazh&dl=0
from gpiozero import Button, TrafficLights, Buzzer
from time import sleep

button = Button(21)
lights = TrafficLights(25, 8, 7)
buzzer = Buzzer(15)

while True:
      lights.off()
      lights.green.on()
      button.wait_for_press()
      sleep(5)
      lights.amber.on()
      sleep(1)
      lights.off()
      buzzer.beep(0.3, 0.3)
      lights.red.on()
      sleep(6.5)
      buzzer.off()
      lights.off()
