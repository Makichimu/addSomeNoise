import requests
import os
import json
import pytest
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

media_path = os.path.join(os.path.dirname(__file__), 'audios')

@pytest.mark.parametrize("effects", [["radio", "crowd", "dropout"]])
def test_process_audio(effects):
    logger.info("Starting test_process_audio with effects: %s", effects)
    with open(f"{media_path}/test_audio.mp3", 'rb') as file:
        response = requests.post(
            'http://0.0.0.0:8000/api/audio/process',
            files={'file': ('test_audio.mp3', file, 'audio/mpeg')},
            data={'effects': json.dumps(effects)}
        )
    logger.info("Received response with status code: %d", response.status_code)
    assert response.status_code == 200
    response_data = response.json()
    logger.info("Response data: %s", response_data)
    assert "test_audio_processed" in response_data["audio_url"]
    logger.info("Test completed successfully")