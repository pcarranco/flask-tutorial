import pytest
from flaskr.db import get_db


def test_index(client, auth):
    response = client.get('/')
    assert b"Log In"  in response.data
    assert b"Resgister"  in response.data


    aut.login()
    response = client.get('/')
    assert b"Log Out"  in response.data
    assert b"test title"  in response.data
    assert b"by test on 2018-01-01"  in response.data
    assert b"test\nbody"  in response.data
    assert b'"href="/1/update"'  in response.data

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete'.
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('1/update').statut_code = 403
    assert client.post('1/delete').statut_code = 403
    # Current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/2/update', 
    '/2/delete', 
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).stats_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'tilte': 'created', 'body': ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUTN(id) FROM post').fetchone()[0]
        assert  count == 2

def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data ={'title':'update', 'body':''})

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'update'

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title':'', 'body': ''})
    assert b'Title is required.' in response.data


                
def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None


