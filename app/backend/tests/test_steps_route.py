import unittest
from unittest.mock import patch
from main import app  # Assuming create_app is the app factory function in your app

class BuildStageStepsTest(unittest.TestCase):
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

    @patch("routes.get_stage_steps")
    def test_get_stage_steps_success(self, mock_get_stage_steps):
        # Mock server.get_stage_steps to simulate a successful job trigger
        mock_steps = [
                {
                    "id": 1,
                    "displayName": "Step 1",
                    "displayDescription": "Step 1 description",
                    "state": "SUCCESS",
                    "result": "SUCCESS",
                    "startTime": "2021-09-01T12:00:00",
                    "durationInMillis": 1000
                },
                {
                    "id": 2,
                    "displayName": "Step 2",
                    "displayDescription": "Step 2 description",
                    "state": "SUCCESS",
                    "result": "SUCCESS",
                    "startTime": "2021-09-01T12:01:00",
                    "durationInMillis": 2000
                }

        ]
        mock_get_stage_steps.return_value = mock_steps

        response = self.client.get('/build-stages/123/stages/1/steps')
        json_data = response.get_json()

        # Assert the response status status_code
        self.assertEqual(response.status_code, self.SuccessErrorCode)

        # Verify the returned data structure and content
        self.assertEqual(json_data["status"], "success")
        self.assertEqual(len(json_data["body"]["steps"]), 2)
        for i, step in enumerate(json_data["body"]["steps"]):
            self.assertEqual(step["id"], mock_steps[i]["id"])
            self.assertEqual(step["type"], mock_steps[i]["displayName"])
            self.assertEqual(step["content"], mock_steps[i]["displayDescription"])
            self.assertEqual(step["state"], mock_steps[i]["state"])
            self.assertEqual(step["status"], mock_steps[i]["result"])
            self.assertEqual(step["start_time"], mock_steps[i]["startTime"])
            self.assertEqual(step["duration"], mock_steps[i]["durationInMillis"])

    @patch("routes.get_stage_steps")
    def test_get_stage_steps_request_failure(self, mock_get_stage_steps):
        # Mock server.get_stage_steps to raise a RequestException
        from requests import RequestException
        msg = "Network error"
        mock_get_stage_steps.side_effect = RequestException(msg)

        response = self.client.get('/build-stages/123/stages/1/steps')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.RequestExceptionErrorCode)

        # Verify the returned data structure and error message
        self.assertEqual(json_data["status"], "failure")
        self.assertIn("message", json_data["body"])
        self.assertEqual(f"Network error: {msg}", json_data["body"]["message"])

    @patch("routes.get_stage_steps")
    def test_get_stage_steps_timeout(self, mock_get_stage_steps):
        # Mock server.get_stage_steps to raise a TimeoutError
        msg = "Request timeout"
        mock_get_stage_steps.side_effect = TimeoutError(msg)

        response = self.client.get('/build-stages/123/stages/1/steps')
        json_data = response.get_json()

        # Assert the response status code
        self.assertEqual(response.status_code, self.TimeoutErrorCode)

        # Verify the returned data structure and error message
        self.assertEqual(json_data["status"], "failure")
        self.assertIn("message", json_data["body"])
        self.assertEqual(f"Request timeout: {msg}", json_data["body"]["message"])

    @patch("routes.get_stage_steps")
    def test_get_stage_steps_unknown_error(self, mock_get_stage_steps):
        # Mock server.get_stage_steps to raise a generic Exception
        msg = "Unknown error"
        mock_get_stage_steps.side_effect = Exception(msg)

        response = self.client.get('/build-stages/123/stages/1/steps')
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

if __name__ == '__main__':
    unittest.main()
