from yapper import Yapper, PiperSpeaker, PiperVoiceUS

class TextToSpeech:
	def __init__(self):
		speaker = PiperSpeaker(voice=PiperVoiceUS.AMY)
		self.yapper = Yapper(speaker=speaker)

	def say(self, text):
		self.yapper.yap(text)
