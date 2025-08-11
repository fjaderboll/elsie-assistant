import logging
import time
import json
import sys
import os
import argparse
import traceback

from audio_processor import AudioProcessor
from transcriber import Transcriber
from response_generator import ResponseGenerator
from tts import TextToSpeech

class Assistant:
	def __init__(self, config):
		self.personality = config['personality']
		self.debug = config['debug']
		self.audio_processor = AudioProcessor()
		self.transcriber = Transcriber(model_path=config['voskModelPath'])
		self.response_generator = ResponseGenerator(model=config['ollamaModel'])
		self.tts = TextToSpeech()

	def start(self):
		logging.info("Starting Elsie Voice Assistant")

		chat_history = [{ "role": "system", "content": self.personality }]

		while True:
			try:
				# record audio from the microphone
				recorded_audio = self.audio_processor.record_audio()
				if not recorded_audio:
					logging.info("No audio recorded, starting to record again")
					continue
				if self.debug:
					self.audio_processor.store_audio(recorded_audio, 'temp/user_recording.wav')
			
				# transcribe the audio
				user_text = self.transcriber.transcribe_audio(wave_data=recorded_audio)
				if not user_text:
					logging.warning("Transcription not successful, starting to record again")
					continue
				if self.debug:
					self.transcriber.store_transcription('User', user_text, 'temp/transcription.log')
				logging.info("User said: " + user_text)

				# generate a response
				chat_history.append({"role": "user", "content": user_text})
				response_text = self.response_generator.generate_response(chat_history)
				logging.info("Assistant replied: " + response_text)
				chat_history.append({"role": "assistant", "content": response_text})
				if self.debug:
					self.transcriber.store_transcription('Assistant', response_text, 'temp/transcription.log')

				# playback the response text
				self.tts.say(response_text)
			except KeyboardInterrupt:
				logging.info("Aborted by user")
				break
			except Exception as e:
				logging.error(f"An error occurred: {e}")
				if self.debug:
					print(traceback.format_exc())
				time.sleep(10)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--config', help='Path to config file (default: settings.json)', default='settings.json', type=str)
	args = parser.parse_args()

	if not os.path.isfile(args.config):
		logging.error(f"Config file '{args.config}' does not exist.")
		sys.exit(1)
	
	config = json.load(open(args.config, 'r'))

	log_level = logging.DEBUG if config['debug'] else logging.INFO
	logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

	assistant = Assistant(config)
	assistant.start()
