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

@app.get('/files/')
def list_files():
    files = []

    for grid_out in database.fs.find():
        files.append(
            {
                'filename': grid_out.filename,
                'file_id': str(grid_out._id),
                'size_kb': round(grid_out.length / 1024, 2),
                'upload_date': grid_out.uploadDate
            }
        )
    return {'count': len(files), 'files': files}