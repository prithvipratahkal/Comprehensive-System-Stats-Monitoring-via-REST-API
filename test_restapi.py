import unittest
from unittest.mock import patch, MagicMock
from bottle import request, response, abort, run
import json
import logging
from restapi import validate_api_key, system_stats
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', force=True)

class TestsForRESTApi(unittest.TestCase):

    # Simulating no API key provided
    @patch('bottle.request')
    def test_missing_api_key(self, mock_request):
        mock_request.get_header.return_value = None

        with self.assertRaises(Exception):
            validate_api_key()

        with self.assertRaises(AssertionError):
            mock_request.abort.assert_called_once_with(
                401, json.dumps({'status': 'error', 'message': 'Unauthorized: Missing API key'})
            )

    # Simulating invalid API key provided
    @patch('bottle.request')
    def test_invalid_api_key(self, mock_request):
        mock_request.get_header.return_value = 'invalid-key'

        with self.assertRaises(Exception):
            validate_api_key()

        with self.assertRaises(AssertionError):
            mock_request.abort.assert_called_once_with(
                401, json.dumps({'status': 'error', 'message': 'Unauthorized: Invalid API key'})
            )

    # Simulating valid API key provided
    @patch('restapi.request')
    @patch('restapi.abort')
    def test_valid_api_key(self, mock_abort, mock_request):
        mock_request.get_header.return_value = 'my-secret-key'
        validate_api_key()
        mock_abort.assert_not_called()

    
    # Helper function to mock query parameters
    def mock_query_params(self, mock_request, params):
        mock_request.query.get.side_effect = lambda key: params.get(key)

   # Test system stats with a few parameters
    @patch('bottle.request')
    def test_system_stats_few_params(self, mock_request):
        # Mock query parameters
        mock_request.query = MagicMock()
        mock_request.query.get.side_effect = lambda key: {
            'include_cpu': 'true',
            'include_memory': 'true',
            'include_disk': '',
            'include_network': None
        }.get(key)

        # Mock system stats functions
        with patch('restapi.get_cpu_usage', return_value={'cpu': '50%'}), \
             patch('restapi.get_memory_usage', return_value={'memory': '4GB'}):
            
            # Call the method
            response_data = system_stats()

            # Validate the response
            self.assertIn('cpu', response_data)
            self.assertIn('memory', response_data)


    # Test system stats query with all parameters included
    @patch('bottle.request')
    def test_system_stats_all_params(self, mock_request):
        self.mock_query_params(mock_request, {
            'include_cpu': 'true',
            'include_memory': 'true',
            'include_disk': 'true',
            'include_network': 'true'
        })

        # Mock system stats functions
        with patch('restapi.get_cpu_usage', return_value={'cpu': '50%'}), \
             patch('restapi.get_memory_usage', return_value={'memory': '4GB'}), \
             patch('restapi.get_disk_usage', return_value={'disk': '200GB'}), \
             patch('restapi.get_network_usage', return_value={'network': '100MBps'}):
            
            # Call the method
            response_data = system_stats()

            self.assertIn('cpu', response_data)
            self.assertIn('memory', response_data)
            self.assertIn('disk', response_data)
            self.assertIn('network', response_data)

        
    # Test system stats query with no parameters
    @patch('bottle.request')
    def test_system_stats_no_params(self, mock_request):
        self.mock_query_params(mock_request, {})

        # Mock the get_all_stats function
        with patch('restapi.get_cpu_usage', return_value={'cpu': '50%'}), \
            patch('restapi.get_memory_usage', return_value={'memory': '4GB'}), \
            patch('restapi.get_disk_usage', return_value={'disk': '200GB'}), \
            patch('restapi.get_network_usage', return_value={'network': '100MBps'}):
            response_data = system_stats()
            self.assertIn('cpu', response_data)
            self.assertIn('memory', response_data)
            self.assertIn('disk', response_data)
            self.assertIn('network', response_data)

    
    @patch('bottle.request')
    def test_system_stats_internal_error(self, mock_request):
        self.mock_query_params(mock_request, {
            'include_cpu': 'true',
            'include_memory': 'true',
            'include_disk': 'true',
            'include_network': 'true'
        })

        with patch('restapi.get_cpu_usage', side_effect=Exception("Test Error")):
            response_data = json.loads(system_stats())
            self.assertIn('status', response_data)
            self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['message'], 'Internal error occurred')


    @patch('bottle.request')
    def test_system_stats_invalid_params(self, mock_request):
        self.mock_query_params(mock_request, {'invalid_param': 'true'})

        response_data = json.loads(system_stats())
        self.assertIn('status', response_data)
        self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['message'], 'Invalid parameters provided')
