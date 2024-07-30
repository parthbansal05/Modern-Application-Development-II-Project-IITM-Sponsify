from server_pkg.server.app import db


class User(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    ph_no = db.Column(db.String(10), nullable=False, unique=True)
    pwd = db.Column(db.String(120), nullable=False, unique=False)
    
    user_type = db.Column(db.String(2), nullable=False, unique=False)
    
    category = db.Column(db.String(100), nullable=False, unique=False)
    niche = db.Column(db.String(100), nullable=False, unique=False)
    followers = db.Column(db.Integer, nullable=False, unique=False)

    industry = db.Column(db.String(100), nullable=False, unique=False)
    budget = db.Column(db.Integer, nullable=False, unique=False)

    sponsor_approval = db.Column(db.String(10), nullable=False, unique=False, default="False")

    def __repr__(self):
        return '<User %r>' % self.username