def test_unknown_route(client):
    assert client.get('/nope').status_code == 404
