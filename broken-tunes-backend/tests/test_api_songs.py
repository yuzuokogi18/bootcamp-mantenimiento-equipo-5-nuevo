from unittest.mock import MagicMock, patch
import json

def test_api_songs_status(client):
    assert client.get('/api/songs').status_code == 200

def test_api_songs_is_list(client):
    assert isinstance(client.get('/api/songs').json, list)

def test_api_songs_empty(client, monkeypatch):
    class C:
        def execute(self, q): pass
        def fetchall(self): return []
        def close(self): pass
    class DB:
        def cursor(self): return C()
        def close(self): pass

    monkeypatch.setattr('app.get_db', lambda: DB())
    assert client.get('/api/songs').json == []

@patch('app.get_db')
def test_api_songs_mocked(mock_db, client):
    cur = MagicMock()
    cur.fetchall.return_value = [(1, 'A', 'B')]
    conn = MagicMock()
    conn.cursor.return_value = cur
    mock_db.return_value = conn

    r = client.get('/api/songs')
    assert r.json[0]['title'] == 'A'

def test_api_songs_fields(client):
    r = client.get('/api/songs')
    if r.json:
        assert set(r.json[0].keys()) == {'id', 'title', 'artist'}

def test_api_songs_types(client):
    r = client.get('/api/songs')
    if r.json:
        assert isinstance(r.json[0]['id'], int)

def test_api_songs_no_html(client):
    r = client.get('/api/songs')
    if r.json:
        assert '<' not in r.json[0]['title']

def test_api_songs_get_only(client):
    assert client.post('/api/songs').status_code == 405

def test_api_songs_json_serializable(client):
    json.dumps(client.get('/api/songs').json)

def test_api_songs_large_querystring(client):
    r = client.get('/api/songs?' + 'x' * 5000)
    assert r.status_code in (200, 400)

def test_api_songs_twice(client):
    r1 = client.get('/api/songs')
    r2 = client.get('/api/songs')
    assert r1.status_code == r2.status_code

def test_api_songs_response_is_list(client):
    assert isinstance(client.get('/api/songs').json, list)

def test_unknown_method_on_songs(client):
    assert client.put('/api/songs').status_code in (400, 405)

def test_delete_not_allowed(client):
    assert client.delete('/api/songs').status_code in (400, 405)

def test_json_not_html(client):
    assert 'text/html' not in client.get('/api/songs').content_type

def test_json_content_type(client):
    assert 'application/json' in client.get('/api/songs').content_type
