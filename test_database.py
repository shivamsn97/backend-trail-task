import unittest
from datetime import datetime, timedelta
from database import InMemoryDB, Submission

class TestInMemoryDB(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDB()
        self.submission1 = ("Test Title 1", "Test Author 1", "Test Text 1", "http://testurl1.com", "Test User 1")
        self.submission2 = ("Test Title 2", "Test Author 2", "Test Text 2", "http://testurl2.com", "Test User 2")
        self.submission3 = ("Test Title 3", "Test Author 3", "Test Text 3", "http://testurl3.com", "Test User 3")
        self.db.add_submission(*self.submission1)
        self.db.add_submission(*self.submission2)
        self.db.add_submission(*self.submission3)

    def test_add_submission(self):
        submission4 = ("Test Title 4", "Test Author 4", "Test Text 4", "http://testurl4.com", "Test User 4")
        self.db.add_submission(*submission4)
        self.assertEqual(self.db.submissions[0].title, submission4[0])

    def test_search_submissions(self):
        results = self.db.search_submissions(title="Test Title 1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, self.submission1[1])

        results = self.db.search_submissions(author="Test Author 2")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, self.submission2[0])

        results = self.db.search_submissions(title="Test Title", author="Test Author")
        self.assertEqual(len(results), 3)

    def test_get_submission(self):
        submission = self.db.submissions[2]
        result = self.db.get_submission(submission.id)
        self.assertEqual(result, submission)

if __name__ == '__main__':
    unittest.main()