import unittest
from app.main import create_app
# from app.extensions import mdb
from app.models.models_mdb import *


class MdbBasicTestCases(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

  
    def test_insert_objects(self):

        uf = UserForum(email="email_test", first_name="fn_test", last_name="ln_test")
        uf.save() 


        fc = ForumContent(text="test text...", lang="US")

        fp = ForumPost(title="titlex", author="authorx", tags=("tag1","tag2"), content=fc)
        fp.save() 

