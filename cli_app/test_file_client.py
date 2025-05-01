import pytest

import sys
import tempfile
from pathlib import Path

import file_client


def test_stat(mock_stat_response, capsys):
    line = "file-client -b rest stat 67a7c424-6b41-4f25-99e5-2aaccf334567"
    sys.argv = line.split()
    file_client.main()
    captured = capsys.readouterr()
    assert "File name: pinkie_pie.txt" in captured.out
    assert "Size: 17 bytes" in captured.out
    assert "MIME type: text/plain" in captured.out
    assert "File created at: 2025-01-01T12:00:00" in captured.out


def test_stat_another_url(mock_stat_response_another_url, capsys):
    line = "file-client -b rest -u https://api.example.com/ stat 89c533b3-2106-4f26-adff-1314d3148896"
    sys.argv = line.split()
    file_client.main()
    captured = capsys.readouterr()
    assert "File name: main.py" in captured.out
    assert "Size: 30 bytes" in captured.out
    assert "MIME type: text/x-python" in captured.out
    assert "File created at: 2024-12-01T12:00:00" in captured.out


def test_stat_output_file(mock_stat_response, capsys):
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


def test_stat_not_found(mock_stat_response_not_found, capsys):
    line = "file-client -b rest stat 67a7c424-6b41-4f25-99e5-2aaccf334563"
    sys.argv = line.split()
    with pytest.raises(SystemExit) as e:
        file_client.main()
    captured = capsys.readouterr()
    assert e.value.code == 1
    assert "File under 67a7c424-6b41-4f25-99e5-2aaccf334563 not found." in captured.err


def test_read(mock_read_response, capsys):
    line = "file-client -b rest read 67a7c424-6b41-4f25-99e5-2aaccf334567"
    sys.argv = line.split()
    file_client.main()
    captured = capsys.readouterr()
    assert "Hello Pinkie Pie!" in captured.out


def test_read_another_url(mock_read_response_another_url, capsys):
    line = "file-client -b rest -u https://api.example.com/ read 89c533b3-2106-4f26-adff-1314d3148896"
    sys.argv = line.split()
    file_client.main()
    captured = capsys.readouterr()
    assert "print(This is an example API!)" in captured.out


def test_read_output_file(mock_read_response, capsys):
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "out.txt"
        line = f"file-client -b rest -o {output_path} read 67a7c424-6b41-4f25-99e5-2aaccf334567"
        sys.argv = line.split()
        file_client.main()
        assert output_path.exists()

        out = output_path.read_text()
        assert "Hello Pinkie Pie!" in out


def test_read_not_found(mock_read_response_not_found, capsys):
    line = "file-client -b rest read 67a7c424-6b41-4f25-99e5-2aaccf334563"
    sys.argv = line.split()
    with pytest.raises(SystemExit) as e:
        file_client.main()
    captured = capsys.readouterr()
    assert e.value.code == 1
    assert "File under 67a7c424-6b41-4f25-99e5-2aaccf334563 not found." in captured.err
