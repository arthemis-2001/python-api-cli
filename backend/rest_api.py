"""
A simple REST API using FastAPI framework with an in-memory database (a Python dict).

Routes included:
- POST: `/file/` -- upload a file to the dict
- GET: `/file/{file_id}/stat/` -- get the metadata about a file (file_id is its UUID)
- GET: `/file/{file_id}/read/` -- get the content of a file (file_id is its UUID)
- DELETE: `/file/{file_id}/` -- delete a file from the dict (file_id is its UUID)
"""

from fastapi import FastAPI, File, Form, HTTPException, status, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel, Field, field_serializer
from typing import Optional
from datetime import datetime
from uuid import *

app = FastAPI()

files = {}


class FileMeta(BaseModel):
    id: Optional[str] = Field(None, description="UUID of the file")
    name: str = Field(..., description="Name of the file, including extension")
    mimetype: str = Field(..., description="MIME type of the file, e.g., 'text/plain'")
    size: int = Field(..., description="Size of the file in bytes")
    create_datetime: Optional[datetime] = Field(..., description="Timestamp of file creation")


class StoredFile(FileMeta):
    content: bytes = Field(..., description="Binary content of the file")

    @field_serializer("create_datetime", when_used="json")
    def serialize_created_at(self, value: datetime) -> str:
        return value.isoformat(timespec='seconds')


@app.post("/file/", response_model=StoredFile)
async def upload_file(
        uploaded_file: UploadFile = File(...),
        created_at: Optional[datetime] = Form(None)
):
    if not created_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="created_at is required"
        )

    content = await uploaded_file.read()

    file_id = UUID('a3c2e4b1-51bf-4c79-9a98-0be6638d5195')

    file = StoredFile(
        id=str(file_id),
        name=uploaded_file.filename,
        mimetype=uploaded_file.content_type,
        size=uploaded_file.size,
        create_datetime=created_at,
        content=content
    )

    files[file_id] = file

    return file


@app.get("/file/")
async def all_files():
    return files


@app.get("/file/{file_id}/stat/")
async def stat(file_id: UUID):
    file = files.get(file_id)

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return {
        "create_datetime": file.create_datetime,
        "size": file.size,
        "mimetype": file.mimetype,
        "name": file.name
    }


@app.get("/file/{file_id}/read/")
async def read(file_id: UUID):
    file = files.get(file_id)

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return Response(
        content=file.content,
        media_type=file.mimetype,
        headers={
            "Content-Disposition": f'inline; filename="{file.name}"'
        }
    )


@app.delete("/file/{file_id}/", response_model=StoredFile)
async def delete_file(file_id: UUID):
    file = files.pop(file_id, None)

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return file
