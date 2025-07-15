import unittest
import tempfile
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from user_manager import UserManager

class TestUserManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary database for testing
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        self.db_path = f"sqlite:///{self.test_db.name}"
        self.user_manager = UserManager(self.db_path)

    def tearDown(self):
        # Clean up the temporary database
        os.unlink(self.test_db.name)

    def test_create_user(self):
        """Test user creation"""
        result = self.user_manager.create_user("testuser", "test@example.com", "password123")
        self.assertTrue(result)
        
        # Test duplicate user creation should fail
        result = self.user_manager.create_user("testuser", "test2@example.com", "password456")
        self.assertFalse(result)

    def test_authenticate_user(self):
        """Test user authentication"""
        # Create a user first
        self.user_manager.create_user("testuser", "test@example.com", "password123")
        
        # Test correct credentials
        result = self.user_manager.authenticate_user("testuser", "password123")
        self.assertTrue(result)
        self.assertTrue(self.user_manager.is_logged_in())
        
        # Test incorrect credentials
        result = self.user_manager.authenticate_user("testuser", "wrongpassword")
        self.assertFalse(result)

    def test_logout(self):
        """Test user logout"""
        # Create and login a user
        self.user_manager.create_user("testuser", "test@example.com", "password123")
        self.user_manager.authenticate_user("testuser", "password123")
        self.assertTrue(self.user_manager.is_logged_in())
        
        # Test logout
        self.user_manager.logout()
        self.assertFalse(self.user_manager.is_logged_in())

    def test_search_history(self):
        """Test search history functionality"""
        # Create and login a user
        self.user_manager.create_user("testuser", "test@example.com", "password123")
        self.user_manager.authenticate_user("testuser", "password123")
        
        # Add search history
        result = self.user_manager.add_to_search_history("summary", "owner/repo")
        self.assertTrue(result)
        
        result = self.user_manager.add_to_search_history("vulnerability", "owner/repo", "file.py")
        self.assertTrue(result)
        
        # Get search history
        history = self.user_manager.get_search_history()
        self.assertEqual(len(history), 2)

    def test_bookmarks(self):
        """Test bookmark functionality"""
        # Create and login a user
        self.user_manager.create_user("testuser", "test@example.com", "password123")
        self.user_manager.authenticate_user("testuser", "password123")
        
        # Add bookmarks
        result = self.user_manager.add_bookmark("repo", "owner/repo", title="Test Repo")
        self.assertTrue(result)
        
        result = self.user_manager.add_bookmark("file", "owner/repo", "file.py", "Test File", "Important file")
        self.assertTrue(result)
        
        # Get bookmarks
        bookmarks = self.user_manager.get_bookmarks()
        self.assertEqual(len(bookmarks), 2)
        
        # Test duplicate bookmark should fail
        result = self.user_manager.add_bookmark("repo", "owner/repo", title="Duplicate")
        self.assertFalse(result)

    def test_unauthorized_operations(self):
        """Test that operations require login"""
        # Test search history without login
        result = self.user_manager.add_to_search_history("summary", "owner/repo")
        self.assertFalse(result)
        
        history = self.user_manager.get_search_history()
        self.assertEqual(len(history), 0)
        
        # Test bookmarks without login
        result = self.user_manager.add_bookmark("repo", "owner/repo")
        self.assertFalse(result)
        
        bookmarks = self.user_manager.get_bookmarks()
        self.assertEqual(len(bookmarks), 0)

if __name__ == '__main__':
    unittest.main()
