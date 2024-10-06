import unittest
from unittest.mock import patch
from main import app  # Assuming create_app is the app factory function in your app

class BuildStagesTest(unittest.TestCase):
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

    @patch("routes.get_build_stages")
    def test_get_build_stages_success(self, mock_get_build_stages):
        # Mock server.get_build_stages to simulate a successful job trigger
        mock_stages = [
                {
                    "id": 1,
                    "displayName": "Stage 1",
                    "displayDescription": "Stage 1 description",
                    "state": "SUCCESS",
                    "result": "SUCCESS",
                    "startTime": "2021-09-01T12:00:00",
                    "durationInMillis": 1000
                },
                {
                    "id": 2,
                    "displayName": "Stage 2",
                    "displayDescription": "Stage 2 description",
                    "state": "SUCCESS",
                    "result": "SUCCESS",
                    "startTime": "2021-09-01T12:01:00",
                    "durationInMillis": 2000
                }
        ]
        mock_get_build_stages.return_value = mock_stages

        response = self.client.get('/build-stages/123')
        json_data = response.get_json()

        # Assert the response status status_code
        self.assertEqual(response.status_code, self.SuccessErrorCode)

        # Verify the returned data structure and content
        self.assertEqual(json_data["status"], "success")
        self.assertEqual(len(json_data["body"]["stages"]), 2)
        for i, stage in enumerate(json_data["body"]["stages"]):
            self.assertEqual(stage["id"], mock_stages[i]["id"])
            self.assertEqual(stage["name"], mock_stages[i]["displayName"])
            self.assertEqual(stage["description"], mock_stages[i]["displayDescription"])
            self.assertEqual(stage["state"], mock_stages[i]["state"])
            self.assertEqual(stage["status"], mock_stages[i]["result"])
            self.assertEqual(stage["start_time"], mock_stages[i]["startTime"])
            self.assertEqual(stage["duration"], mock_stages[i]["durationInMillis"])

    @patch("routes.get_build_stages")
    def test_get_build_stages_request_failure(self, mock_get_build_stages):
        # Mock server.get_build_stages to raise a RequestException
        from requests import RequestException
        msg = "Network error"
        mock_get_build_stages.side_effect = RequestException(msg)

        response = self.client.get('/build-stages/123')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.RequestExceptionErrorCode)

        # Verify the returned data structure and error message
        self.assertEqual(json_data["status"], "failure")
        self.assertIn("message", json_data["body"])
        self.assertEqual(f"Network error: {msg}", json_data["body"]["message"])

    @patch("routes.get_build_stages")
    def test_get_build_stages_timeout(self, mock_get_build_stages):
        # Mock server.get_build_stages to raise a TimeoutError
        msg = "Request timeout"
        mock_get_build_stages.side_effect = TimeoutError(msg)

        response = self.client.get('/build-stages/123')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.TimeoutErrorCode)

        # Verify the returned data structure and error message
        self.assertEqual(json_data["status"], "failure")
        self.assertIn("message", json_data["body"])
        self.assertEqual(f"Request timeout: {msg}", json_data["body"]["message"])

    @patch("routes.get_build_stages")
    def test_get_build_stages_unknown_error(self, mock_get_build_stages):
        # Mock server.get_build_stages to raise a generic Exception
        msg = "Unknown error"
        mock_get_build_stages.side_effect = Exception(msg)

        response = self.client.get('/build-stages/123')
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
