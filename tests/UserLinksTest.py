
import unittest
from server import app, db
from server.models import User, Post


class UserModelCase(unittest.TestCase):
    def setUp(self):
        # create temporal DB in memory!
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get(self):
        response = self.client.get('/index', follow_redirects = True)
        print(response)



