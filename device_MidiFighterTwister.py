# name=DJTT Midi Fighter Twister
# url=

import patterns
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist
import math
import midi
import utils

class TMidiFighterTwister:

	def OnInit(self):
		print("On Init")
		self.KNOB = self.KNOB()
		self.BTN = self.BTN()
		self.COLOR = self.COLOR()
		self.ANI = self.ANI()
		self.OnRefresh(0)

	def OnDeInit(self):
		print("On De Init")

	def UpdateKnobs(self, Index, Value):

		#print("Update KNOB")
		if (self.KNOB.PAN == Index):
			if (64 < Value < 65): Value = 65
			if (64 > Value > 63): Value = 63
		Value = int(Value)
		#print("Knob Output: i=", Index, ", val=", Value)
		device.midiOutMsg(0 + midi.MIDI_CONTROLCHANGE + (Index << 8) + (Value << 16))

	def UpdateLEDs(self, Index, Color, ANI):

		#print("Update LEDs")
		#print("LED Output: i=", Index," color=", Color," ANI=", ANI)
		device.midiOutMsg(1 + (midi.MIDI_CONTROLCHANGE) + (Index << 8) + (Color << 16))
		device.midiOutMsg(5 + (midi.MIDI_CONTROLCHANGE) + (Index << 8) + (ANI << 16))

	def OnMidiIn(self, event):

		print("On Midi In")

	def OnMidiMsg(self, event):

		print("On Midi Msg")
		#print("CC: ", event.controlNum, " Value: ", event.controlVal, " Chan: ", event.midiChan)

		i = mixer.trackNumber()

		if (event.midiChan == self.CHN.KNOB):

			event.handled = False

			if event.controlNum == self.KNOB.VOL:
				sVol = self.scaleValue(event.controlVal, 127, 1)
				mixer.setTrackVolume(mixer.trackNumber(), sVol)
				event.handled = True

			if event.controlNum == self.KNOB.PAN:
				sPan = (self.scaleValue(event.controlVal, 127, 2) - 1)
				if (abs(sPan) < 0.008):
					sPan = 0
				mixer.setTrackPan(mixer.trackNumber(), sPan)
				event.handled = True

		elif (event.midiChan == self.CHN.BTN):

			event.handled = False

			if (event.controlNum == self.BTN.PLAY) & (event.controlVal == 127):
				transport.start()
				event.handled = True

			if (event.controlNum == self.BTN.STOP) & (event.controlVal == 127):
				transport.stop()
				event.handled = True

			if (event.controlNum == self.BTN.RECORD) & (event.controlVal == 127):
				transport.record()
				event.handled = True

			if (event.controlNum == self.BTN.LOOP_MODE) & (event.controlVal == 127):
				transport.setLoopMode()
				event.handled = True

			if (event.controlNum == self.BTN.MUTE) & (event.controlVal == 127):
				mixer.enableTrack(i)
				event.handled = True

			if (event.controlNum == self.BTN.SOLO) & (event.controlVal == 127):
				mixer.soloTrack(i)
				event.handled = True

			if (event.controlNum == self.BTN.TRACK_ARM) & (event.controlVal == 127):
				mixer.armTrack(i)
				event.handled = True

		else:

			event.handled = False

	def OnControlChange(self, event):

		print("On Control Change")

		event.handled = False

	def OnMidiOutMsg(self, event):

		print("On Midi Out Msg")

		event.handled = False

	def OnRefresh(self, flags):

		if device.isAssigned():
			print("On Refresh")

			i = mixer.trackNumber()

			Volume = mixer.getTrackVolume(i)
			sVol = self.scaleValue(Volume, 1, 127)
			self.UpdateKnobs(self.KNOB.VOL, sVol)
			self.UpdateLEDs(self.KNOB.VOL, self.COLOR.BRIGHT_GREEN, self.ANI.SOLID)

			Pan = 1 + (mixer.getTrackPan(i))
			sPan = self.scaleValue(Pan, 2, 127)
			self.UpdateKnobs(self.KNOB.PAN, sPan)

			if mixer.isTrackSolo(i):
				self.UpdateLEDs(self.BTN.SOLO, self.COLOR.GREEN_YELLOW, self.ANI.PULSE)
			else:
				if (Pan < 1):
					self.UpdateLEDs(self.KNOB.PAN, self.COLOR.YELLOW, self.ANI.SOLID)
				elif (Pan > 1):
					self.UpdateLEDs(self.KNOB.PAN, self.COLOR.RED, self.ANI.SOLID)
				else:
					self.UpdateLEDs(self.KNOB.PAN, self.COLOR.BRIGHT_GREEN, self.ANI.SOLID)

			if mixer.isTrackEnabled(i):
				self.UpdateLEDs(self.BTN.MUTE, self.COLOR.BRIGHT_GREEN, self.ANI.SOLID)
			else:
				self.UpdateLEDs(self.BTN.MUTE, self.COLOR.GREEN_YELLOW, self.ANI.PULSE)

			if mixer.isTrackArmed(i):
				self.UpdateLEDs(self.KNOB.VOL, self.COLOR.RED, self.ANI.PULSE)

			color = mixer.getTrackColor(i)

			if transport.isPlaying():
				self.UpdateLEDs(self.BTN.PLAY, self.COLOR.GREEN, self.ANI.PULSE)
				self.UpdateLEDs(self.BTN.STOP, self.COLOR.GREEN, self.ANI.SOLID)
			else:
				self.UpdateLEDs(self.BTN.PLAY, self.COLOR.DARK_BLUE, self.ANI.SOLID)
				self.UpdateLEDs(self.BTN.STOP, self.COLOR.DARK_BLUE, self.ANI.SOLID)

			if transport.isRecording():
				self.UpdateLEDs(self.BTN.RECORD, self.COLOR.RED, self.ANI.PULSE)
			else:
				self.UpdateLEDs(self.BTN.RECORD, self.COLOR.YELLOW, self.ANI.SOLID)

			if transport.getLoopMode():
				self.UpdateLEDs(self.BTN.LOOP_MODE, self.COLOR.BRIGHT_GREEN, self.ANI.SOLID)
			else:
				self.UpdateLEDs(self.BTN.LOOP_MODE, self.COLOR.LIGHT_ORANGE, self.ANI.SOLID)


	def OnDoFullRefresh(self):

		print("On Do Full Refresh: ")

	def OnUpdateBeatIndicator(self, value):

		print("On Update Beat Indicator")

	def OnIdle(self):

		self.dirtyRefreshMacros()

	def scaleValue(self, value, scaleIn, scaleOut):
		return ((value/scaleIn) * scaleOut)

	def dirtyRefreshMacros(self):
		for controlId in range(8):
			eventID = device.findEventID(midi.EncodeRemoteControlID(device.getPortNumber(), 0, 0) + controlId, 1)
			sVal = self.scaleValue(device.getLinkedValue(eventID), 1, 127)
			#print("CID: ", controlId, "val: ", sVal)
			self.UpdateKnobs(controlId, sVal)

	class KNOB:
		 PAN = 11
		 VOL = 15

	class COLOR:
		DARK_BLUE = 1
		LIGHT_BLUE = 20
		CYAN = 30
		GREEN = 50
		BRIGHT_GREEN = 56
		GREEN_YELLOW = 59
		YELLOW = 65
		LIGHT_ORANGE = 68
		ORANGE = 72
		RED = 80
		PINK = 110
		PURPLE = 127

	class BTN:
		LOOP_MODE = 8
		MUTE = 10
		SOLO = 11
		PLAY = 12
		STOP = 13
		RECORD = 14
		TRACK_ARM = 15

	class ANI:
		SOLID = 0
		PULSE = 12

	class CHN:
		KNOB = 0
		BTN = 1


MidiFighterTwister = TMidiFighterTwister()

def OnInit():
	MidiFighterTwister.OnInit()

def OnDeInit():
	MidiFighterTwister.OnDeInit()

def OnMidiIn(event):
	MidiFighterTwister.OnMidiIn(event)

def OnMidiMsg(event):
	MidiFighterTwister.OnMidiMsg(event)

def OnControlChange(event):
	MidiFighterTwister.OnControlChange(event)

def OnIdle():
	MidiFighterTwister.OnIdle()

def OnMidiOutMsg(event):
	MidiFighterTwister.OnMidiOutMsg(event)

def OnRefresh(Flags):
	MidiFighterTwister.OnRefresh(Flags)

def OnDoFullRefresh(Flags):
	MidiFighterTwister.OnDoFullRefresh(Flags)

def OnUpdateBeatIndicator(value):
	MidiFighterTwister.OnUpdateBeatIndicator(value)
