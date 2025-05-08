"""
A config file for tests that mocks the HTTP requests to a backend
"""

import pytest
from requests.exceptions import RequestException
from requests_mock import Mocker

from typing import Tuple
import re


@pytest.fixture
def mock_stat(requests_mock: Mocker) -> None:
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
def mock_stat_another_url(requests_mock: Mocker) -> None:
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
def mock_read(requests_mock: Mocker) -> None:
    requests_mock.get(
        'http://localhost/file/67a7c424-6b41-4f25-99e5-2aaccf334567/read/',
        headers={"Content-Type": "text/plain; charset=utf-8"},
        content=b"Hello Pinkie Pie!",
        status_code=200
    )


@pytest.fixture
def mock_read_another_url(requests_mock: Mocker) -> None:
    requests_mock.get(
        'https://api.example.com/file/89c533b3-2106-4f26-adff-1314d3148896/read/',
        headers={"Content-Type": "text/x-python; charset=utf-8"},
        content=b"print(This is an example API!)",
        status_code=200
    )


@pytest.fixture
def mock_error_status_code(
        request: pytest.FixtureRequest,
        requests_mock: Mocker
    ) -> Tuple[str, str, int]:
    subcommand, message, status_code = request.param
    requests_mock.get(
        f'http://localhost/file/67a7c424-6b41-4f25-99e5-2aaccf334569/{subcommand}/',
        json={
            "detail": message,
        },
        status_code=status_code
    )
    return subcommand, message, status_code


@pytest.fixture
def mock_exception(
        request: pytest.FixtureRequest,
        requests_mock: Mocker
    ) -> Tuple[str, str, RequestException]:
    subcommand, base_url, exception = request.param
    requests_mock.get(
        f'{base_url}file/67a7c424-6b41-4f25-99e5-2aaccf334571/{subcommand}/',
        exc=exception
    )
    return subcommand, base_url, exception
