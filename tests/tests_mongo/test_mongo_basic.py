import unittest
from app.main import create_app
from app.extensions import mongo


class MongoBasicTestCases(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()        
        self.mdb = mongo.db

    def tearDown(self):
        self.app_context.pop()

    def test_simple(self):
        
        post = {"author":"Mike", "text":"hello mike"}

        # import ipdb; ipdb.set_trace() 

        ret1 = self.mdb.tsc.insert_one(post)

        ret2 = self.mdb.tsc.find_one()





