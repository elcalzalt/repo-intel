import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_analyzer import AIAnalyzer
import unittest
from unittest.mock import patch, Mock

class TestAI(unittest.TestCase):

    def setUp(self):
        patcher = patch('ai_analyzer.genai.Client')
        self.addCleanup(patcher.stop)
        self.mock_client = patcher.start()
        self.ai = AIAnalyzer(os.environ.get('GENAI_KEY'))
        
    @patch('ai_analyzer.genai.Client')
    def test_summarize(self, mock_client):
        mock_response = Mock()
        mock_response.text = "Test summary"
        mock_client.return_value.models.generate_content.return_value = mock_response

        repo_data = (
            "owner/repo",
            "description",
            "readme content",
            ("commit msg", ["patch1"]),
            []
        )
        result = self.ai.summarize(repo_data)
        self.assertIsNotNone(result)

    @patch('ai_analyzer.genai.Client')
    def test_scan_file(self, mock_client):
        mock_response = Mock()
        mock_response.text = "No vulnerabilities found"
        mock_client.return_value.models.generate_content.return_value = mock_response

        result = self.ai.scan_file("test.py", "print('hello')")
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
