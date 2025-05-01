import pytest


@pytest.fixture
def mock_stat_response(requests_mock):
    requests_mock.get(
        'http://localhost/file/67a7c424-6b41-4f25-99e5-2aaccf334567/stat/',
        json={
            "create_datetime": "2025-01-01T12:00:00",
            "size": 17,
            "mimetype": "text/plain",
            "name": "pinkie_pie.txt"
        },
        status_code=200
    )


@pytest.fixture
def mock_read_response(requests_mock):
    requests_mock.get(
        'http://localhost/file/67a7c424-6b41-4f25-99e5-2aaccf334567/read/',
        headers={"Content-Type": "text/plain; charset=utf-8"},
        content=b"Hello Pinkie Pie!",
        status_code=200
    )
