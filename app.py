from config import api, app
from models import User, Blog, Comment
from flask import session, make_response, jsonify
from flask_restful import Resource


class Home(Resource):
    def get(self):
        return jsonify({"message": "DOJO Blogs"})


api.add_resource(Home, "/")


class Users(Resource):
    def get(self):
        users = []

        for user in User.query.all():
            users.append(user.to_dict(rules=['-blogs', '-_password_hash']))
        return make_response({"users": users}, 200)


api.add_resource(Users, "/users")


class UserByID(Resource):
    def get(self, id):
        user = User.query.filter(User.id == id).first()

        if user:
            response = user.to_dict(rules=['-blogs', '-_password_hash'])
            return make_response({"user": response}, 200)
        else:
            return make_response({"error": "User not found"}, 401)


api.add_resource(UserByID, "/users/<int:id>")


class Blogs(Resource):
    def get(self):
        blogs = []

        for blog in Blog.query.all():
            blogs.append(blog.to_dict(rules=['-user', '-comments']))
        return make_response({"blogs": blogs}, 200)


api.add_resource(Blogs, "/blogs")


class BlogByID(Resource):
    def get(self, id):
        blog = Blog.query.filter(Blog.id == id).first()

        if blog:
            response = blog.to_dict(rules=['-user', '-comments'])
            return make_response({"blog": response}, 200)
        else:
            return make_response({"error": "Blog not found"}, 401)


api.add_resource(BlogByID, "/blogs/<int:id>")


class Comments(Resource):
    def get(self):
        comments = []

        for comment in Comment.query.all():
            comments.append(comment.to_dict(rules=['-blog']))
        return make_response({"comments": comments}, 200)


api.add_resource(Comments, "/comments")


class CommentByID(Resource):
    def get(self, id):
        comment = Comment.query.filter_by(id=id).first()

        if comment:
            response = comment.to_dict(rules=['-blog'])
            return make_response({"comment": response}, 200)
        else:
            return make_response({"error":"Comment not found"}, 401)


api.add_resource(CommentByID, "/comments/<int:id>")


if __name__ == "__main__":
    app.run(debug=True)
