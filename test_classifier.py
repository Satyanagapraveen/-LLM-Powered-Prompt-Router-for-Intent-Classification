"""Tests for classifier.py — verifies classify_intent output structure and fallback."""

import unittest
from unittest.mock import patch, MagicMock
from classifier import classify_intent


class TestClassifyIntent(unittest.TestCase):
    """Test the classify_intent function with mocked LLM responses."""

    VALID_INTENTS = {"code", "data", "writing", "career", "unclear"}

    @patch("classifier.client")
    def test_returns_valid_json_structure(self, mock_client):
        """classify_intent must return a dict with 'intent' (str) and 'confidence' (float)."""
        mock_response = MagicMock()
        mock_response.text = '{"intent": "code", "confidence": 0.95}'
        mock_client.models.generate_content.return_value = mock_response

        result = classify_intent("how do I sort a list in python?")

        self.assertIsInstance(result, dict)
        self.assertIn("intent", result)
        self.assertIn("confidence", result)
        self.assertIsInstance(result["intent"], str)
        self.assertIsInstance(result["confidence"], float)

    @patch("classifier.client")
    def test_valid_intent_labels(self, mock_client):
        """The returned intent must be one of the allowed labels."""
        mock_response = MagicMock()
        mock_response.text = '{"intent": "data", "confidence": 0.88}'
        mock_client.models.generate_content.return_value = mock_response

        result = classify_intent("what's the average of these numbers?")
        self.assertIn(result["intent"], self.VALID_INTENTS)

    @patch("classifier.client")
    def test_handles_markdown_wrapped_json(self, mock_client):
        """LLMs sometimes wrap JSON in ```json ... ``` — must still parse correctly."""
        mock_response = MagicMock()
        mock_response.text = '```json\n{"intent": "writing", "confidence": 0.9}\n```'
        mock_client.models.generate_content.return_value = mock_response

        result = classify_intent("my paragraph sounds awkward")
        self.assertEqual(result["intent"], "writing")
        self.assertEqual(result["confidence"], 0.9)

    @patch("classifier.client")
    def test_fallback_on_malformed_json(self, mock_client):
        """If the LLM returns garbage, must default to unclear/0.0 without crashing."""
        mock_response = MagicMock()
        mock_response.text = "Sorry, I can't classify that."
        mock_client.models.generate_content.return_value = mock_response

        result = classify_intent("hey")
        self.assertEqual(result["intent"], "unclear")
        self.assertEqual(result["confidence"], 0.0)

    @patch("classifier.client")
    def test_fallback_on_empty_response(self, mock_client):
        """Empty LLM response must also produce the safe fallback."""
        mock_response = MagicMock()
        mock_response.text = ""
        mock_client.models.generate_content.return_value = mock_response

        result = classify_intent("")
        self.assertEqual(result["intent"], "unclear")
        self.assertEqual(result["confidence"], 0.0)

    @patch("classifier.client")
    def test_confidence_is_float(self, mock_client):
        """Confidence must always be a float, never a string."""
        mock_response = MagicMock()
        mock_response.text = '{"intent": "career", "confidence": 0.75}'
        mock_client.models.generate_content.return_value = mock_response

        result = classify_intent("I'm preparing for a job interview")
        self.assertIsInstance(result["confidence"], float)


if __name__ == "__main__":
    unittest.main()
