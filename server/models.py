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
	@validates('content', 'category', 'summary', 'title')
	def validate_post(self, key, value):

		if key == 'title':
			# check that post title has one of the following: "Won't Believe", "Secret", "Top", "Guess"
			if not value:
				raise ValueError("Title is required.")
			
			if not any(phrase in value for phrase in ["Won't Believe", "Secret", "Top", "Guess"]):
				raise ValueError("Title must be clickbait-y.")

		elif key == 'content':
			# check for post content >= 250 characters
			if value is None or len(value) < 250:
				raise ValueError("Post content must be at least 250 characters long.")

		elif key == 'summary':
			# check for post summary <= 250 characters
			if value is not None and len(value) > 250:
				raise ValueError("Post summary must be less than 250 characters.")

		elif key == 'category':
			# check for post category being either fiction or non-fiction
			if value not in ["Fiction", "Non-Fiction"]:
				raise ValueError("Category must be either Fiction or Non-Fiction.")

			return value

	def __repr__(self):
		return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
