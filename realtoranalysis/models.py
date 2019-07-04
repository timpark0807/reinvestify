from datetime import datetime
from realtoranalysis import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    # property = db.relationship('Property', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class AnonymousUser(AnonymousUserMixin):
    id = None  # add an id attribute to the default AnonymousUser


login_manager.anonymous_user = AnonymousUser


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default="Untitled")
    url = db.Column(db.String(250))
    street = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zipcode = db.Column(db.String(100))

    type = db.Column(db.String(100))
    year = db.Column(db.String(100))
    bed = db.Column(db.String(100))
    bath = db.Column(db.String(100))
    sqft = db.Column(db.String(100))

    price = db.Column(db.String(100))
    term = db.Column(db.String(100))
    down = db.Column(db.String(100))
    interest = db.Column(db.String(100))
    closing = db.Column(db.String(100))

    rent = db.Column(db.String(100))
    other = db.Column(db.String(100))
    expenses = db.Column(db.String(100))
    vacancy = db.Column(db.String(100))
    appreciation = db.Column(db.String(100))
    income_growth = db.Column(db.String(100))
    expense_growth = db.Column(db.String(100))

    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# db.drop_all()
# db.create_all()
#
