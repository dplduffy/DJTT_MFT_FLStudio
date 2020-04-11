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

import midi
import utils

class TMidiFighterTwister():
	def OnInit(self):

		print("On Init")
		self.Reset()

	def OnDeInit(self):

		self.Reset()

	def UpdateKnobs(self, Index, Value):

		print("Update Knobs")
		print("Knob Output: i=", Index, ", val=", Value)
		#device.midiOutMsg()

	def UpdateLEDs(self, Index):

		print("Update Knobs")

	def OnMidiIn(self, event):

		print("On Midi In")
		print("Midi CC: ", event.controlNum)
		print("Midi CC Value: ", event.controlVal)

		if event.controlNum == 15:
			i = mixer.trackNumber()
			scaledValue = self.scaleValue(event.controlVal, 127, 1)
			mixer.setTrackVolume(i, scaledValue)
			print("Scaled Volume Out ", scaledValue)
		#event.handled = true

	def Reset(self):

		print("Reset")

	def OnMidiMsg(self, event):

		print("On Midi Msg")

		event.handled = False

	def OnMidiOutMsg(self, event):

		print("On Midi Out Msg")

		event.handled = False

	def OnRefresh(self, flags):
		if device.isAssigned():
			print("On Refresh")
			print("Flags: ", flags)

			if flags == 4:
				i = mixer.trackNumber()
				volume = mixer.getTrackVolume(i)
				scaledValue = self.scaleValue(volume, 1, 127)
				self.UpdateKnobs(15, scaledValue)
			else:
				print("false")

	def OnDoFullRefresh(self):

		print("On Do Full Refresh")

	def scaleValue(self, value, scaleIn, scaleOut):
		print("scaleValue")
		return ((value/scaleIn) * scaleOut)

	#def OnDirtyMixerTrack(self, Flags):

	#	print("On Dirty Mixer Track")
	#	print(Flags)

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

#def OnDirtyMixerTrack(Flags):
#	MidiFighterTwister.OnDirtyMixerTrack(Flags)
