from pydantic import BaseModel
from datetime import datetime, timezone

class files(BaseModel):
    file_name: str
    uploader_name:str
    uploaded_at: datetime = datetime.now(timezone.utc)