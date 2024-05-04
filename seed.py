from models import User, Blog, Comment
from config import db, app
from faker import Faker

with app.app_context():
    print("Deleting all records")
    User.query.delete()
    Blog.query.delete()
    Comment.query.delete()

    fake = Faker()

    print("Creating users")
    user1 = User(first_name = fake.first_name(), last_name = fake.last_name(), email = fake.email())
    user1.password_hash = "1234"
    user2 = User(first_name=fake.first_name(), last_name=fake.last_name(), email=fake.email())
    user2.password_hash = "2345"
    user3 = User(first_name = fake.first_name(), last_name = fake.last_name(), email = fake.email())
    user3.password_hash = "3456"
    user4 = User(first_name = fake.first_name(), last_name = fake.last_name(), email = fake.email())
    user4.password_hash = "4567"
    user5 = User(first_name=fake.first_name(), last_name=fake.last_name(), email=fake.email())
    user5.password_hash = "5678"

    db.session.add_all([user1, user2, user3, user4, user5])
    db.session.commit()


    print("Creating blogs")
    blog1 = Blog(title = "The Art of Coding: Tips and Tricks for Beginners" ,content = "In this blog post, we'll explore some valuable tips and tricks for beginner programmers. From mastering basic syntax to understanding common programming concepts, this guide is perfect for those just starting on their coding journey.")
    blog1.user_id = 1
    blog2 = Blog(title = "Exploring the World of Machine Learning: A Beginner's Guide", content = "Dive into the fascinating world of machine learning with our beginner's guide. Learn about key concepts such as supervised and unsupervised learning, and discover how machine learning is transforming industries worldwide.")
    blog2.user_id = 2
    blog3 = Blog(title = "10 Must-Read Books for Every Programmer", content = "Looking to expand your programming knowledge? Check out our list of 10 must-read books for every programmer. From classics to new releases, these books are sure to inspire and educate.")
    blog3.user_id = 3
    blog4 = Blog(title = "Understanding React Hooks: A Comprehensive Guide", content = "React Hooks revolutionized the way we write React components. In this comprehensive guide, we'll cover everything you need to know about React Hooks, including how to use them in your projects and common pitfalls to avoid.")
    blog4.user_id = 4
    blog5 = Blog(title = "How to Build a RESTful API with Flask and SQLAlchemy", content = "Building a RESTful API is a fundamental skill for any developer. In this tutorial, we'll walk you through the process of building a RESTful API using Flask and SQLAlchemy. Learn how to create routes, handle requests, and interact with a database to build a fully functional API.")
    blog5.user_id = 5

    db.session.add_all([blog1, blog2, blog3, blog4, blog5])
    db.session.commit()

    print("Creating comments")
    comment1 = Comment(author=fake.name(), email=fake.email(), content="Great post! Really helped me understand the concept better.")
    comment1.blog_id = 1
    comment2 = Comment(author=fake.name(), email=fake.email(), content="I have a question about this part. Can you explain it further?")
    comment2.blog_id = 2
    comment3 = Comment(author=fake.name(), email=fake.email(), content="This is so useful! I'll definitely be referring back to this in the future.")
    comment3.blog_id = 3
    comment4 = Comment(author=fake.name(), email=fake.email(), content="I tried implementing this in my project and ran into some issues. Any advice?")
    comment4.blog_id = 4
    comment5 = Comment(author=fake.name(), email=fake.email(), content=" love the way you explain things. It makes complex topics seem so much simpler.")
    comment5.blog_id = 5

    db.session.add_all([comment1, comment2, comment3, comment4, comment5])
    db.session.commit()

    print("Seeding database")
    print("Seeding complete")