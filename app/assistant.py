import logging
import time
import sys
import argparse
import traceback

from audio_processor import AudioProcessor
from transcriber import Transcriber
from response_generator import ResponseGenerator

class Assistant:
	def __init__(self, debug=False, vosk_model_path=None, ollama_model='llama3'):
		self.debug = debug
		self.audio_processor = AudioProcessor()
		self.transcriber = Transcriber(model_path=vosk_model_path)
		self.response_generator = ResponseGenerator(model=ollama_model)

	def start(self):
		logging.info("Starting Elsie Voice Assistant")

		chat_history = [
			{
				"role": "system",
				"content": """
					You are a helpful robot called Elsie. 
					You are friendly and fun and you will try to be helpful.
					Your answers are short and concise like in a verbal conversation.
				"""
			}
		]
		
		while True:
			try:
				# record audio from the microphone
				recorded_audio = self.audio_processor.record_audio()
				if not recorded_audio:
					logging.info("No audio recorded, starting recording again")
					continue
				if self.debug:
					self.audio_processor.store_audio(recorded_audio, 'temp/user_recording.wav')
			
				# transcribe the audio
				user_text = self.transcriber.transcribe_audio(wave_data=recorded_audio)
				if not user_text:
					logging.warning("Transcription not successful, starting recording again")
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

	#			# convert the response text to speech
	#			response_audio = text_to_speech(response_text)
	#
	#			# play the generated speech audio
	#			self.audio_processor.play_audio(response_audio)
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
	parser.add_argument('-d', '--debug', help='Enable debug mode', action='store_true')
	parser.add_argument('--vosk-model', help='Path to alternative Vosk model (by default a slim English model will be used)', default=None, type=str)
	parser.add_argument('--ollama-model', help='Ollama model to use for response generation', default='llama3', type=str)
	args = parser.parse_args()

	log_level = logging.DEBUG if args.debug else logging.INFO
	logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

	assistant = Assistant(debug=args.debug, vosk_model_path=args.vosk_model, ollama_model=args.ollama_model)
	assistant.start()
