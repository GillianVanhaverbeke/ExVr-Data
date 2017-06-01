import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

rows = [5, 6, 12]
collumns = [13, 16, 17]

class Zeeslag:
	def __init__(self):
		for row in rows:
			GPIO.setup(row, GPIO.OUT)
			GPIO.output(row, False)

		for collumn in collumns:
			GPIO.setup(collumn, GPIO.OUT)
			GPIO.output(collumn, True)

	def changeCollumnOn(self, selectedRow):
		GPIO.output(rows[selectedRow], True)

	def changeCollumnOff(self, selectedRow):
		GPIO.output(rows[selectedRow], False)

	def changeRowOn(self, selectedRow):
		GPIO.output(collumns[selectedRow], False)

	def changeRowOff(self, selectedRow):
		GPIO.output(collumns[selectedRow], True)


try:
	x = Zeeslag()
	while True:
		y = int(input("geef gwn een waarde in 0-2"))
		x.changeRowOn(y)
		time.sleep(0.2)

		y2 = int(input("geef gwn een waarde in 0-2"))
		x.changeCollumnOn(y2)
		time.sleep(0.2)

		z = int(input("geef gwn een waarde in 0-2"))
		x.changeRowOff(z)
		time.sleep(0.2)

		z2 = int(input("geef gwn een waarde in 0-2"))
		x.changeCollumnOff(z2)
		time.sleep(0.2)

except KeyboardInterrupt:
	GPIO.cleanup()
