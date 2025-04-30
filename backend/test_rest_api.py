from fastapi.testclient import TestClient

import io
from datetime import datetime

from .rest_api import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_upload_file():
    file_content = b"Hello World!"

    file = io.BytesIO(file_content)
    name = "hello_world.txt"
    file.name = name

    mime_type = "text/plain"

    created_at = datetime.now().isoformat(timespec="seconds")

    response = client.post(
        "/file/",
        files={
            "uploaded_file": (file.name, file, mime_type)
        },
        data={
            "created_at": created_at
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["create_datetime"] == created_at
    assert data["size"] == len(file_content)
    assert data["mimetype"] == mime_type
    assert data["name"] == name



