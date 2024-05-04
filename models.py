from config import app, db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates


class User(db.Model, SerializerMixin):

    __tablename__ = "users"

    #serialize_rules = ("-blogs.user")

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)

    # Relationship mapping user to blogs
    blogs = db.relationship("Blog", back_populates="user")

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    @validates("email")
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("Email must include @")
        return email

    def __repr__(self):
        return f"<Name: {self.first_name} {self.last_name}, Email: {self.email}>"


class Blog(db.Model, SerializerMixin):

    __tablename__ = "blogs"

    #serialize_rules = ("-user.blogs", "-comments.blog")

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"))

    # Relationship mapping blog to a user and comment
    user = db.relationship("User", back_populates="blogs")
    comments = db.relationship("Comment", back_populates="blog")

    def __repr__(self):
        return f"<Comment {self.id}, Comment: {self.content}>"


class Comment(db.Model, SerializerMixin):

    __tablename__ = "comments"

    #serialize_rules = ("-blog.comment")

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"))

    blog = db.relationship("Blog", back_populates="comments")

    def __repr__(self):
        return f"<Comment {self.id} {self.author} {self.content}"


