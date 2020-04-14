# name=DJTT Midi Fighter Twister
# url=

import fl
import patterns
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist
import math

#import midi
#import utils

class TMidiFighterTwister:

	def OnInit(self):
		print("On Init")
		self.knobs = self.Knobs()
		self.buttons = self.Buttons()
		self.colors = self.Colors()
		self.animation = self.Animation()
		self.MidiMsgTypeCC = 11
		self.OnRefresh(0)

	def OnDeInit(self):
		print("On De Init")

	def UpdateKnobs(self, Index, Value):

		print("Update Knobs")
		if (64 < Value < 65): Value = 65
		if (64 > Value > 63): Value = 63
		Value = int(Value)
		print("Knob Output: i=", Index, ", val=", Value)
		device.midiOutMsg(0 + (self.MidiMsgTypeCC << 4) + (Index << 8) + (Value << 16))

	def UpdateLEDs(self, Index, Color, Animation):

		print("Update LEDs")
		print("LED Output: i=", Index," color=", Color," animation=", Animation)
		device.midiOutMsg(1 + (self.MidiMsgTypeCC << 4) + (Index << 8) + (Color << 16))
		device.midiOutMsg(5 + (self.MidiMsgTypeCC << 4) + (Index << 8) + (Animation << 16))

	def OnMidiIn(self, event):

		print("On Midi In")
		print("Midi CC: ", event.controlNum)
		print("Midi CC Value: ", event.controlVal)

		if event.controlNum == self.knobs.volume:
			scaledVolume = self.scaleValue(event.controlVal, 127, 1)
			mixer.setTrackVolume(mixer.trackNumber(), scaledVolume)

		if event.controlNum == self.knobs.pan:
			scaledPan = (self.scaleValue(event.controlVal, 127, 2) - 1)
			if (abs(scaledPan) < 0.008): scaledPan = 0
			mixer.setTrackPan(mixer.trackNumber(), scaledPan)

		if (event.controlNum == self.buttons.play) & (event.controlVal == 127):
			transport.start()

		if (event.controlNum == self.buttons.stop) & (event.controlVal == 127):
			transport.stop()

		if (event.controlNum == self.buttons.record) & (event.controlVal == 127):
			transport.record()

		#event.handled = true

	def OnMidiMsg(self, event):

		print("On Midi Msg")

		event.handled = False

	def OnMidiOutMsg(self, event):

		print("On Midi Out Msg")

		event.handled = False

	def OnRefresh(self, flags):

		if device.isAssigned():
			print("On Refresh")

			i = mixer.trackNumber()

			volume = mixer.getTrackVolume(i)
			scaledVolume = self.scaleValue(volume, 1, 127)
			self.UpdateKnobs(self.knobs.volume, scaledVolume)

			pan = 1 + (mixer.getTrackPan(i))
			scaledPan = self.scaleValue(pan, 2, 127)
			self.UpdateKnobs(self.knobs.pan, scaledPan)

			color = mixer.getTrackColor(i)

			if transport.isPlaying():
				self.UpdateLEDs(self.buttons.play, self.colors.green, self.animation.solid)
				self.UpdateLEDs(self.buttons.stop, self.colors.green, self.animation.solid)
			else:
				self.UpdateLEDs(self.buttons.play, self.colors.darkBlue, self.animation.solid)
				self.UpdateLEDs(self.buttons.stop, self.colors.darkBlue, self.animation.solid)

			if transport.isRecording():
				self.UpdateLEDs(self.buttons.record, self.colors.red, self.animation.solid)
			else:
				self.UpdateLEDs(self.buttons.record, self.colors.yellow, self.animation.solid)

			if transport.getLoopMode():
				self.UpdateLEDs(self.buttons.loopMode, self.colors.greenYellow, self.animation.solid)
			else:
				self.UpdateLEDs(self.buttons.loopMode, self.colors.lightOrange, self.animation.solid)


	def OnDoFullRefresh(self):

		print("On Do Full Refresh")

	def scaleValue(self, value, scaleIn, scaleOut):
		print("scaleValue")
		return ((value/scaleIn) * scaleOut)

	class Knobs:
		 volume = 15
		 pan = 11

	class Colors:
		darkBlue = 1
		lightBlue = 20
		cyan = 30
		green = 50
		greenYellow = 60
		yellow = 65
		lightOrange = 68
		orange = 72
		red = 80
		pink = 110
		purple = 127

	class Buttons:
		loopMode = 8
		play = 12
		stop = 13
		record = 14

	class Animation:
		solid = 0
		pulse = 14


MidiFighterTwister = TMidiFighterTwister()

def OnInit():
	MidiFighterTwister.OnInit()

def OnDeInit():
	MidiFighterTwister.OnDeInit()

def OnMidiIn(event):
	MidiFighterTwister.OnMidiIn(event)

def OnMidiMsg(event):
	MidiFighterTwister.OnMidiMsg(event)

def OnMidiOutMsg(event):
	MidiFighterTwister.OnMidiOutMsg(event)

def OnRefresh(Flags):
	MidiFighterTwister.OnRefresh(Flags)

def OnDoFullRefresh():
	MidiFighterTwister.OnDoFullRefresh()
