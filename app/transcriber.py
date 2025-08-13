import os
import vosk
import json
import wave
import logging

class Transcriber:
	def __init__(self, lang='en-us', model_name=None):
		if model_name is not None:
			model = vosk.Model(f'models/{model_name}')
		else:
			model = vosk.Model(lang=lang)
		self.recognizer = vosk.KaldiRecognizer(model, 16000)

	def transcribe_audio(self, wave_data=None, wave_file_path=None):
		if wave_file_path is not None:
			wf = wave.open(wave_file_path, 'rb')
			if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE" or wf.getframerate() != 16000:
				logging.error("Audio file must be WAV format mono PCM 16 kHz.")
				return None
			wave_data = wf.readframes(wf.getnframes())

		if wave_data is None or len(wave_data) == 0:
			logging.error("No valid audio data available for transcription.")
			return None
		
		self.recognizer.AcceptWaveform(wave_data)
		result = json.loads(self.recognizer.FinalResult())
		return result['text']

if __name__ == "__main__":
	transcriber = Transcriber()
	text = transcriber.transcribe_audio(wave_file_path='temp/user_recording.wav')
	print('Text 1:', text)

	text = transcriber.transcribe_audio(wave_file_path='temp/test.wav')
	print('Text 2:', text)
