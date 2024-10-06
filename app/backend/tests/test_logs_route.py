import unittest
from unittest.mock import patch
from main import app  # Assuming create_app is the app factory function in your app

class GetLogsTest(unittest.TestCase):
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

    @patch("routes.get_step_logs")
    def test_get_step_logs_success(self, mock_get_step_logs):
        # Mock server.get_step_logs to simulate a successful job trigger
        mock_logs = "Log content"
        mock_get_step_logs.return_value = mock_logs

        response = self.client.get('/build-stages/123/stages/1/steps/1/logs')
        json_data = response.get_json()

        # Assert the response status status_code
        self.assertEqual(response.status_code, self.SuccessErrorCode)

        # Verify the returned data structure and content
        self.assertEqual(json_data["status"], "success")
        self.assertEqual(json_data["body"]["logs"], mock_logs)

    @patch("routes.get_step_logs")
    def test_get_step_logs_request_failure(self, mock_get_step_logs):
        # Mock server.get_step_logs to raise a RequestException
        from requests import RequestException
        msg = "Network error"
        mock_get_step_logs.side_effect = RequestException(msg)

        response = self.client.get('/build-stages/123/stages/1/steps/1/logs')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.RequestExceptionErrorCode)

        # Verify the returned data structure and error message
        self.assertEqual(json_data["status"], "failure")
        self.assertIn("message", json_data["body"])
        self.assertEqual(f"Network error: {msg}", json_data["body"]["message"])

    @patch("routes.get_step_logs")
    def test_get_step_logs_timeout(self, mock_get_step_logs):
        # Mock server.get_step_logs to raise a TimeoutError
        msg = "Request timeout"
        mock_get_step_logs.side_effect = TimeoutError(msg)

        response = self.client.get('/build-stages/123/stages/1/steps/1/logs')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.TimeoutErrorCode)

        # Verify the returned data structure and error message
        self.assertEqual(json_data["status"], "failure")
        self.assertIn("message", json_data["body"])
        self.assertEqual(f"Request timeout: {msg}", json_data["body"]["message"])

    @patch("routes.get_step_logs")
    def test_get_step_logs_unknown_error(self, mock_get_step_logs):
        # Mock server.get_step_logs to raise a generic Exception
        msg = "Unknown error"
        mock_get_step_logs.side_effect = Exception(msg)

        response = self.client.get('/build-stages/123/stages/1/steps/1/logs')
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

