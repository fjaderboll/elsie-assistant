import vosk
import faster_whisper
import json
import wave
import logging
import io

class SpeechToText:
	def __init__(self, engine, model_name=None):
		self.engine = engine

		if engine == 'vosk':
			if model_name:
				model = vosk.Model(f'models/{model_name}')
			else:
				model = vosk.Model(lang='en-us')
			self.recognizer = vosk.KaldiRecognizer(model, 16000)
		elif engine == 'whisper':
			self.model = faster_whisper.WhisperModel(
				model_name,
				device="cpu",  # or "cuda" for GPU
				compute_type="int8",
				download_root="models",  # cache directory
				# condition_on_previous_text = False # Can reduce hallucinations if we don't use prompts
			)

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
		
		if self.engine == 'vosk':
			self.recognizer.AcceptWaveform(wave_data)
			result = json.loads(self.recognizer.FinalResult())
			return result['text']
		elif self.engine == 'whisper':
			segments, info = self.model.transcribe(io.BytesIO(wave_data))
			transcription = ' '.join([segment.text for segment in segments])
			logging.info(f"Detected language '{info.language}' with probability {info.language_probability}")
			return transcription

if __name__ == "__main__":
	transcriber = Transcriber(engine='vosk')
	text = transcriber.transcribe_audio(wave_file_path='temp/user_recording.wav')
	print('Text 1:', text)

	text = transcriber.transcribe_audio(wave_file_path='temp/test.wav')
	print('Text 2:', text)
