"""Tests for router.py — verifies routing, unclear handling, logging, and manual override."""

import unittest
import os
import json
from unittest.mock import patch, MagicMock
from router import route_and_respond


class TestRouteAndRespond(unittest.TestCase):
    """Test the route_and_respond function with mocked LLM responses."""

    # --- Unclear intent handling ---

    @patch("router.log_route")
    def test_unclear_intent_returns_clarifying_question(self, mock_log):
        """When intent is 'unclear', response must ask for clarification."""
        intent_data = {"intent": "unclear", "confidence": 0.3}
        result = route_and_respond("hey", intent_data)
        self.assertIn("coding", result.lower())
        self.assertIn("data analysis", result.lower())
        self.assertIn("writing", result.lower())
        self.assertIn("career", result.lower())

    @patch("router.log_route")
    def test_low_confidence_treated_as_unclear(self, mock_log):
        """When confidence < 0.7, route as unclear even if intent is set."""
        intent_data = {"intent": "code", "confidence": 0.4}
        result = route_and_respond("do something", intent_data)
        self.assertIn("not sure", result.lower())

    @patch("router.log_route")
    def test_unclear_intent_is_logged(self, mock_log):
        """Unclear intents must still be logged."""
        intent_data = {"intent": "unclear", "confidence": 0.2}
        route_and_respond("hey", intent_data)
        mock_log.assert_called_once()

    # --- Expert routing ---

    @patch("router.log_route")
    @patch("router.client")
    def test_code_intent_routes_to_code_prompt(self, mock_client, mock_log):
        """A 'code' intent should use the code expert prompt."""
        mock_response = MagicMock()
        mock_response.text = "Use list.sort() in Python."
        mock_client.models.generate_content.return_value = mock_response

        intent_data = {"intent": "code", "confidence": 0.95}
        result = route_and_respond("how do I sort a list?", intent_data)

        self.assertEqual(result, "Use list.sort() in Python.")
        mock_client.models.generate_content.assert_called_once()

    @patch("router.log_route")
    @patch("router.client")
    def test_data_intent_routes_correctly(self, mock_client, mock_log):
        mock_response = MagicMock()
        mock_response.text = "The average is 36.2."
        mock_client.models.generate_content.return_value = mock_response

        intent_data = {"intent": "data", "confidence": 0.9}
        result = route_and_respond("what's the average of 12, 45, 23, 67, 34", intent_data)
        self.assertEqual(result, "The average is 36.2.")

    @patch("router.log_route")
    @patch("router.client")
    def test_writing_intent_routes_correctly(self, mock_client, mock_log):
        mock_response = MagicMock()
        mock_response.text = "Consider removing passive voice."
        mock_client.models.generate_content.return_value = mock_response

        intent_data = {"intent": "writing", "confidence": 0.88}
        result = route_and_respond("My paragraph sounds awkward", intent_data)
        self.assertEqual(result, "Consider removing passive voice.")

    @patch("router.log_route")
    @patch("router.client")
    def test_career_intent_routes_correctly(self, mock_client, mock_log):
        mock_response = MagicMock()
        mock_response.text = "Practice STAR method for interviews."
        mock_client.models.generate_content.return_value = mock_response

        intent_data = {"intent": "career", "confidence": 0.92}
        result = route_and_respond("I'm preparing for a job interview", intent_data)
        self.assertEqual(result, "Practice STAR method for interviews.")

    # --- Logging ---

    @patch("router.client")
    @patch("router.log_route")
    def test_successful_route_calls_log(self, mock_log, mock_client):
        """Every successful route must call log_route."""
        mock_response = MagicMock()
        mock_response.text = "Answer."
        mock_client.models.generate_content.return_value = mock_response

        intent_data = {"intent": "code", "confidence": 0.95}
        route_and_respond("sort a list", intent_data)
        mock_log.assert_called_once()

    # --- Manual override ---

    @patch("router.log_route")
    @patch("router.client")
    def test_manual_override_routes_to_specified_intent(self, mock_client, mock_log):
        """@code prefix should bypass classifier and route to code expert."""
        mock_response = MagicMock()
        mock_response.text = "Here is a fix."
        mock_client.models.generate_content.return_value = mock_response

        intent_data = {"intent": "unclear", "confidence": 0.3}
        result = route_and_respond("@code fix this bug", intent_data)

        self.assertEqual(result, "Here is a fix.")
        # The logged intent_data should reflect the override
        logged_intent = mock_log.call_args[0][0]
        self.assertEqual(logged_intent["intent"], "code")

    @patch("router.log_route")
    def test_invalid_override_falls_through(self, mock_log):
        """An invalid @prefix should not override — treated normally."""
        intent_data = {"intent": "unclear", "confidence": 0.3}
        result = route_and_respond("@unknown do something", intent_data)
        self.assertIn("not sure", result.lower())


class TestLogFile(unittest.TestCase):
    """Test that log entries are valid JSONL."""

    LOG_FILE = "route_log.jsonl"

    @patch("router.client")
    def test_log_entry_has_required_keys(self, mock_client):
        """Each log entry must contain intent, confidence, user_message, final_response."""
        mock_response = MagicMock()
        mock_response.text = "Test response."
        mock_client.models.generate_content.return_value = mock_response

        # Clear log for isolated test
        if os.path.exists(self.LOG_FILE):
            with open(self.LOG_FILE, "r") as f:
                lines_before = len(f.readlines())
        else:
            lines_before = 0

        intent_data = {"intent": "code", "confidence": 0.95}
        route_and_respond("test message", intent_data)

        with open(self.LOG_FILE, "r") as f:
            lines = f.readlines()

        last_entry = json.loads(lines[-1])
        self.assertIn("intent", last_entry)
        self.assertIn("confidence", last_entry)
        self.assertIn("user_message", last_entry)
        self.assertIn("final_response", last_entry)


if __name__ == "__main__":
    unittest.main()
