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

#import midi
#import utils

class TMidiFighterTwister():
	def OnInit(self):

		print("On Init")
		self.Reset()

	def OnDeInit(self):

		self.Reset()

	def UpdateKnobs(self, Index):

		print("Update Knobs")

	def UpdateLEDs(self, Index):

		print("Update Knobs")

	def OnMidiIn(self, event):

		print("On Midi In")

		event.handled = False

	def Reset(self):

		print("Reset")

	def OnMidiMsg(self, event):

		print("On Midi Msg")

		event.handled = False

	def OnMidiOutMsg(self, event):

		print("On Midi Out Msg")

		event.handled = False

	def OnRefresh(self, flags):

		print("On Refresh")

		#print(flags)

	def OnDoFullRefresh(self, flags):

		print("On Do Full Refresh")

	def OnDirtyMixerTrack(self, flags):

		print("On Dirty Mixer Track")

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

def OnDoFullRefresh(Flags):
	MidiFighterTwister.OnRefresh(Flags)

def OnDirtyMixerTrack(Flags):
	MidiFighterTwister.OnDirtyMixerTrack(Flags)
