import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_analyzer import AIAnalyzer
import unittest

class TestAI(unittest.TestCase):

    def setUp(self):
        self.ai = AIAnalyzer(os.environ.get('GENAI_KEY'))