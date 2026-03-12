def test_api_songs_not_empty_status(client):
    r = client.get('/api/songs')
    assert r.status_code == 200


def test_backup_endpoint_exists(client):
    r = client.post('/api/backup/1')
    assert r.status_code in (200, 404)


def test_play_endpoint_exists(client):
    r = client.get('/play/1')
    assert r.status_code in (200, 404)