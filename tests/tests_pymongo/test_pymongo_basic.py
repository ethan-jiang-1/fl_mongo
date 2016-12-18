import unittest
from app.main import create_app
from app.extensions import mongo


class MongoBasicTestCases(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()        
        self.mdb = mongo.db
        
        self.mdb.tsc.remove()
        self.tsc = self.mdb.tsc

    def tearDown(self):
        self.app_context.pop()

    def test_insert_one(self):

        self.assertEquals(self.tsc.count(),0)
        
        post = {"author": "Mike", "text": "hello mike"}

        ret1 = self.tsc.insert_one(post)
        rec_id = ret1.inserted_id

        ret2 = self.tsc.find_one()
        rec_id_find = ret2["_id"]

        self.assertEquals(self.tsc.count(),1)
        self.assertEquals(rec_id,rec_id_find)


    def test_update_add_field(self):

        self.assertEquals(self.tsc.count(),0)

        post = {"author": "Mike", "text": "hello mike"}
        self.tsc.insert_one(post)

        post_find = self.tsc.find_one() 
        self.assertTrue("author" in post_find)
        self.assertTrue("text" in post_find)
        self.assertFalse("comment" in post_find)

        post_query = {"author": "Mike"}
        post_new = {"author": "Mike", "text": "hello mike", "comment": "comment ok"}
        self.tsc.update(post_query,post_new)

        post_find = self.tsc.find_one() 
        self.assertTrue("author" in post_find)
        self.assertTrue("text" in post_find)
        self.assertTrue("comment" in post_find)

    def test_update_change_field(self):

        self.assertEquals(self.tsc.count(),0)

        post = {"name": "joe", "friends": 32, "enimies":2 }
        self.tsc.insert_one(post)

        post_find = self.tsc.find_one()
        self.assertTrue("name" in post_find)
        self.assertTrue("friends" in post_find)
        self.assertTrue("enimies" in post_find)

        post_find["relationships"] = {"friends": 32, "enimies":2 }
        post_find.pop("friends")
        post_find.pop("enimies")

        self.tsc.update({"name":"joe"}, post_find)

        post_find_new = self.tsc.find_one()
        self.assertTrue("name" in post_find_new)
        self.assertFalse("friends" in post_find_new)
        self.assertFalse("enimies" in post_find_new)
        self.assertTrue("relationships" in post_find_new)
        self.assertTrue("friends" in post_find_new["relationships"])
        self.assertTrue("enimies" in post_find_new["relationships"])


    def test_update_change_field_by_id(self):
        self.assertEquals(self.tsc.count(),0)

        post = {"name": "joe", "friends": 32, "enimies":2 }
        self.tsc.insert_one(post)

        post_find = self.tsc.find_one()
        self.assertTrue("name" in post_find)
        self.assertTrue("friends" in post_find)
        self.assertTrue("enimies" in post_find)

        post_find["relationships"] = {"friends": 32, "enimies":2 }
        post_find.pop("friends")
        post_find.pop("enimies")

        self.tsc.update({"_id":post_find["_id"]}, post_find)

        post_find_new = self.tsc.find_one()
        self.assertTrue("name" in post_find_new)
        self.assertFalse("friends" in post_find_new)
        self.assertFalse("enimies" in post_find_new)
        self.assertTrue("relationships" in post_find_new)
        self.assertTrue("friends" in post_find_new["relationships"])
        self.assertTrue("enimies" in post_find_new["relationships"])

    def test_find_multiple_post(self):
        self.assertEquals(self.tsc.count(),0)

        post1 = {"name": "joe", "friends": 32, "enimies":2 }
        self.tsc.insert_one(post1)
        post2 = {"name": "joe", "friends": 32, "enimies":2 }
        self.tsc.insert_one(post2)

        self.assertEquals(self.tsc.count(),2)

        posts = self.tsc.find() 

        self.assertEquals(posts.count(), 2)
        self.assertTrue("name" in posts[0])
        self.assertTrue("name" in posts[1])

        self.assertNotEquals(posts[0], posts[1])
        self.assertNotEquals(posts[0]["_id"], posts[1]["_id"])
        self.assertEquals(posts[0]["name"], posts[1]["name"])
        self.assertEquals(posts[0]["friends"], posts[1]["friends"])


    def test_op_inc(self):
        self.assertEquals(self.tsc.count(),0)

        pageview = {"url": "www.mysite.com", "pageviews": 10}
        self.tsc.insert_one(pageview)

        pageview_find = self.tsc.find_one()
        self.tsc.update({"_id": pageview_find["_id"]}, {"$inc": {"pageviews":1}})

        pageview_find = self.tsc.find_one()
        self.assertEquals(pageview_find["pageviews"],11)


        self.tsc.update({"_id": pageview_find["_id"]}, {"$inc": {"pageviews":1}})
        self.tsc.update({"_id": pageview_find["_id"]}, {"$inc": {"pageviews":1}})
        self.tsc.update({"_id": pageview_find["_id"]}, {"$inc": {"pageviews":1}})

        pageview_find = self.tsc.find_one()
        self.assertEquals(pageview_find["pageviews"],14)
