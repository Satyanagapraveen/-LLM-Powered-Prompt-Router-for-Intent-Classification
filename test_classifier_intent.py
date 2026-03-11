"""Tests for classify_intent with the 15+ required test messages."""

import unittest
from unittest.mock import patch, MagicMock
from classifier import classify_intent


class TestClassifierIntentMessages(unittest.TestCase):
    """
    Verify classify_intent returns valid structure for each of the
    15 required test messages (using mocked LLM responses).
    """

    VALID_INTENTS = {"code", "data", "writing", "career", "unclear"}

    TEST_CASES = [
        ("how do i sort a list of objects in python?", "code"),
        ("explain this sql query for me", "data"),
        ("This paragraph sounds awkward, can you help me fix it?", "writing"),
        ("I'm preparing for a job interview, any tips?", "career"),
        ("what's the average of these numbers: 12, 45, 23, 67, 34", "data"),
        ("Help me make this better.", "unclear"),
        (
            "I need to write a function that takes a user id and returns their profile, "
            "but also i need help with my resume.",
            "unclear",
        ),
        ("hey", "unclear"),
        ("Can you write me a poem about clouds?", "unclear"),
        ("Rewrite this sentence to be more professional.", "writing"),
        ("I'm not sure what to do with my career.", "career"),
        ("what is a pivot table", "data"),
        ("fxi thsi bug pls: for i in range(10) print(i)", "code"),
        ("How do I structure a cover letter?", "career"),
        ("My boss says my writing is too verbose.", "writing"),
    ]

    @patch("classifier.client")
    def test_all_15_messages_return_valid_structure(self, mock_client):
        """Each of the 15 test messages must produce a dict with intent + confidence."""
        for message, expected_intent in self.TEST_CASES:
            mock_response = MagicMock()
            mock_response.text = (
                f'{{"intent": "{expected_intent}", "confidence": 0.9}}'
            )
            mock_client.models.generate_content.return_value = mock_response

            with self.subTest(message=message):
                result = classify_intent(message)
                self.assertIsInstance(result, dict)
                self.assertIn("intent", result)
                self.assertIn("confidence", result)
                self.assertIn(result["intent"], self.VALID_INTENTS)
                self.assertIsInstance(result["confidence"], float)
                self.assertGreaterEqual(result["confidence"], 0.0)
                self.assertLessEqual(result["confidence"], 1.0)


if __name__ == "__main__":
    unittest.main()
