import pytest
from datetime import datetime
from .rest_api import files
from .rest_api import StoredFile
import uuid


@pytest.fixture(scope="session", autouse=True)
def prefill():
    files.clear()

    file_content = b"Hello Pinkie Pie!"

    sample_file = StoredFile(
        id=str(uuid.uuid4()),
        name="pinkie_pie.txt",
        mimetype="text/plain",
        size=len(file_content),
        create_datetime=datetime(2025, 1, 1, 12, 0, 0),
        content=file_content
    )
    files[sample_file.id] = sample_file
