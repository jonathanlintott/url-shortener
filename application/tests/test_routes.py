import string
from unittest import mock, TestCase

from application.models import UrlPair
from application.routes import generate_string
from application.tests.base import BaseTestCase


class TestGenerateString(TestCase):
    def test_string(self):
        out = generate_string(12)
        self.assertEqual(len(out), 12)
        for char in out:
            self.assertIn(char, string.ascii_letters + string.digits)


class TestShortenUrl(BaseTestCase):
    url = '/shorten_url'

    def test_no_url_in_data(self):
        response = self.post(self.url, expected_status_code=400, data={
            'bad_joke': 'What did the duck say when it brought some '
                        'lipstick? Put it on my bill'
        })
        out = response.json
        self.assertIn('error', out)
        self.assertEqual(out['error'], "Must include 'url' in post data")

        self.assertEqual(len(UrlPair.query.all()), 0)

    def test_invalid_url(self):
        response = self.post(self.url, expected_status_code=400,
                             data={'url': 'NotAValid{}URL'})
        out = response.json
        self.assertIn('error', out)
        self.assertEqual(out['error'], 'Not a valid URL')

    @mock.patch('application.routes.generate_string')
    def test_valid_url(self, gen_mock):
        gen_mock.return_value = 'abc123'

        url = 'www.someplace.com'
        response = self.post(self.url, expected_status_code=201,
                             data={'url': url})
        out = response.json
        self.assertIn('shortened_url', out)
        self.assertEqual(out['shortened_url'], 'http://localhost/abc123')

        gen_mock.assert_called_once()

        url_pairs = UrlPair.query.all()
        self.assertEqual(len(url_pairs), 1)
        self.assertEqual(url_pairs[0].original_url, url)
        self.assertEqual(url_pairs[0].shortened_url, 'abc123')


class TestRetrieveURL(BaseTestCase):
    def _setup_data(self):
        self.original_url = 'http://www.anotherplace.org'
        self.shortened_url = 'def456'
        url_pair = UrlPair(original_url=self.original_url,
                           shortened_url=self.shortened_url)
        self.db.session.add(url_pair)
        self.db.session.commit()

    def test_no_record(self):
        response = self.get('/abc123', expected_status_code=404)
        out = response.json
        self.assertIn('error', out)
        self.assertEqual(out['error'], 'No URL found')

    def test_successful_redirect(self):
        response = self.get(f'/{self.shortened_url}', expected_status_code=302)
        self.assertEqual(response.location, self.original_url)


class TestIntegration(BaseTestCase):
    def test_store_and_retrieve(self):
        original_url = 'www.spacejam.com'

        response = self.post('/shorten_url', data={'url': original_url},
                             expected_status_code=201)
        out = response.json
        self.assertIn('shortened_url', out)
        shortened_url = out['shortened_url']

        endpoint = shortened_url.split('/')[-1]

        response2 = self.get(f'/{endpoint}', expected_status_code=302)
        self.assertEqual(response2.location, 'http://' + original_url)
