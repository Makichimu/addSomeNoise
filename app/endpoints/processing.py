from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
from app.utils.logger import logger
from app.utils.audio_processing import AudioProcessor
import json
import os

media_path = os.path.join(os.path.dirname(__file__), '..', 'media')

router = APIRouter()

@router.post("/process")
def process_audio(file: UploadFile = Form(...), effects: str = Form(...)):
    try:
        effects_list = json.loads(effects)
        # Save the uploaded file
        file_location = f"{media_path}/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(file.file.read())
            logger.info(f"File saved to {file_location}")

        # Process the audio file with the specified effects
        processor = AudioProcessor(file_location)
        processor.process_audio(effects_list)
        logger.info("Audio processed")
        processed_file_location = processor.save_audio()
        logger.info(f"Processed file saved to {processed_file_location}")
        
        # Return the processed file location as a URL
        processed_file_url = f"/media/{os.path.basename(processed_file_location)}"
        return JSONResponse(content={"audio_url": processed_file_url})

    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)