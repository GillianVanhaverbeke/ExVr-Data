from Zeeslag import BattleShip
import RPi.GPIO as GPIO
import spidev
import time
import os

x = BattleShip()

class Joystick():
	# Define sensor channels
	# (channels 3 to 7 unused)
	swt_channel = 0
	vrx_channel = 1
	vry_channel = 2

	shot = 5

	ActiveRow = 0
	ActiveCollumn = 2

	# Define delay between readings (s)
	delay = 0.2

	# Open SPI bus
	GPIO.setmode(GPIO.BCM)

	spi = spidev.SpiDev()
	spi.open(0, 0)

	# Function to read SPI data from MCP3008 chip
	# Channel must be an integer 0-7
	def ReadChannel(self, channel):
		adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
		data = ((adc[1] & 3) << 8) + adc[2]
		return data

	def ActivateSelected(self, row, col):
		for i in range(self.shot):
			x.changeRowOn(row)
			x.changeCollumnOn(col)
			print("test")
			time.sleep(self.delay)
			x.changeRowOff(row)
			x.changeCollumnOff(col)
			time.sleep(self.delay)

try:
	JoyS = Joystick()

	x.changeCollumnOn(JoyS.ActiveCollumn)
	x.changeRowOn(JoyS.ActiveRow)

	IsSelected = False

	while True:
		# Read the joystick position data
		vrx_pos = JoyS.ReadChannel(JoyS.vrx_channel)
		vry_pos = JoyS.ReadChannel(JoyS.vry_channel)

		if IsSelected == False:
			if vrx_pos < 50:
				x.changeRowOff(JoyS.ActiveRow)
				JoyS.ActiveRow -= 1

			if vrx_pos > 1000:
				x.changeRowOff(JoyS.ActiveRow)
				JoyS.ActiveRow += 1

			if JoyS.ActiveRow > 2:
				JoyS.ActiveRow = 0
			elif JoyS.ActiveRow < 0:
				JoyS.ActiveRow = 2
			else:
				x.changeRowOn(JoyS.ActiveRow)
			time.sleep(JoyS.delay)

			if vry_pos < 50:
				x.changeCollumnOff(JoyS.ActiveCollumn)
				JoyS.ActiveCollumn -= 1

			if vry_pos > 1000:
				x.changeCollumnOff(JoyS.ActiveCollumn)
				JoyS.ActiveCollumn += 1

			if JoyS.ActiveCollumn > 2:
				JoyS.ActiveCollumn = 0
			elif JoyS.ActiveCollumn < 0:
				JoyS.ActiveCollumn = 2
			else:
				x.changeCollumnOn(JoyS.ActiveCollumn)

			time.sleep(JoyS.delay)



		# Read switch state
		swt_val = JoyS.ReadChannel(JoyS.swt_channel)

		if swt_val < 50:
			IsSelected = True
			JoyS.ActivateSelected(JoyS.ActiveRow, JoyS.ActiveCollumn)
			IsSelected = False

		# Print out results
		print("--------------------------------------------")
		print("X : {}  Y : {}  Switch : {}".format(vrx_pos, vry_pos, swt_val))

		# Wait before repeating loop
except KeyboardInterrupt:
	GPIO.cleanup()
