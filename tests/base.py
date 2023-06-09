import unittest

from bluelog import create_app
from bluelog.extensions import db
from bluelog.models import Admin


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        self.client = self.app.test_client()
        self.cli_runner = self.app.test_cli_runner()

        db.create_all()
        user = Admin(name='Grey Li', username='grey', about='I am test', blog_title='Testlog', blog_sub_title='a test')
        user.set_password('123')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self, username=None, password=None):
        if username is None and password is None:
            username = 'grey'
            password = '123'

        return self.client.post('/auth/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)
