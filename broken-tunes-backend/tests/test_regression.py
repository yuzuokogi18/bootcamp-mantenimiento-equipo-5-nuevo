def test_regression_songs_status(client):
    assert client.get('/api/songs').status_code == 200


def test_regression_songs_is_list(client):
    assert isinstance(client.get('/api/songs').json, list)


def test_regression_songs_content_type(client):
    assert 'application/json' in client.get('/api/songs').content_type


def test_regression_songs_not_html(client):
    assert 'text/html' not in client.get('/api/songs').content_type


def test_regression_songs_twice(client):
    r1 = client.get('/api/songs')
    r2 = client.get('/api/songs')
    assert r1.status_code == r2.status_code


def test_regression_songs_post_not_allowed(client):
    assert client.post('/api/songs').status_code == 405


def test_regression_songs_delete_not_allowed(client):
    assert client.delete('/api/songs').status_code in (400,405)


def test_regression_songs_large_query(client):
    r = client.get('/api/songs?' + 'x'*3000)
    assert r.status_code in (200,400)


def test_regression_backup_not_found(client):
    assert client.post('/api/backup/9999').status_code == 404


def test_regression_backup_endpoint(client):
    assert client.post('/api/backup/1').status_code in (200,404)


def test_regression_backup_json(client):
    assert client.post('/api/backup/999').is_json


def test_regression_backup_method_not_allowed(client):
    assert client.get('/api/backup/1').status_code == 405


def test_regression_backup_put_invalid(client):
    assert client.put('/api/backup/1').status_code == 405


def test_regression_backup_form_data(client):
    r = client.post('/api/backup/999', data={'note':'test'})
    assert r.status_code in (200,404)


def test_regression_backup_sql_injection(client):
    assert client.post('/api/backup/1 OR 1=1').status_code in (400,404,405)


def test_regression_play_ok(client):
    assert client.get('/play/1').status_code in (200,404)


def test_regression_play_not_found(client):
    assert client.get('/play/9999').status_code == 404


def test_regression_play_invalid_id(client):
    assert client.get('/play/abc').status_code in (400,404)


def test_regression_play_post_not_allowed(client):
    assert client.post('/play/1').status_code == 405


def test_regression_play_sql(client):
    assert client.get('/play/1 OR 1=1').status_code in (200,400,404)


def test_regression_play_sql_encoded(client):
    assert client.get('/play/1%20OR%201=1').status_code in (200,400,404)


def test_regression_play_path_traversal(client):
    assert client.get('/play/../../etc/passwd').status_code in (400,404)


def test_regression_play_invalid_characters(client):
    assert client.get('/play/!!!!').status_code < 500


def test_regression_play_mimetype(client):
    r = client.get('/play/1')
    if r.status_code == 200:
        assert 'audio' in r.content_type


def test_regression_unknown_route(client):
    assert client.get('/noexiste').status_code == 404


def test_regression_api_songs_structure(client):
    r = client.get('/api/songs')
    if r.json:
        assert 'title' in r.json[0]


def test_regression_api_songs_artist_field(client):
    r = client.get('/api/songs')
    if r.json:
        assert 'artist' in r.json[0]


def test_regression_api_songs_id_field(client):
    r = client.get('/api/songs')
    if r.json:
        assert 'id' in r.json[0]


def test_regression_api_songs_id_type(client):
    r = client.get('/api/songs')
    if r.json:
        assert isinstance(r.json[0]['id'], int)


def test_regression_api_songs_json_valid(client):
    assert client.get('/api/songs').is_json