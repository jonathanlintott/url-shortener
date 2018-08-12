from flask_testing import TestCase
import json

from application import app, db


class BaseTestCase(TestCase):
    db = db

    def create_app(self):
        app.config.from_object('application.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

        if hasattr(self, '_setup_data'):
            self._setup_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get(self, url, expected_status_code=200):
        response = self.client.get(url)

        self.assertEqual(response.status_code, expected_status_code)

        return response

    def post(self, url, data, expected_status_code=200):
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, expected_status_code)

        return response
