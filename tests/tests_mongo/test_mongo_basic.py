import unittest
from app.main import create_app


class MongoBasicTestCases(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')

    def tearDown(self):
        pass 

    def test_simple(self):
        self.assertTrue(True)