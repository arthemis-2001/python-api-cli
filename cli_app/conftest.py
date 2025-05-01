"""
A config file for tests that mocks the HTTP requests to a backend
"""

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
def mock_stat_response_another_url(requests_mock):
    requests_mock.get(
        'https://api.example.com/file/89c533b3-2106-4f26-adff-1314d3148896/stat/',
        json={
            "create_datetime": "2024-12-01T12:00:00",
            "size": 30,
            "mimetype": "text/x-python",
            "name": "main.py"
        },
        status_code=200
    )


@pytest.fixture
def mock_stat_response_not_found(requests_mock):
    requests_mock.get(
        'http://localhost/file/67a7c424-6b41-4f25-99e5-2aaccf334563/stat/',
        json={
            "detail": "File not found",
        },
        status_code=404
    )


@pytest.fixture
def mock_read_response(requests_mock):
    requests_mock.get(
        'http://localhost/file/67a7c424-6b41-4f25-99e5-2aaccf334567/read/',
        headers={"Content-Type": "text/plain; charset=utf-8"},
        content=b"Hello Pinkie Pie!",
        status_code=200
    )


@pytest.fixture
def mock_read_response_another_url(requests_mock):
    requests_mock.get(
        'https://api.example.com/file/89c533b3-2106-4f26-adff-1314d3148896/read/',
        headers={"Content-Type": "text/x-python; charset=utf-8"},
        content=b"print(This is an example API!)",
        status_code=200
    )


@pytest.fixture
def mock_read_response_not_found(requests_mock):
    requests_mock.get(
        'http://localhost/file/67a7c424-6b41-4f25-99e5-2aaccf334563/read/',
        json={
            "detail": "File not found",
        },
        status_code=404
    )
