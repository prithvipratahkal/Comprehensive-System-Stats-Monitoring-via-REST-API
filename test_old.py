import unittest
from unittest.mock import patch, MagicMock
import json
from restapi import validate_api_key
from restapi import  system_stats

def mock_get_cpu_usage():
    return {'cpu': 50}

def mock_get_memory_usage():
    return {'memory': 70}

def mock_get_disk_usage():
    return {'disk': 30}

def mock_get_network_usage():
    return {'network': 100}

def mock_get_all_stats():
    return {'cpu': 50, 'memory': 70, 'disk': 30, 'network': 100}

class TestsForRESTApi(unittest.TestCase):
    @patch('bottle.request.get_header')
    def test_missing_api_key(self, mock_get_header):
        # Simulating no API key provided
        mock_get_header.return_value = None

        validate_api_key()
        # Check that `abort` is called with the correct arguments for invalid key
        mock_abort.assert_called_once_with(
            401, json.dumps({'status': 'error', 'message': 'Unauthorized: Missing API key'})
        )

    # Test case to check the behavior when an invalid API key is provided
    @patch('bottle.request.get_header')
    def test_invalid_api_key(self, mock_get_header):
        # Simulating an invalid API key
        mock_get_header.return_value = "wrong-key"

        with self.assertRaises(Exception) as context:
            validate_api_key()  # This should trigger the 401 Unauthorized error
        self.assertEqual(str(context.exception), 'Unauthorized: Invalid API key')







    @patch('restapi.request')
    @patch('restapi.abort')
    def test_valid_api_key(self, mock_abort, mock_request):
        mock_request.get_header.return_value = 'my-secret-key'
        validate_api_key()
        # Check that `abort` is not called when the key is valid
        mock_abort.assert_not_called()

    @patch('restapi.request')
    @patch('restapi.abort')
    def test_missing_api_key(self, mock_abort, mock_request):
        mock_request.get_header.return_value = None
        validate_api_key()
        # Check that `abort` is called with the correct arguments for invalid key
        mock_abort.assert_called_once_with(
            401, json.dumps({'status': 'error', 'message': 'Unauthorized: Missing API key'})
        )

    @patch('restapi.request')
    @patch('restapi.abort')
    def test_invalid_api_key(self, mock_abort, mock_request):
        mock_request.get_header.return_value = 'invalid-key'
        validate_api_key()
        # Check that `abort` is called with the correct arguments for invalid key
        mock_abort.assert_called_once_with(
            401, json.dumps({'status': 'error', 'message': 'Unauthorized: Invalid API key'})
        )

    def setUp(self):
        self.patches = [
            patch('restapi.get_cpu_usage'),
            patch('restapi.get_memory_usage'),
            patch('restapi.get_disk_usage'),
            patch('restapi.get_network_usage'),
            patch('restapi.get_all_stats'),
            patch('restapi.response')
        ]
        
        # Start all patches
        self.mocks = [p.start() for p in self.patches]
        
        # Ensure that they are stopped after each test case
        self.addCleanup(self._stop_patches)

    def _stop_patches(self):
        for patch in self.patches:
            patch.stop()

    def test_no_query_params(self):
        self.mocks[0].return_value = 'all_stats'
        response_value = system_stats()
        expected_response = {
            "stats": ['cpu_stats', 'memory_stats', 'disk_stats', 'network_stats']
        }
        self.assertEqual(json.loads(response_value), expected_response)
        self.assertEqual(response.status, 200)

    
if __name__ == '__main__':
    unittest.main()