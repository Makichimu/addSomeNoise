from pydub import AudioSegment
from app.utils.audio_effects import AudioEffects
from app.utils.logger import logger
import os

class AudioProcessor:
    def __init__(self, original_audio):
        self.media_path = os.path.join(os.path.dirname(__file__), '..', 'media')
        self.original_audio_path = os.path.join(self.media_path, original_audio)
        self.original_audio = AudioSegment.from_file(self.original_audio_path)
        self.audio_effects = AudioEffects()
        self.processed_audio = None

    def process_audio(self, effects: list):
        audio_data = self.original_audio
        for effect in effects:
            if effect == 'radio':
                audio_data = self.audio_effects.radio_effect(audio_data)
            elif effect == 'crowd':
                audio_data = self.audio_effects.crowd_effect(audio_data)
            elif effect == 'dropout':
                audio_data = self.audio_effects.drop_out_effect(audio_data)
            elif effect == 'echo':
                audio_data = self.audio_effects.echo_effect(audio_data)
        logger.info('Audio processed')
        self.processed_audio = audio_data

    def save_audio(self):
        original_filename = os.path.splitext(os.path.basename(self.original_audio_path))[0]
        processed_audio_filename = f'{original_filename}_processed.mp3'
        processed_audio_path = os.path.join(self.media_path, processed_audio_filename)
        self.processed_audio.export(processed_audio_path, format='mp3')
        logger.info('Audio saved')
        return processed_audio_path