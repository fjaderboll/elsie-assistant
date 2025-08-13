import wave
from pathlib import Path
from piper import PiperVoice, download_voices

class TextToSpeech:
	def __init__(self, model='en_US-lessac-medium'):
		download_voices.download_voice(model, Path('models'))
		self.voice = PiperVoice.load(f'models/{model}.onnx')

	def convert_to_wave(self, text, output_path):
		with wave.open(output_path, "wb") as wave_file:
			self.voice.synthesize_wav(text, wave_file)
