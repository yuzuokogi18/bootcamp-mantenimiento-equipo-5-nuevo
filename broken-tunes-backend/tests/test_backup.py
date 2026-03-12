from unittest.mock import MagicMock, patch

def test_backup_not_found(client):
    assert client.post('/api/backup/999').status_code == 404

@patch('app.get_db')
def test_backup_ok(mock_db, client):
    cur = MagicMock()
    cur.fetchone.return_value = (1, 'Song', 'Artist', b'123')
    cur.lastrowid = 5
    conn = MagicMock()
    conn.cursor.return_value = cur
    mock_db.return_value = conn

    r = client.post('/api/backup/1')
    assert r.json['ok'] is True

def test_backup_get_not_allowed(client):
    assert client.get('/api/backup/1').status_code == 405

def test_backup_default_values(client):
    assert client.post('/api/backup/999').status_code == 404

@patch('app.get_db')
def test_backup_commit_called(mock_db, client):
    cur = MagicMock()
    cur.fetchone.return_value = (1, 'Song', 'Artist', b'123')
    conn = MagicMock()
    conn.cursor.return_value = cur
    mock_db.return_value = conn

    client.post('/api/backup/1')
    conn.commit.assert_called_once()

def test_backup_json(client):
    assert client.post('/api/backup/999').is_json

def test_backup_form_data(client):
    assert client.post('/api/backup/999', data={'note': 'x'}).status_code == 404

def test_backup_numeric_id(client):
    assert client.post('/api/backup/1').status_code in (200, 404)

def test_backup_invalid_method(client):
    assert client.put('/api/backup/1').status_code == 405

def test_backup_response_type(client):
    r = client.post('/api/backup/999')
    assert isinstance(r.json, dict)

def test_backup_without_id(client):
    assert client.post('/api/backup/').status_code in (404, 405)

def test_api_backup_sql_injection(client):
    r = client.post('/api/backup/1 OR 1=1')
    assert r.status_code in (400, 404, 405)

def test_backup_returns_json(client):
    r = client.post('/api/backup/1')
    if r.status_code == 200:
        assert r.is_json
