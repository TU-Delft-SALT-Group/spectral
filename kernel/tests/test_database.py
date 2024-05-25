import pytest
from unittest.mock import Mock, patch
from spectral.database import Database


@pytest.fixture
def db():
    return Database(
        user="test_user",
        password="test_pass",
        host="test_host",
        port=5432,
        dbname="test_db",
    )


@patch("spectral.database.psycopg.connect")
def test_connection(mock_connect, db):
    db.connection()
    (
        mock_connect.assert_called_once_with(
            dbname="test_db",
            user="test_user",
            password="test_pass",
            host="test_host",
            port=5432,
        )
    )


def test_fetch_file(db):
    mock_cursor = Mock()
    db.conn = Mock()
    db.cursor = mock_cursor
    mock_cursor.fetchone.return_value = [
        1,
        "test_name",
        b"test_data",
        "creation_time",
        "modified_time",
        "uploader",
        "session",
        False,
    ]

    result = db.fetch_file(1)
    assert result == {
        "id": 1,
        "name": "test_name",
        "data": b"test_data",
        "creationTime": "creation_time",
        "modifiedTime": "modified_time",
        "uploader": "uploader",
        "session": "session",
        "emphemeral": False,
    }, "Fetch file result does not match expected format"
    mock_cursor.execute.assert_called_once_with("SELECT * FROM files WHERE id = %s", [1])


def test_store_transcription(db):
    mock_cursor = Mock()
    db.conn = Mock()
    db.cursor = mock_cursor

    file_transcription = [{"start": 0.0, "end": 1.0, "value": "hello"}]
    db.store_transcription(1, file_transcription)

    assert (
        mock_cursor.execute.call_count == 2
    ), "Store transcription did not execute expected number of queries"


def test_get_transcriptions(db):
    mock_cursor = Mock()
    db.conn = Mock()
    db.cursor = mock_cursor
    mock_cursor.fetchall.side_effect = [[(1,)], [(0.0, 1.0, "hello")]]

    result = db.get_transcriptions(1)
    assert result == [
        [{"start": 0.0, "end": 1.0, "value": "hello"}]
    ], "Get transcriptions result does not match expected format"
    mock_cursor.execute.assert_called()


def test_close(db):
    mock_cursor = Mock()
    db.conn = Mock()
    db.cursor = mock_cursor

    db.close()
    mock_cursor.close.assert_called_once()
    db.conn.close.assert_called_once()
