from flask import Blueprint, request, jsonify
from .models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


user_routes = Blueprint('user', __name__)

@user_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(
        username = data['username'],
        email = data['email'],
    )
   
    try:
        new_user.set_password(data['password'])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    # user = User(username=username, email=email)
    # user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200

@user_routes.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"username": user.username, "email": user.email}), 200


# @author_routes.route('/blog', methods=['POST'])
# @jwt_required()
# def create_blog():
#     user_id = get_jwt_identity()
#     data = request.get_json()
#     title = data.get('title')
#     content = data.get('content')
#     image = data.get('image')  # Assuming this is a URL or base64 string

#     if not title or not content:
#         return jsonify({"error": "Title and content are required"}), 400

#     new_blog = Blog(title=title, content=content, image=image, author_id=user_id)
#     db.session.add(new_blog)
#     db.session.commit()

#     return jsonify({"message": "Blog created successfully", "blog_id": new_blog.id}), 201

# @author_routes.route('/blog/<int:blog_id>', methods=['PUT'])
# @jwt_required()
# def update_blog(blog_id):
#     user_id = get_jwt_identity()
#     blog = Blog.query.get(blog_id)
    
#     if not blog or blog.author_id != user_id:
#         return jsonify({"error": "Blog not found or unauthorized"}), 404
    
#     data = request.get_json()
#     blog.title = data.get('title', blog.title)
#     blog.content = data.get('content', blog.content)
#     blog.image = data.get('image', blog.image)
    
#     db.session.commit()
#     return jsonify({"message": "Blog updated successfully"}), 200

# @author_routes.route('/blog/<int:blog_id>', methods=['DELETE'])
# @jwt_required()
# def delete_blog(blog_id):
#     user_id = get_jwt_identity()
#     blog = Blog.query.get(blog_id)
    
#     if not blog or blog.author_id != user_id:
#         return jsonify({"error": "Blog not found or unauthorized"}), 404
    
#     db.session.delete(blog)
#     db.session.commit()
#     return jsonify({"message": "Blog deleted successfully"}), 200

