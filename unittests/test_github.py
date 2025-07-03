import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from github_client import GitHubClient
import unittest

class TestGitHub(unittest.TestCase):

    def setUp(self):
        self.gh = GitHubClient()
