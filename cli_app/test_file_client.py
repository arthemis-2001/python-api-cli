import sys
import file_client


def test_stat(mock_stat_response, capsys):
    line = "file-client -b rest -u http://localhost/ stat 67a7c424-6b41-4f25-99e5-2aaccf334567"
    sys.argv = line.split()
    file_client.main()
    captured = capsys.readouterr()
    assert "File name: pinkie_pie.txt" in captured.out
    assert "Size: 17 bytes" in captured.out
    assert "MIME type: text/plain" in captured.out
    assert "File created at: 2025-01-01T12:00:00" in captured.out


def test_read(mock_read_response, capsys):
    line = "file-client -b rest -u http://localhost/ read 67a7c424-6b41-4f25-99e5-2aaccf334567"
    sys.argv = line.split()
    file_client.main()
    captured = capsys.readouterr()
    assert "Hello Pinkie Pie!" in captured.out
