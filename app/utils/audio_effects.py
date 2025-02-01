from pydub import AudioSegment
import random
from app.utils.logger import logger
import ffmpeg
import io
import os

noises_path = os.path.join(os.path.dirname(__file__), '..', 'noises')

class AudioEffects:
    def __init__(self):
        self.white_noise = AudioSegment.from_file(os.path.join(noises_path, "white_noise.wav"))
        self.crowd_noise = AudioSegment.from_file(os.path.join(noises_path, "crowd_noise.wav"))

    def radio_effect(self, audio_data: AudioSegment) -> AudioSegment:
        audio_buffer = io.BytesIO()
        audio_data.export(audio_buffer, format="wav")
        audio_buffer.seek(0)
        
        out, _ = (
            ffmpeg
            .input('pipe:0', format='wav')
            .filter('volume', volume=-6)
            .filter('lowpass', f=5000)
            .filter('highpass', f=300)
            .output('pipe:1', format='wav')
            .run(input=audio_buffer.read(), capture_stdout=True, capture_stderr=True)
        )
        processed_audio = AudioSegment.from_file(io.BytesIO(out), format="wav").apply_gain(-10)
        
        self.white_noise = self.white_noise[:len(processed_audio)].apply_gain(-14)
        logger.info('Applying radio effect')
        return processed_audio.overlay(self.white_noise, loop=True)
        
    
    def crowd_effect(self, audio_data: AudioSegment) -> AudioSegment:
        self.crowd_noise = self.crowd_noise[:len(audio_data)].apply_gain(-4)
        logger.info('Applying crowd effect')
        return audio_data.overlay(self.crowd_noise, loop=True)
    
    def drop_out_effect(self, audio_data: AudioSegment) -> AudioSegment:
        logger.info('Applying dropout effect')
        dropout_length = 100
        num_dropouts = len(audio_data) // 2000  # Increase frequency of dropouts
        for _ in range(num_dropouts):
            start = random.randint(0, len(audio_data) - dropout_length)
            silence = AudioSegment.silent(duration=dropout_length)
            audio_data = audio_data[:start] + silence + audio_data[start + dropout_length:]
        return audio_data
    
    def echo_effect(self, audio_data: AudioSegment) -> AudioSegment:
        audio_buffer = io.BytesIO()
        audio_data.export(audio_buffer, format="wav")
        audio_buffer.seek(0)
        
        out, _ = (
            ffmpeg
            .input('pipe:0', format='wav')
            .filter('aecho', 0.8, 0.88, 60, 0.4)  # Добавление эффекта эха
            .output('pipe:1', format='wav')
            .run(input=audio_buffer.read(), capture_stdout=True, capture_stderr=True)
        )
        processed_audio = AudioSegment.from_file(io.BytesIO(out), format="wav")
        logger.info('Applying echo effect')
        return processed_audio