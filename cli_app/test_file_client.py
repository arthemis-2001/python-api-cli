import pytest
from requests.exceptions import *

import sys
import tempfile
from pathlib import Path
from typing import Any

import file_client


def test_stat(
        mock_stat: Any,
        capsys: pytest.CaptureFixture[str]
    ) -> None:
    line = "file-client -b rest stat 67a7c424-6b41-4f25-99e5-2aaccf334567"
    sys.argv = line.split()
    file_client.main()
    captured = capsys.readouterr()
    assert "File name: pinkie_pie.txt" in captured.out
    assert "Size: 17 bytes" in captured.out
    assert "MIME type: text/plain" in captured.out
    assert "File created at: 2025-01-01T12:00:00" in captured.out


def test_stat_another_url(
        mock_stat_another_url: Any,
        capsys: pytest.CaptureFixture[str]
    ) -> None:
    line = "file-client -b rest -u https://api.example.com/ stat 89c533b3-2106-4f26-adff-1314d3148896"
    sys.argv = line.split()
    file_client.main()
    captured = capsys.readouterr()
    assert "File name: main.py" in captured.out
    assert "Size: 30 bytes" in captured.out
    assert "MIME type: text/x-python" in captured.out
    assert "File created at: 2024-12-01T12:00:00" in captured.out


def test_stat_output_file(
        mock_stat: Any,
        capsys: pytest.CaptureFixture[str]
    ) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "out.txt"
        line = f"file-client -b rest -o {output_path} stat 67a7c424-6b41-4f25-99e5-2aaccf334567"
        sys.argv = line.split()
        file_client.main()
        assert output_path.exists()

        out = output_path.read_text()
        assert "File name: pinkie_pie.txt" in out
        assert "Size: 17 bytes" in out
        assert "MIME type: text/plain" in out
        assert "File created at: 2025-01-01T12:00:00" in out


def test_read(
        mock_read: Any,
        capsys: pytest.CaptureFixture[str]
    ) -> None:
    line = "file-client -b rest read 67a7c424-6b41-4f25-99e5-2aaccf334567"
    sys.argv = line.split()
    file_client.main()
    captured = capsys.readouterr()
    assert "Hello Pinkie Pie!" in captured.out


def test_read_another_url(
        mock_read_another_url: Any,
        capsys: pytest.CaptureFixture[str]
    ) -> None:
    line = "file-client -b rest -u https://api.example.com/ read 89c533b3-2106-4f26-adff-1314d3148896"
    sys.argv = line.split()
    file_client.main()
    captured = capsys.readouterr()
    assert "print(This is an example API!)" in captured.out


def test_read_output_file(
        mock_read: Any,
        capsys: pytest.CaptureFixture[str]
    ) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "out.txt"
        line = f"file-client -b rest -o {output_path} read 67a7c424-6b41-4f25-99e5-2aaccf334567"
        sys.argv = line.split()
        file_client.main()
        assert output_path.exists()

        out = output_path.read_text()
        assert "Hello Pinkie Pie!" in out


@pytest.mark.parametrize(
    "mock_error_status_code",
    [
        ("stat", "File not found", 404),
        ("read", "Bad request", 400),
        ("stat", "Unauthorized", 401),
        ("read", "Forbidden", 403),
        ("stat", "Internal server error", 500),
        ("read", "Request Timeout", 504),
    ],
    indirect=True,
)
def test_error(
        mock_error_status_code: Any,
        capsys: pytest.CaptureFixture[str]
    ) -> None:
    subcommand, message, status_code = mock_error_status_code
    line = f"file-client -b rest {subcommand} 67a7c424-6b41-4f25-99e5-2aaccf334569"
    sys.argv = line.split()
    with pytest.raises(SystemExit) as e:
        file_client.main()
    captured = capsys.readouterr()
    assert e.value.code == 1

    if status_code == 400:
        assert "Bad request." in captured.err
    elif status_code == 401:
        assert "Authorization required." in captured.err
    elif status_code == 403:
        assert "Access forbidden." in captured.err
    elif status_code == 404:
        assert f"File under 67a7c424-6b41-4f25-99e5-2aaccf334569 not found." in captured.err
    elif status_code >= 500:
        assert "Server error." in captured.err


@pytest.mark.parametrize(
    "mock_exception",
    [
        ("stat", "http://example.com/", ConnectionError),
        ("stat", "http://example.com/", Timeout),
        ("stat", "invalid://", MissingSchema),
        ("read", "http://example.com/", ConnectionError),
        ("read", "http://example.com/", Timeout),
        ("read", "invalid://", MissingSchema),
    ],
    indirect=True,
)
def test_exception(
        mock_exception: Any,
        capsys: pytest.CaptureFixture[str]
    ) -> None:
    subcommand, base_url, exception = mock_exception
    line = f"file-client -b rest -u {base_url} {subcommand} 67a7c424-6b41-4f25-99e5-2aaccf334571"
    sys.argv = line.split()
    with pytest.raises(SystemExit) as e:
        file_client.main()
    captured = capsys.readouterr()
    assert e.value.code == 1

    if exception == ConnectionError:
        assert "REST backend not reachable." in captured.err
    elif exception == Timeout:
        assert "Request timed out." in captured.err
    elif exception == InvalidSchema:
        assert "Error: Invalid URL." in captured.err


@pytest.mark.parametrize(
    "subcommand, backend",
    [("stat", "foo"), ("foo", "rest"), ("foo", "foo")],
)
def test_invalid_usage(
        subcommand: str,
        backend: str,
        capsys: pytest.CaptureFixture[str]
    ) -> None:
    line = f"file-client -b {backend} {subcommand} 67a7c424-6b41-4f25-99e5-2aaccf334569"
    sys.argv = line.split()
    with pytest.raises(SystemExit) as e:
        file_client.main()
    captured = capsys.readouterr()
    assert e.value.code == 2

    assert "file-client: error" in captured.err
