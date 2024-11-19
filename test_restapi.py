import unittest
from webtest import TestApp
from bottle import default_app
from restapi import app  # Importing the Bottle app from restapi.py
import json
from unittest.mock import patch


class TestSystemStatsAPI(unittest.TestCase):

    def setUp(self):
        """Set up the test application."""
        # Wrap the Bottle app with `default_app()` for compatibility with `webtest`
        self.test_app = TestApp(default_app())
        self.api_key = "my-secret-key"
        self.headers = {'x-api-key': self.api_key}

    def test_no_api_key(self):
        """Test API request without an API key."""
        response = self.test_app.get('/system-stats', status=401)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized: Missing API key', json.loads(response.body.decode('utf-8'))['message'])

    def test_invalid_api_key(self):
        """Test API request with an invalid API key."""
        headers = {'x-api-key': 'wrong-key'}
        response = self.test_app.get('/system-stats', headers=headers, status=401)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized: Invalid API key', json.loads(response.body.decode('utf-8'))['message'])

    def test_valid_api_key_without_params(self):
        """Test API request with a valid API key but no parameters."""
        response = self.test_app.get('/system-stats', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('stats', json.loads(response.body.decode('utf-8')))

    def test_invalid_query_param(self):
        """Test API request with invalid query parameters."""
        response = self.test_app.get('/system-stats?invalid_param=true', headers=self.headers, status=400)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid parameters provided', json.loads(response.body.decode('utf-8'))['message'])

    def test_include_cpu(self):
        """Test API request with include_cpu parameter."""
        response = self.test_app.get('/system-stats?include_cpu=true', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('stats', json.loads(response.body.decode('utf-8')))

    def test_include_memory(self):
        """Test API request with include_memory parameter."""
        response = self.test_app.get('/system-stats?include_memory=true', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('stats', json.loads(response.body.decode('utf-8')))

    def test_include_disk(self):
        """Test API request with include_disk parameter."""
        response = self.test_app.get('/system-stats?include_disk=true', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('stats', json.loads(response.body.decode('utf-8')))

    def test_include_network(self):
        """Test API request with include_network parameter."""
        response = self.test_app.get('/system-stats?include_network=true', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('stats', json.loads(response.body.decode('utf-8')))

    def test_stats_exception_handling(self):
        """Test handling an exception during stats retrieval."""
        with patch('restapi.get_all_stats', side_effect=Exception("Simulated error")):
            response = self.test_app.get('/system-stats', headers=self.headers, status=500)
            self.assertEqual(response.status_code, 500)
            self.assertIn('Internal error occurred', json.loads(response.body.decode('utf-8'))['message'])

    def test_no_stats_collected(self):
        with patch('restapi.get_all_stats', return_value=None), \
            patch('restapi.get_cpu_usage', return_value=None), \
            patch('restapi.get_memory_usage', return_value=None), \
            patch('restapi.get_disk_usage', return_value=None), \
            patch('restapi.get_network_usage', return_value=None):
            response = self.test_app.get('/system-stats', headers=self.headers, status=500)
            self.assertEqual(response.status_code, 500)
            self.assertIn('No stats collected, check your parameters', json.loads(response.body.decode('utf-8'))['message'])



if __name__ == '__main__':
    unittest.main()
