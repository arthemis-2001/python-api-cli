from fastapi.testclient import TestClient

import io
from datetime import datetime

from .rest_api import app

client = TestClient(app)


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


def test_stat():
    response = client.get("/file/67a7c424-6b41-4f25-99e5-2aaccf334567/stat/")

    assert response.status_code == 200
    assert response.json() == {
        "create_datetime": "2025-01-01T12:00:00",
        "size": 17,
        "mimetype": "text/plain",
        "name": "pinkie_pie.txt"
    }


def test_read():
    response = client.get("/file/67a7c424-6b41-4f25-99e5-2aaccf334567/read/")

    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "text/plain; charset=utf-8"
    assert response.content == b"Hello Pinkie Pie!"


def test_delete_file():
    response = client.delete("/file/67a7c424-6b41-4f25-99e5-2aaccf334567/")

    assert response.status_code == 200
    data = response.json()

    assert data["create_datetime"] == "2025-01-01T12:00:00"
    assert data["size"] == 17
    assert data["mimetype"] == "text/plain"
    assert data["name"] == "pinkie_pie.txt"
