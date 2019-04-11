
import os
import requests
import unittest
from sqlalchemy import create_engine

class DockerComposeTestCase(unittest.TestCase):

    def test_endpoint(self):
        r = requests.post('http://localhost:5000/add', data={'expression':'100+100'})
        self.assertNotEqual(r.text.find('100+100'), -1)

    def test_error_endpoint(self):
        r = requests.post('http://localhost:5000/add', data={'expression':'100+'})
        self.assertNotEqual(r.status_code, 200)

    def test_db(self):
        r = requests.post('http://localhost:5000/add', data={'expression':'100+100'})
        engine = create_engine('postgresql://cs162_user:cs162_password@localhost:5432/cs162', echo = True)

        with engine.connect() as con:
            rs = con.execute("SELECT * FROM Expression WHERE text = '100+100'")
            rows = rs.fetchall()

        self.assertNotEqual(len(rows), 0)

    def test_error_db(self):
        r = requests.post('http://localhost:5000/add', data={'expression':'100+'})
        engine = create_engine('postgresql://cs162_user:cs162_password@localhost:5432/cs162', echo = True)

        with engine.connect() as con:
            rs = con.execute("SELECT * FROM Expression WHERE text = '100+'")
            rows = rs.fetchall()

        self.assertEqual(len(rows), 0)

    def test_rows(self):
        r = requests.post('http://localhost:5000/add', data={'expression':'100+100'})
        engine = create_engine('postgresql://cs162_user:cs162_password@localhost:5432/cs162', echo = True)

        with engine.connect() as con:

            rs = con.execute('SELECT * FROM Expression')
            rows = rs.fetchall()

        r2 = requests.post('http://localhost:5000/add', data={'expression':'100+'})

        with engine.connect() as con:

            rs2 = con.execute('SELECT * FROM Expression')
            rows2 = rs2.fetchall()

        self.assertEqual(len(rows), len(rows2))

if __name__ == '__main__':
    unittest.main()
