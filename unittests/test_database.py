import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cache_db import CacheDatabase
import unittest

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Use in-memory SQLite for isolation
        self.db = CacheDatabase('sqlite:///:memory:')

    def test_cache_insert_and_retrieve_summary(self):
        """Test summary_cache insert and retrieval"""
        repo = 'repo1'
        resp = 'summary result'
        tstamp = '123'
        # initially no cache
        result = self.db.get_recent_cache(repo, self.db.summary_cache, tstamp)
        self.assertEqual(result, (None, False, False))
        # insert data
        self.db.insert_data(self.db.summary_cache, {'repo_name': repo, 'response': resp, 'updated_at': tstamp})
        # same timestamp: cache hit
        response, exists, up_to_date = self.db.get_recent_cache(repo, self.db.summary_cache, tstamp)
        self.assertTrue(exists)
        self.assertTrue(up_to_date)
        self.assertEqual(response, resp)
        # different timestamp: not up to date
        response2, exists2, up_to_date2 = self.db.get_recent_cache(repo, self.db.summary_cache, '999')
        self.assertTrue(exists2)
        self.assertFalse(up_to_date2)

    def test_cache_insert_and_delete_vulnerability(self):
        """Test vulnerability_cache insert, retrieve and delete"""
        repo = 'repo2'
        file = 'file.py'
        resp = 'vuln result'
        tstamp = '321'
        fullpath = repo + file
        # insert vulnerability data
        self.db.insert_data(self.db.vulnerability_cache, {'repo_name': repo, 'file_name': file, 'response': resp, 'updated_at': tstamp, 'full_path': fullpath})
        # retrieve
        response, exists, up_to_date = self.db.get_recent_cache(repo, self.db.vulnerability_cache, tstamp, file)
        self.assertTrue(exists)
        self.assertTrue(up_to_date)
        self.assertEqual(response, resp)
        # delete entry
        self.db.delete_entry(repo, self.db.vulnerability_cache, file_path=file)
        # now should be absent
        result = self.db.get_recent_cache(repo, self.db.vulnerability_cache, tstamp, file)
        self.assertEqual(result, (None, False, False))

if __name__ == '__main__':
    unittest.main()
