import unittest
from unittest.mock import patch
from main import app  # Assuming create_app is the app factory function in your app

class TriggerBuildTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create the app and configure it for testing
        cls.app = app # create_app()
        cls.SuccessErrorCode = 202
        cls.JenkinsExceptionErrorCode = 502
        cls.RequestExceptionErrorCode = 502
        cls.TimeoutErrorCode = 504
        cls.UnknownErrorCode = 500
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    @patch("routes.server.build_job")
    def test_trigger_build_success(self, mock_build_job):
        # Mock server.build_job to simulate a successful job trigger
        mock_queue_id = 123
        mock_build_job.return_value = mock_queue_id

        response = self.client.post('/trigger-build')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.SuccessErrorCode)
        
        # Verify the returned data structure and content
        self.assertEqual(json_data["status"], "success")
        self.assertIn("info", json_data["body"])
        self.assertEqual(json_data["body"]["info"]["queue_id"], mock_queue_id)
        
        # Assert logging (optional, if logger is used)
        # mock_logger.info.assert_called_once_with(
        #     f"Build triggered for pipeline: {PIPELINE_NAME}, Build queue id: {mock_queue_id}"
        # )

    @patch("routes.server.build_job")
    def test_trigger_build_jenkins_failure(self, mock_build_job):
        # Mock server.build_job to raise a JenkinsException
        # mock_build_job.side_effect = Exception("Jenkins Error")
        from jenkins import JenkinsException
        msg = "Jenkins Error"
        mock_build_job.side_effect = JenkinsException(msg)

        response = self.client.post('/trigger-build')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.JenkinsExceptionErrorCode)

        # Verify the returned data structure and error message
        self.assertEqual(json_data["status"], "failure")
        self.assertIn("message", json_data["body"])
        self.assertEqual(f"Error triggering build: {msg}", json_data["body"]["message"])

    @patch("routes.server.build_job")
    def test_trigger_build_request_failure(self, mock_build_job):
        # Mock server.build_job to raise a RequestException
        from requests import RequestException
        msg = "Network error"
        mock_build_job.side_effect = RequestException(msg)

        response = self.client.post('/trigger-build')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.RequestExceptionErrorCode)

        # Verify the returned data structure and error message
        self.assertEqual(json_data["status"], "failure")
        self.assertIn("message", json_data["body"])
        self.assertEqual(f"Network error: {msg}", json_data["body"]["message"])

    @patch("routes.server.build_job")
    def test_trigger_build_timeout(self, mock_build_job):
        # Mock server.build_job to raise a TimeoutError
        msg = "Request timeout"
        mock_build_job.side_effect = TimeoutError(msg)

        response = self.client.post('/trigger-build')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.TimeoutErrorCode)

        # Verify the returned data structure and error message
        self.assertEqual(json_data["status"], "failure")
        self.assertIn("message", json_data["body"])
        self.assertEqual(f"Request timeout: {msg}", json_data["body"]["message"])

    @patch("routes.server.build_job")
    def test_trigger_build_unknown_error(self, mock_build_job):
        # Mock server.build_job to raise a generic Exception
        msg = "Unknown error"
        mock_build_job.side_effect = Exception(msg)

        response = self.client.post('/trigger-build')
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

