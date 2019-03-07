import unittest
from app import app, db
from app.models import User, Post
from datetime import datetime, timedelta


class UserModelCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='eugene')
        u.set_password('cat')

        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='eugene', email='eugene@ex.com')

        self.assertEqual(u.get_avatar(128), (
            'https://www.gravatar.com/avatar/52110e8b4360a9954730b7e58efe9b5e?s=128&d=identicon'))

    def test_follow(self):
        u1 = User(username='john', email='john@ex.com')
        u2 = User(username='susan', email='susan@ex.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()

        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='john', email='john@ex.com')
        u2 = User(username='susan', email='susan@ex.com')
        u3 = User(username='mary', email='mary@ex.com')
        u4 = User(username='david', email='david@ex.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()

        p1 = Post(title='John says', body="Post from John", author=u1,
                  pub_date=now + timedelta(seconds=1))
        p2 = Post(title='Susan says', body="Post from Susan", author=u2,
                  pub_date=now + timedelta(seconds=4))
        p3 = Post(title='Mary says', body="Post from Mary", author=u3,
                  pub_date=now + timedelta(seconds=3))
        p4 = Post(title='David says', body="Post from David", author=u4,
                  pub_date=now + timedelta(seconds=2))

        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # John follows Susan
        u1.follow(u4)  # John follows David
        u2.follow(u3)  # Susan follows Mary
        u3.follow(u4)  # Mary follows David

        db.session.commit()

        # check the followed post for each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()

        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
