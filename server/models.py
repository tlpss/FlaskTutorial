from server import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


# N-M relation
# as an association table because there is nothing else then the FK's
# reference of a column is like : followers.c.<column> where c is a property of SQL Alchemy
followers = db.Table('followers',
                    db.Column('follower_id',db.Integer, db.ForeignKey('user.id')),
                    db.Column('followed_id',db.Integer, db.ForeignKey('user.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic') # 'Post'= reference to a class not yet created
    # posts not in DB scheme, just convenient to access all items in a 1-N relation
    # (actually gathered by running the query)
    about_me = db.Column(db.String(256), nullable=True)
    last_seen  =db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    # in above : UserClass is Left table, and is (primary) joined on userID to select all entries
    #          : secondary explaines how te right-hand relation is formed (how all followers are gathered)
    #          : result is a list of all Users, followed by this specific user
    #          : backref -> how is this relation accessed from the right -side
    #          :(ie how can you get all followers for a user)
    #          : lazy -> how/when is query executed
    #          : options -> DYNAMIC (equivalent) = query is executed at runtime -> allows filters etc
    #          :         -> SELECT, JOINED, SUBQUERY



    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return  f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'



    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
                 followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        # returns all followed and own posts
        followed_posts= Post.query.join(followers,
                (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own_posts = Post.query.filter_by(user_id=self.id)
        return own_posts.union(followed_posts).order_by(Post.timestamp.desc())
        #return (followed_posts.union(own_posts)).order_by(Post.timestamp.desc())

    #TODO: figure out how to filter before joining -> faster query!!

# connection between DB and flask-login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f'<post {self.body} >'


