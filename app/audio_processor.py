import speech_recognition as sr
import pygame
import logging

class AudioProcessor:
    """
    Record audio from the microphone and save it as an MP3 file.
    
    Args:
    file_path (str): The path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    retries (int): Number of retries if recording fails.
    energy_threshold (int): Energy threshold for considering whether a given chunk of audio is speech or not.
    pause_threshold (float): How much silence the recognizer interprets as the end of a phrase (in seconds).
    phrase_threshold (float): Minimum length of a phrase to consider for recording (in seconds).
    dynamic_energy_threshold (bool): Whether to enable dynamic energy threshold adjustment.
    calibration_duration (float): Duration of the ambient noise calibration (in seconds).
    """
    def __init__(self, energy_threshold=2000, pause_threshold=1, phrase_threshold=0.1, dynamic_energy_threshold=True):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = pause_threshold
        self.recognizer.phrase_threshold = phrase_threshold
        self.recognizer.dynamic_energy_threshold = dynamic_energy_threshold

    def record_audio(self, timeout=10, retries=3, calibration_duration=1, phrase_time_limit=None):
        for attempt in range(retries):
            try:
                with sr.Microphone() as source:
                    logging.info("Calibrating for ambient noise...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
                    logging.info("Recording started")
                    # Listen for the first phrase and extract it into audio data
                    audio_data = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                    logging.info("Recording complete")

                    wave_data = audio_data.get_wav_data(convert_rate=16000)
                    return wave_data
            except sr.WaitTimeoutError:
                logging.warning(f"Listening timed out, retrying... ({attempt + 1}/{retries})")
            except Exception as e:
                logging.error(f"Failed to record audio: {e}")
                if attempt == retries -1:
                    raise
            
        logging.error("Recording failed after all retries")
        return None

    def store_audio(self, wave_data, file_path):
        with open(file_path, "wb") as audio_file:
            audio_file.write(wave_data)
        logging.debug(f"Audio saved to {file_path}")

    def play_audio(self, file_path):
        """
        Play an audio file using pygame.
        
        Args:
        file_path (str): The path to the audio file to play.
        """
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
        except pygame.error as e:
            logging.error(f"Failed to play audio: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred while playing audio: {e}")
        finally:
            pygame.mixer.quit()
