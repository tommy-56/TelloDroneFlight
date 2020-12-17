"""
Xbox 360 Controller Tello Drone Flight Python 3.7
Written by Tommy Anderson
Date 5/29/19
Python Program to fly tello drone with xbox 360 controller
Inspiration from github user Jabrils - TelloTv Project
Original Code to Fly with keyboard that I adjusted is from damiafuentes onn github
Controls can be found in README
"""
from djitellopy import Tello
import cv2
import pygame
from pygame.locals import *
import numpy as np
import time, re

# Speed Setting for Flight
S = 60

# Speed setting for Yaw movement
YAWSPEED = 50

# Frames of pygame
FPS = 25

JOYSTICKS = []
# Mapping for Controller
X360_AXIS_IDS = {
	'LEFT_X': 0,
	'LEFT_Y': 1,
	'LEFT_TRIGGER': 2,
	'RIGHT_X': 3,
	'RIGHT_Y': 4,
	'RIGHT_TRIGGER': 5,
	'D_PAD_X': 6,
	'D_PAD_Y': 7,
}
X360_BUTTON_IDS = {
	'A': 0,
	'B': 1,
	'X': 2,
	'Y': 3,
	'L_BUMPER': 4,
	'R_BUMPER': 5,
	'BACK': 6,
	'START': 7,
	'GUIDE': 8,
	'L_STICK': 9,
	'R_STICK': 10,
}
X360_AXIS_NAMES = dict([(idn, name) for name, idn in X360_AXIS_IDS.items()])
X360_BUTTON_NAMES = dict([(idn, name) for name, idn in X360_BUTTON_IDS.items()])

AXIS_NAMES = X360_AXIS_NAMES
AXIS_IDS = X360_AXIS_IDS
BUTTON_NAMES = X360_BUTTON_NAMES
BUTTON_IDS = X360_BUTTON_IDS
HAT_NAMES = {}
HAT_IDS = {}


