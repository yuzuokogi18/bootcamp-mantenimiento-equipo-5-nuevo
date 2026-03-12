from unittest.mock import MagicMock, patch

@patch('app.get_db')
def test_play_ok(mock_db, client):
    cur = MagicMock()
    cur.fetchone.return_value = (1, 'Song', 'Artist', b'123', None)
    conn = MagicMock()
    conn.cursor.return_value = cur
    mock_db.return_value = conn

    assert client.get('/play/1').status_code == 200

def test_play_not_found(client):
    assert client.get('/play/9999').status_code == 404

@patch('app.get_db')
def test_play_mimetype(mock_db, client):
    cur = MagicMock()
    cur.fetchone.return_value = (1, 'Song', 'Artist', b'123', None)
    conn = MagicMock()
    conn.cursor.return_value = cur
    mock_db.return_value = conn

    assert client.get('/play/1').content_type == 'audio/mpeg'

def test_play_invalid_id(client):
    assert client.get('/play/abc').status_code in (400, 404)

@patch('app.get_db')
def test_play_empty_blob(mock_db, client):
    cur = MagicMock()
    cur.fetchone.return_value = (1, 'Song', 'Artist', b'', None)
    conn = MagicMock()
    conn.cursor.return_value = cur
    mock_db.return_value = conn

    assert client.get('/play/1').status_code == 200

def test_play_sql_injection(client):
    assert client.get('/play/1 OR 1=1').status_code in (400, 404)

def test_play_method_not_allowed(client):
    assert client.post('/play/1').status_code == 405

def test_play_sql_like_input(client):
    assert client.get('/play/1 OR 1=1').status_code in (200, 400, 404)

def test_play_encoded_sql_input(client):
    assert client.get('/play/1%20OR%201=1').status_code in (200, 400, 404)

def test_play_path_traversal(client):
    assert client.get('/play/../../etc/passwd').status_code in (400, 404)

def test_play_invalid_characters(client):
    assert client.get('/play/!!!!').status_code < 500
