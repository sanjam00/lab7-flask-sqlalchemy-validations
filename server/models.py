from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        # check for presence
        if not name:
            raise ValueError("Author name must be present.")
        
				# check for duplications
        duplicate_name = db.session.query(Author.name).filter_by(name=name).first()
        if duplicate_name is not None:
            raise ValueError("Author name must be unique.")
        
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        # check phone number length
        if not isinstance(phone_number, str) or not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number must be 10 digits.")
        
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates()
    def validate_post(self, title, content, category, summary):
        pass
        # check for post content >= 250 characters

        # check for post summary <= 250 characters

        # check for post category being either fiction or non-fiction

        # check that post title has one of the following: "Won't Believe", "Secret", "Top", "Guess"

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
