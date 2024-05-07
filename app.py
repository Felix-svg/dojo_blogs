from config import api, app, db, jwt
from models import User, Blog, Comment
from flask import session, make_response, jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


class Home(Resource):
    def get(self):
        return jsonify({"message": "DOJO Blogs"})


api.add_resource(Home, "/")


class Signup(Resource):
    def post(self):
        try:
            first_name = request.get_json()['first_name']
            last_name = request.get_json()['last_name']
            email = request.get_json()['email']
            password = request.get_json()['password']
        except KeyError:
            return make_response({"error": "User details not provided"}, 400)

        user = User.query.filter_by(email=email).first()

        if user:
            return {'message': "User Already Exists"}, 400

        if first_name and last_name and email and password:
            new_user = User(first_name=first_name, last_name=last_name, email=email)
            new_user.password_hash = password

            db.session.add(new_user)
            db.session.commit()

            access_token = create_access_token(identity=new_user.id)

            return {
                'message': "User Registration Success",
                'access_token': access_token
            }, 201

        return make_response({'error': '422 Unprocessable Entity'}, 422)


api.add_resource(Signup, "/signup")


class Login(Resource):
    def post(self):
        try:
            email = request.get_json()['email']
            password = request.get_json()['password']
        except KeyError:
            return make_response({"error": "Email or password not provided"}, 400)

        user = User.query.filter(User.email == email).first()
        if user and user.authenticate(password):
            access_token = create_access_token(identity=user.id)
            return {
                'message': "User Login Success",
                'access_token': access_token
            }, 200

        else:
            return make_response({"error": "Invalid username or password"}, 401)


api.add_resource(Login, "/login")


# class CheckSession(Resource):
#     def get(self):
#         if session.get('user_id'):
#             user = User.query.filter(User.id == session['user_id']).first()
#             return user.to_dict(only=['id', 'email']), 200
#         return {'error': '401 Resource not found'}, 401
#
#
# api.add_resource(CheckSession, "/check_session")
#
#
# class Logout(Resource):
#     def delete(self):
#         if session.get('user_id'):
#             session.pop("user_id")
#             return {}, 204
#         else:
#             return {'error': '401 Unauthorized'}, 401
#
#
# api.add_resource(Logout, "/logout")


class Users(Resource):
    #@jwt_required()
    def get(self):
        # current_user_id = get_jwt_identity()
        # if not current_user_id:
        #     return make_response({"error": "User not authenticated"}, 401)

        try:
            users = []
            for user in User.query.all():
                users.append(user.to_dict(rules=['-blogs', '-_password_hash']))
            return make_response({"users": users}, 200)
        except Exception as e:
            return make_response({"error": str(e)}, 500)


api.add_resource(Users, "/users")


class UserByID(Resource):
    def get(self, id):
        user = User.query.filter(User.id == id).first()

        if user:
            response = user.to_dict(rules=['-blogs', '-_password_hash'])
            return make_response({"user": response}, 200)
        else:
            return make_response({"error": "User not found"}, 401)

    @jwt_required()
    def delete(self, id):
        user = User.query.filter(User.id == id).first()

        if user:
            db.session.delete(user)
            db.session.commit()

            return make_response({"message": "User deleted successfully"})

        return make_response({"error": "User does not exist"})


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

    @jwt_required()
    def patch(self, id):
        blog = Blog.query.filter(Blog.id == id).first()

        for attr in request.json():
            setattr(blog, attr, request.json[attr])
        db.session.add(blog)
        db.session.commit()

        response = blog.to_dict(rules=['-user', '-comments'])
        return make_response({"blog": response}, 200)

    @jwt_required()
    def delete(self, id):
        blog = Blog.query.filter(Blog.id == id).first()

        if blog:
            db.session.delete(blog)
            db.session.commit()

            return make_response({"message": "Blog deleted successfully"})
        return make_response({"error": "Blog does not exist"})


api.add_resource(BlogByID, "/blogs/<int:id>")


class Comments(Resource):
    @jwt_required()
    def get(self):
        comments = []

        for comment in Comment.query.all():
            comments.append(comment.to_dict(rules=['-blog']))
        return make_response({"comments": comments}, 200)


api.add_resource(Comments, "/comments")


class CommentByID(Resource):
    @jwt_required()
    def get(self, id):
        comment = Comment.query.filter_by(id=id).first()

        if comment:
            response = comment.to_dict(rules=['-blog'])
            return make_response({"comment": response}, 200)
        else:
            return make_response({"error": "Comment not found"}, 401)

    @jwt_required()
    def delete(self, id):
        comment = Comment.query.filter(Comment.id == id).first()

        if comment:
            db.session.delete(comment)
            db.session.commit()

            return make_response({"message": "Comment deleted successfully"})
        return make_response({"error": "Comment not found"})


api.add_resource(CommentByID, "/comments/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
