from app.extensions import mdb


class UserForum(mdb.Document):
    email = mdb.StringField(required=True)
    first_name = mdb.StringField(max_length=50)
    last_name = mdb.StringField(max_length=50)


class ForumContent(mdb.EmbeddedDocument):
    text = mdb.StringField()
    lang = mdb.StringField(max_length=3)


class ForumPost(mdb.Document):
    title = mdb.StringField(max_length=120, required=True)
    author = mdb.ReferenceField(UserForum)
    tags = mdb.ListField(mdb.StringField(max_length=30))
    content = mdb.EmbeddedDocumentField(ForumContent)
