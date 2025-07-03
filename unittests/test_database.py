import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cache_db import CacheDatabase
import unittest

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = CacheDatabase()
