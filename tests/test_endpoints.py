import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/scripts")))
import unittest
from app import app, db

class TestEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

    def test_create_user(self):
        self.app.post('/register', data=dict(username='testuser', password='testpassword'), content_type='application/x-www-form-urlencoded')
        response = self.app.post('/create_user', data=dict(username='testuser'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('User created', response.data.decode())

    def test_create_channel(self):
        response = self.app.post('/create_channel', data=dict(channel_name='testchannel'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Channel created', response.data.decode())

    def test_send_message(self):
        # Log in first
        self.app.post('/login', data=dict(username='testuser', password='testpassword'), content_type='application/x-www-form-urlencoded')
        response = self.app.post('/send_message', data=dict(channel='testchannel', message='Hello World'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Message sent', response.data.decode())

if __name__ == '__main__':
    unittest.main()

