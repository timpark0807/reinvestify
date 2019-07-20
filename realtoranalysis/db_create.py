from realtoranalysis import db
from realtoranalysis.models import User, Post

db.drop_all()
db.create_all()

print("DB created.")
