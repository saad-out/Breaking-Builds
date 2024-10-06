import unittest
from unittest.mock import patch
from main import app  # Assuming create_app is the app factory function in your app

class GetBuildQueueStateTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create the app and configure it for testing
        cls.app = app # create_app()
        cls.SuccessErrorCode = 200
        cls.JenkinsExceptionErrorCode = 502
        cls.RequestExceptionErrorCode = 502
        cls.TimeoutErrorCode = 504
        cls.UnknownErrorCode = 500
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    @patch("routes.server.get_queue_item")
    def test_get_build_queue_state_success_left(self, mock_get_queue_item):
        # Mock server.get_queue_item to simulate a successful job trigger
        mock_queue_info = {"executable": {"number": 123}}
        mock_get_queue_item.return_value = mock_queue_info

        response = self.client.get('/queue-state/123')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.SuccessErrorCode)
        
        # Verify the returned data structure and content
        self.assertEqual(json_data["status"], "success")
        self.assertEqual(json_data["body"]["state"], "left")
        self.assertEqual(json_data["body"]["build_number"], 123)
        # Assert logging (optional, if logger is used)
        # mock_logger.info.assert_called_once_with(
        #     f"Getting build queue state for build: {build_id}..."
        # )

    @patch("routes.server.get_queue_item")
    def test_get_build_queue_state_success_cancelled(self, mock_get_queue_item):
        # Mock server.get_queue_item to simulate a successful job trigger
        mock_queue_info = {"cancelled": True}
        mock_get_queue_item.return_value = mock_queue_info

        response = self.client.get('/queue-state/123')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.SuccessErrorCode)
        
        # Verify the returned data structure and content
        self.assertEqual(json_data["status"], "success")
        self.assertEqual(json_data["body"]["state"], "cancelled")
        # Assert logging (optional, if logger is used)
        # mock_logger.info.assert_called_once_with(
        #     f"Getting build queue state for build: {build_id}..."
        # )

    @patch("routes.server.get_queue_item")
    def test_get_build_queue_state_success_queued(self, mock_get_queue_item):
        # Mock server.get_queue_item to simulate a successful job trigger
        mock_queue_info = {}
        mock_get_queue_item.return_value = mock_queue_info

        response = self.client.get('/queue-state/123')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.SuccessErrorCode)
        
        # Verify the returned data structure and content
        self.assertEqual(json_data["status"], "success")
        self.assertEqual(json_data["body"]["state"], "queued")
        # Assert logging (optional, if logger is used)
        # mock_logger.info.assert_called_once_with(
        #     f"Getting build queue state for build: {build_id}..."
        # )

    @patch("routes.server.get_queue_item")
    def test_get_build_queue_state_jenkins_failure(self, mock_get_queue_item):
        # Mock server.get_queue_item to raise a JenkinsException
        from jenkins import JenkinsException
        msg = "Jenkins Error"
        mock_get_queue_item.side_effect = JenkinsException(msg)

        response = self.client.get('/queue-state/123')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.JenkinsExceptionErrorCode)

        # Verify the returned data structure and error message
        self.assertEqual(json_data["status"], "failure")
        self.assertIn("message", json_data["body"])
        self.assertEqual(f"Error getting build queue state: {msg}", json_data["body"]["message"])


    @patch("routes.server.get_queue_item")
    def test_get_build_queue_state_request_failure(self, mock_get_queue_item):
        # Mock server.get_queue_item to raise a RequestException
        from requests import RequestException
        msg = "Network error"
        mock_get_queue_item.side_effect = RequestException(msg)

        response = self.client.get('/queue-state/123')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.RequestExceptionErrorCode)

        # Verify the returned data structure and error message
        self.assertEqual(json_data["status"], "failure")
        self.assertIn("message", json_data["body"])
        self.assertEqual(f"Network error: {msg}", json_data["body"]["message"])


    @patch("routes.server.get_queue_item")
    def test_get_build_queue_state_timeout(self, mock_get_queue_item):
        # Mock server.get_queue_item to raise a TimeoutError
        msg = "Request timeout"
        mock_get_queue_item.side_effect = TimeoutError(msg)

        response = self.client.get('/queue-state/123')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.TimeoutErrorCode)

        # Verify the returned data structure and error message
        self.assertEqual(json_data["status"], "failure")
        self.assertIn("message", json_data["body"])
        self.assertEqual(f"Request timeout: {msg}", json_data["body"]["message"])

    @patch("routes.server.get_queue_item")
    def test_get_build_queue_state_unknown_error(self, mock_get_queue_item):
        # Mock server.get_queue_item to raise a generic Exception
        msg = "Unknown error"
        mock_get_queue_item.side_effect = Exception(msg)

        response = self.client.get('/queue-state/123')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.UnknownErrorCode)

        # Verify the returned data structure and error message
        self.assertEqual(json_data["status"], "failure")
        self.assertIn("message", json_data["body"])
        self.assertEqual(f"Unknown error: {msg}", json_data["body"]["message"])

    @classmethod
    def tearDownClass(cls):
        cls.client = None

if __name__ == "__main__":
    unittest.main()

