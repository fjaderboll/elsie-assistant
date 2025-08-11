import logging
import time
import sys
import argparse

from audio_processor import AudioProcessor
from transcriber import Transcriber

class Assistant:
	def __init__(self, debug=False, vosk_model_path=None):
		self.audio_processor = AudioProcessor()
		self.transcriber = Transcriber(model_path=vosk_model_path)
		self.debug = debug
	
	def start(self):
		logging.info("Starting Elsie Voice Assistant")

		chat_history = [
			{
				"role": "system",
				"content": """You are a helpful Assistant called Elsie. 
			You are friendly and fun and you will help the users with their requests.
			Your answers are short and concise."""
			}
		]
		
		while True:
			try:
				# record audio from the microphone
				recorded_audio = self.audio_processor.record_audio()
				if self.debug:
					self.audio_processor.store_audio(recorded_audio, 'temp/user_recording.wav')
			
				# transcribe the audio
				user_text = self.transcriber.transcribe_audio(wave_data=recorded_audio)
				if not user_text:
					logging.info("Transcription not successful. Starting recording again.")
					continue
				
				if self.debug:
					self.transcriber.store_transcription(user_text, 'temp/user_transcription.log')

				logging.info("You said: " + user_text)

				# append the user's input to the chat history
				chat_history.append({"role": "user", "content": user_text})

	#			# generate a response
	#			response_text = generate_response(chat_history)
	#			logging.info("Response: " + response_text)
	#
	#			# append the assistant's response to the chat history
	#			chat_history.append({"role": "assistant", "content": response_text})
	#
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
				time.sleep(10)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--debug', help='Enable debug mode', action='store_true')
	parser.add_argument('--vosk-model', help='Path to alternative Vosk model (by default a slim English model will be used)', default=None, type=str)
	args = parser.parse_args()

	log_level = logging.DEBUG if args.debug else logging.INFO
	logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

	assistant = Assistant(debug=args.debug, vosk_model_path=args.vosk_model)
	assistant.start()
