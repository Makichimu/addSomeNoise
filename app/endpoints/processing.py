from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
from app.utils.logger import logger
from app.utils.audio_processing import AudioProcessor
import json
import os
import asyncio

media_path = os.path.join(os.path.dirname(__file__), '..', 'media')

router = APIRouter()

async def delete_file_after_delay(file_path: str, delay: int):
    await asyncio.sleep(delay)
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"File {file_path} deleted after delay")

@router.post("/process")
async def process_audio(file: UploadFile = Form(...), effects: str = Form(...)):
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
        
        # Schedule file deletion
        asyncio.create_task(delete_file_after_delay(processed_file_location, 900))
        
        # Return the processed file location as a URL
        processed_file_url = f"/media/{os.path.basename(processed_file_location)}"
        return JSONResponse(content={"audio_url": processed_file_url})

    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)