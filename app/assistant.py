import logging
import time
import json
import sys
import os
import argparse
import traceback
from configparser import ConfigParser

from audio_processor import AudioProcessor
from stt import SpeechToText
from response_generator import ResponseGenerator
from tts import TextToSpeech

class Assistant:
	def __init__(self, config: ConfigParser):
		self.debug = config['default'].getboolean('debug')
		self.audio_processor = AudioProcessor()
		self.stt = SpeechToText(engine=config['speech-to-text']['engine'], model_name=config['speech-to-text'].get('model', None))
		self.response_generator = ResponseGenerator(model=config['response-generation']['model'])
		self.tts = TextToSpeech(model=config['text-to-speech']['model'])
		self.load_chat_history(config['response-generation']['personality'], config['default'].get('chat_history_file', None))

	def load_chat_history(self, personality, chat_history_file):
		self.chat_history = [{ "role": "system", "content": personality }]
		self.chat_history_file = chat_history_file
		
		if self.chat_history_file:
			if os.path.isfile(chat_history_file):
				with open(chat_history_file, 'r') as file:
					self.chat_history = json.load(file)
					logging.info(f"Loaded chat history from {chat_history_file}")
	
	def store_chat_history(self):
		if self.chat_history_file:
			directory = os.path.dirname(self.chat_history_file)
			if directory:
				os.makedirs(directory, exist_ok=True)

			with open(self.chat_history_file, 'w') as file:
				json.dump(self.chat_history, file, indent=4)
			logging.debug(f"Chat history saved to {self.chat_history_file}")

	def start(self):
		logging.info("Starting Elsie Voice Assistant")

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
				user_text = self.stt.transcribe_audio(wave_data=recorded_audio)
				if not user_text:
					logging.warning("Transcription not successful, starting to record again")
					continue
				logging.info("User said: " + user_text)

				# generate a response
				self.chat_history.append({"role": "user", "content": user_text})
				response_text = self.response_generator.generate_response(self.chat_history)
				logging.info("Assistant replied: " + response_text)
				self.chat_history.append({"role": "assistant", "content": response_text})
				self.store_chat_history()

				# generate audio from the response text
				self.tts.convert_to_wave(response_text, 'temp/response.wav')

				# play the audio response
				self.audio_processor.play_audio('temp/response.wav')
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
	parser.add_argument('-c', '--config', help='Path to config file (default: settings.ini)', default='settings.ini', type=str)
	args = parser.parse_args()

	if not os.path.isfile(args.config):
		logging.error(f"Config file '{args.config}' does not exist.")
		sys.exit(1)

	config = ConfigParser()
	config.read(args.config)

	log_level = logging.DEBUG if config['default'].getboolean('debug') else logging.INFO
	logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

	os.makedirs('temp', exist_ok=True)

	assistant = Assistant(config)
	assistant.start()
