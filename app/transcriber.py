import vosk
import json
import wave
import logging

class Transcriber:
	def __init__(self, lang='en-us', model_path=None):
		if model_path is not None:
			model = vosk.Model(model_path)
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

	def store_transcription(self, text, file_path):
		if text is None:
			logging.error("No transcription to store.")
			return
		with open(file_path, 'a') as file:
			file.write(text)
			file.write('\n')
		logging.debug(f"Transcription saved to {file_path}")

if __name__ == "__main__":
	transcriber = Transcriber()
	text = transcriber.transcribe_audio(wave_file_path='temp/user_recording.wav')
	print('Text 1:', text)

	text = transcriber.transcribe_audio(wave_file_path='temp/test.wav')
	print('Text 2:', text)
