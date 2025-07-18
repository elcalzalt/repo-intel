import sys
import os
import base64
from unittest.mock import patch, Mock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from github_client import GitHubClient
import unittest

class TestGitHub(unittest.TestCase):

    def setUp(self):
        self.gh = GitHubClient()
    
    @patch('github_client.requests.get')
    def test_get_readme_success(self, mock_get):
        # Mock successful response with base64 content
        encoded = base64.b64encode(b'some readme').decode('utf-8')
        mock_resp = Mock(status_code=200)
        mock_resp.json.return_value = {'content': encoded}
        mock_get.return_value = mock_resp

        result = self.gh.get_readme('http://api.example.com')
        self.assertEqual(result, 'some readme')

    @patch('github_client.requests.get')
    def test_get_readme_failure(self, mock_get):
        mock_get.return_value = Mock(status_code=404)
        result = self.gh.get_readme('http://api.example.com')
        self.assertIsNone(result)

    @patch('github_client.requests.get')
    def test_get_latest_commit_with_patches(self, mock_get):
        # Mock commit data with patches
        files = [{'patch': 'patch1'}, {'patch': 'patch2'}]
        mock_commit = {'commit': {'message': 'msg'}, 'files': files}
        mock_get.return_value = Mock(status_code=200, json=Mock(return_value=mock_commit))

        msg, patches = self.gh.get_latest_commit('url', 'main')
        self.assertEqual(msg, 'msg')
        self.assertEqual(patches, ['patch1', 'patch2'])

    @patch('github_client.requests.get')
    def test_get_latest_commit_no_patches(self, mock_get):
        # Mock commit with empty files list
        mock_commit = {'commit': {'message': 'msg'}, 'files': []}
        mock_get.return_value = Mock(status_code=200, json=Mock(return_value=mock_commit))

        msg, patches = self.gh.get_latest_commit('url', 'main')
        self.assertEqual(msg, 'msg')
        self.assertIsNone(patches)

    def test_get_open_issues_no_issues(self):
        # When has_issues is False should return None
        result = self.gh.get_open_issues('url', False)
        self.assertIsNone(result)

    @patch('github_client.requests.get')
    def test_get_open_issues_success(self, mock_get):
        issues = [{'title': 't1', 'body': 'b1', 'created_at': 'd1'}]
        mock_resp = Mock(status_code=200)
        mock_resp.json.return_value = issues
        mock_get.return_value = mock_resp

        result = self.gh.get_open_issues('url', True)
        self.assertEqual(result, [('t1', 'b1', 'd1')])

    @patch('github_client.GitHubClient.get_readme')
    @patch('github_client.GitHubClient.get_latest_commit')
    @patch('github_client.GitHubClient.get_open_issues')
    @patch('github_client.requests.get')
    def test_get_repo_info(self, mock_get, mock_open, mock_commit, mock_readme):
        # Mock initial repo info response
        repo_data = {'full_name': 'r', 'description': 'd', 'default_branch': 'main', 'has_issues': True}
        mock_get.return_value = Mock(status_code=200, json=Mock(return_value=repo_data))
        mock_readme.return_value = 'rd'
        mock_commit.return_value = ('cm', ['p'])
        mock_open.return_value = [('i', 'b', 'c')]

        result = self.gh.get_repo_info('owner/repo')
        self.assertEqual(result, ('r', 'd', 'rd', ('cm', ['p']), [('i', 'b', 'c')]))

    @patch('github_client.requests.get')
    def test_get_repo_info_failure(self, mock_get):
        mock_get.return_value = Mock(status_code=500)
        code = self.gh.get_repo_info('owner/repo')
        self.assertEqual(code, 500)

    @patch('github_client.requests.get')
    def test_get_file_contents(self, mock_get):
        # Mock file content
        content = base64.b64encode(b'data').decode('utf-8')
        mock_resp = Mock(status_code=200)
        mock_resp.json.return_value = {'type': 'file', 'content': content}
        mock_get.return_value = mock_resp
        result = self.gh.get_file_contents('owner/repo', 'path')
        self.assertEqual(result, 'data')

    @patch('github_client.requests.get')
    def test_get_file_contents_directory(self, mock_get):
        # JSON list indicates directory
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = []
        result = self.gh.get_file_contents('owner/repo', 'path')
        self.assertFalse(result)

    @patch('github_client.requests.get')
    def test_get_file_contents_non_file(self, mock_get):
        # type not file
        mock_resp = Mock(status_code=200)
        mock_resp.json.return_value = {'type': 'dir'}
        mock_get.return_value = mock_resp
        result = self.gh.get_file_contents('owner/repo', 'path')
        self.assertFalse(result)

    @patch('github_client.requests.get')
    def test_get_file_contents_failure(self, mock_get):
        mock_get.return_value = Mock(status_code=404)
        result = self.gh.get_file_contents('owner/repo', 'path')
        self.assertEqual(result, 404)

    @patch('github_client.requests.get')
    def test_get_update_date(self, mock_get):
        mock_resp = Mock(status_code=200)
        mock_resp.json.return_value = {'updated_at': 'time'}
        mock_get.return_value = mock_resp
        result = self.gh.get_update_date('owner/repo')
        self.assertEqual(result, 'time')

    @patch('github_client.requests.get')
    def test_get_update_date_failure(self, mock_get):
        mock_get.return_value = Mock(status_code=500)
        result = self.gh.get_update_date('owner/repo')
        self.assertEqual(result, 500)

    @patch('github_client.requests.get')
    def test_get_directory(self, mock_get):
        data = [{'a':1}]
        mock_resp = Mock(status_code=200)
        mock_resp.json.return_value = data
        mock_get.return_value = mock_resp
        result = self.gh.get_directory('owner/repo', 'path')
        self.assertEqual(result, data)

    @patch('github_client.requests.get')
    def test_get_directory_failure(self, mock_get):
        mock_get.return_value = Mock(status_code=404)
        result = self.gh.get_directory('owner/repo', 'path')
        self.assertEqual(result, 404)

if __name__ == '__main__':
    unittest.main()
