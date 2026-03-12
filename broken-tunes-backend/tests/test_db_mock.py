from unittest.mock import MagicMock, patch

@patch('app.get_db')
def test_db_cursor_used(mock_db, client):
    conn = MagicMock()
    mock_db.return_value = conn
    client.get('/api/songs')
    conn.cursor.assert_called()

@patch('app.get_db')
def test_db_closed(mock_db, client):
    conn = MagicMock()
    mock_db.return_value = conn
    client.get('/api/songs')
    conn.close.assert_called()

@patch('app.get_db')
def test_cursor_close(mock_db, client):
    cur = MagicMock()
    conn = MagicMock()
    conn.cursor.return_value = cur
    mock_db.return_value = conn
    client.get('/api/songs')
    cur.close.assert_called()

@patch('app.get_db')
def test_fetchall_called(mock_db, client):
    cur = MagicMock()
    cur.fetchall.return_value = []
    conn = MagicMock()
    conn.cursor.return_value = cur
    mock_db.return_value = conn
    client.get('/api/songs')
    cur.fetchall.assert_called()

@patch('app.get_db')
def test_execute_called(mock_db, client):
    cur = MagicMock()
    cur.fetchall.return_value = []
    conn = MagicMock()
    conn.cursor.return_value = cur
    mock_db.return_value = conn
    client.get('/api/songs')
    cur.execute.assert_called()

@patch('app.get_db')
def test_db_exception_handled(mock_db, client):
    mock_db.side_effect = Exception("DB Down")
    r = client.get('/api/songs')
    assert r.status_code == 500