class Drone(object):

	def __init__(self):
		# Initialze Pygame
		pygame.init()

		# Create pygame window
		pygame.display.set_caption("Tello-Game video stream")
		self.screen = pygame.display.set_mode([960, 720])

		# Create tello object to interact with called tello
		self.tello = Tello()

		# Master Movement Velocities
		self.ForwardsBackwards = 0
		self.movRightLeft = 0
		self.UpDown = 0
		self.rotateYaw = 0

		self.send_rc_control = True

		# create update timer
		pygame.time.set_timer(USEREVENT + 1, 50)

	def get_altitude(self):
		try:
			alt = self.tello.get_height()  # Gives Long String
			alt = re.findall(r'\d+', alt)  # Parse just altitude number from string
			alt = alt[0]
			alt = (int(alt) / 3.048)  # Conversion from Decimeters to Feet
			return (format(alt, '0.2f') + ' FT')
		except IndexError:
			print('***Altitude Read Error***')  # console log error message
			return 'Error'  # Message for display

	def check_battery(self):
		try:
			battery = self.tello.get_battery()  # Gives Long String
			battery = re.findall(r'\d+', battery)  # Parse just the battery number from string
			battery = battery[0]
			battery = int(battery)
			if battery > 10:
				return (str(battery) + ' % Bat')
			elif battery == 15:
				return 'LOW BATTERY WARNING 15%'
			elif battery == 10:
				return 'LOW BATTERY LAND NOW'
			elif battery < 10:  # Fail Safe
				time.sleep(5)
				self.tello.land()
				return 'LOW BATTERY EMERGENCY LANDING'
		except TypeError:
			print('******Battery Read Error******')  # Console log error message
			return 'Error'  # Error message for display
		except IndexError:
			return 'Error'

	def run(self):
		# Check For Controller and get Name
		for i in range(0, pygame.joystick.get_count()):
			try:
				JOYSTICKS.append(pygame.joystick.Joystick(i))
				JOYSTICKS[-1].init()
				print("Detected joystick '%s'" % JOYSTICKS[-1].get_name())
			except:
				print("Controller Not Found")
				break

		if not self.tello.connect():
			print("Tello not connected")
			return

		# Turns off video stream in case of crash
		if not self.tello.streamoff():
			print("Could not stop video stream")
			return

		if not self.tello.streamon():
			print("Could not start video stream")
			return
		frame_read = self.tello.get_frame_read()

		should_stop = False
		while not should_stop:
			font = pygame.font.SysFont('comicsansms', 20)
			battery = self.check_battery()
			altitude = self.get_altitude()  # Check battery and Altitude every event
			for event in pygame.event.get(): # checks the event type and calls the corresponding method
				if event.type == USEREVENT + 1:
					self.update()
				elif event.type == QUIT:
					should_stop = True
				elif self.movRightLeft or self.ForwardsBackwards > 0:
					self.movRightLeft = 0
					self.ForwardsBackwards = 0
				elif event.type == JOYAXISMOTION:
					self.StickMov(event.value, AXIS_NAMES[event.axis])
				elif event.type == JOYBUTTONDOWN:
					button = BUTTON_NAMES[event.button]
					self.ButtonPushed(button)
				elif event.type == JOYBUTTONUP:
					button = BUTTON_NAMES[event.button]
					if button != 'B' or 'Y':
						self.ButtonReleased(button)

			if frame_read.stopped:
				frame_read.stop()
				break

			self.screen.fill([0, 0, 0])
			frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
			frame = np.rot90(frame)
			frame = np.flipud(frame)
			frame = pygame.surfarray.make_surface(frame)
			self.screen.blit(frame, (0, 0))
			batteryDisp = font.render(battery, True, (255, 0, 0))  # Add the battery display to the screen
			self.screen.blit(batteryDisp, (50, 10))
			altDisp = font.render(altitude, True, (255, 0, 0))  # Add Altitude display to screen
			self.screen.blit(altDisp, (50, 40))
			pygame.display.update()

			time.sleep(1 / FPS)

		
		self.tello.end()

	def ButtonPushed(self, button): # tracks which buttons on the controller are pressed
		if button == 'A':
			self.UpDown = S
		elif button == 'X':
			self.UpDown = -S
		elif button == "B":
			self.tello.land()
		elif button == "Y":
			self.tello.takeoff()
		elif button == 'L_BUMPER':
			self.rotateYaw = -YAWSPEED
		elif button == 'R_BUMPER':
			self.rotateYaw = YAWSPEED

	def ButtonReleased(self, button):
		# Stop moving
		if button == 'A':
			self.UpDown = 0
		elif button == 'X':
			self.UpDown = 0
		elif button == 'L_BUMPER' or 'R_BUMPER':
			self.rotateYaw = 0

	def StickMov(self, movement, axis): # Tracks joystick movement
		if axis == 'LEFT_Y':
			if movement < 0.25: # controller inputs start at 0 and are sensitive helps prevent minor touches affecting flight
				self.ForwardsBackwards = int(S * movement) # Governs the speed based on the input from the controller.
				print('Move Back')  # Made into int since dji tello package only accepts ints to its velocity function
			elif movement > 0 and movement > -0.25:
				self.ForwardsBackwards = int(S * movement)
				print('Move Forwards')
		elif axis == 'RIGHT_Y':
			if movement > 0.25:
				self.movRightLeft = int(S * movement)
				print('Move Right')
			elif movement < 0 and movement < -0.25:
				self.movRightLeft = int(S * movement)
				print('Move Left')

	def update(self): # send the controls to the drone
		if self.send_rc_control:
			self.tello.send_rc_control(self.movRightLeft, self.ForwardsBackwards, self.UpDown, self.rotateYaw)


def main():
	drone = Drone()
	drone.run()  # Start program


if __name__ == '__main__':
	main()
