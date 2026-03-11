"""Tests for prompts.py — verifies structure and content of expert prompts."""

import unittest
from prompts import PROMPTS


class TestPrompts(unittest.TestCase):
    """Ensure all required expert prompts are present and well-formed."""

    REQUIRED_INTENTS = ["code", "data", "writing", "career"]

    def test_all_required_intents_exist(self):
        for intent in self.REQUIRED_INTENTS:
            self.assertIn(intent, PROMPTS, f"Missing prompt for intent: {intent}")

    def test_at_least_four_prompts(self):
        self.assertGreaterEqual(len(PROMPTS), 4)

    def test_prompts_are_non_empty_strings(self):
        for intent, prompt in PROMPTS.items():
            self.assertIsInstance(prompt, str, f"Prompt for '{intent}' is not a string")
            self.assertTrue(len(prompt.strip()) > 50, f"Prompt for '{intent}' is too short")

    def test_each_prompt_is_distinct(self):
        values = list(PROMPTS.values())
        self.assertEqual(len(values), len(set(values)), "Duplicate prompts detected")


if __name__ == "__main__":
    unittest.main()
