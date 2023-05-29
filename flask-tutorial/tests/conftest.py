import os
import tempfile
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf-8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING':True, # Flask knows it's in test mode
        'DATABASE':db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    # A test client is a tool that can make requests to the application
    return app.test_client()

@pytest.fixture
def runner(app):
    # A test runner is a tool that orchestrates the execution of tests and
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        # url_for() generates the URL to a view based on a name and arguments
        return self._client.post(
            '/auth/login',
            data={'username':username, 'password':password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
