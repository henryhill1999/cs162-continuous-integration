import os
import unittest

from project import app, db, ma


TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cs162_user:cs162_password@localhost/cs162?port=5430'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass

    #http request
    def test_main_page(self):
        response = self.app.post('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    #post request
    def test_add_valid(self):
        response = self.app.post(
          '/add',
          data = {“expression”:”1+1”},
          follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_add_invalid(self):
        response = self.app.post(
          '/add',
          data = {'expression':'1+'},
          follow_redirects=True
        )
        self.assertEqual(response.status_code, 401)

    #checking connection to db
    def test_connection_db(self):
        engine = create_engine('postgresql://cs162_user:cs162_password@localhost:5432/cs162', echo = True)
        import create_engine from sqlalchemy
        result = engine.connect()
        self.assertEqual(result.execute("SELECT value FROM Expression WHERE text='1+1'"), 2)


if __name__ == "__main__":
    unittest.main()
