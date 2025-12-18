from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from bson import ObjectId
from bson.errors import InvalidId

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

@app.delete('/delete/{file_id}')
def delete_file(file_id: str):
    try:
        oid = ObjectId(file_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail='Invalid file ID format')
    
    if not database.fs.exists(oid):
        raise HTTPException(status_code=404, detail='File not found')
    
    database.fs.delete(oid)

    return {
        'message': 'file delete successfully',
        'file_id': file_id
    }