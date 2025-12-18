from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

import database

app = FastAPI(lifespan=database.lifespan)

# upload file into mongodb
@app.post('/upload/')
def upload_pdf(
    file: UploadFile = File(...) # open for file upload
):
    # get file id
    file_id = database.fs.put(file.file, filename=file.filename)
    return {
        'file_id': str(file_id),
    }