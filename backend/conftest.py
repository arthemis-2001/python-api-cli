import pytest
from datetime import datetime
from .rest_api import files
from .rest_api import StoredFile
from uuid import *


@pytest.fixture(scope="session", autouse=True)
def prefill():
    files.clear()

    file_content = b"Hello Pinkie Pie!"

    file_id = UUID('67a7c424-6b41-4f25-99e5-2aaccf334567')

    sample_file = StoredFile(
        id=str(file_id),
        name="pinkie_pie.txt",
        mimetype="text/plain",
        size=len(file_content),
        create_datetime=datetime(2025, 1, 1, 12, 0, 0),
        content=file_content
    )
    files[file_id] = sample_file
