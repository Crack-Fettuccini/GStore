import re
from flask import jsonify
from models import db, Users
from sqlalchemy.sql import func
from flask_restful import Resource, reqparse
from .. import bcrypt, eregex, pregex, jwt_redis_blocklist, app
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies, get_jwt
from flask_jwt_extended import create_access_token, jwt_required, current_user

class TestNode(Resource):
  def get(self):
    return "Hello World"
  
class RefreshJWTToken(Resource):
  @jwt_required()
  def get(self):
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=app.config["JWT_ACCESS_TOKEN_EXPIRES"])
    response = jsonify({"msg" : "Access token revoked"})
    unset_jwt_cookies(response)
    user = db.session.query(Users).filter_by(Email=current_user.Email).first()
    access_token = create_access_token(identity=user)
    response = jsonify({"accessToken":access_token, "userLevel":user.Level})
    set_access_cookies(response, access_token)
    user.updateActivity()
    return response

class Register(Resource):
  def post(self):
    credentials = reqparse.RequestParser()
    credentials.add_argument("email", type=str, help="Your email", required=True)
    credentials.add_argument("password", type=str, help="Password associated with this email id", required=True)
    credentials.add_argument("passwordCheck", type=str, help="Password associated with this email id", required=True)
    [Email, Password, RePassword] = credentials.parse_args().values()
    if Email != None and Password != None and RePassword != None:
      Email = Email.lower()
      if re.fullmatch(eregex,Email):
        if not db.session.query(Users).filter_by(Email=Email).first():
          if re.fullmatch(pregex,Password):
            if Password == RePassword:
              password=bcrypt.generate_password_hash(Password)
              new_user=Users(Username = Email.split('@')[0], Email = Email, Password = password, Level = "U", LastActive = func.now()
)
              db.session.add(new_user)
              db.session.commit()
              user = db.session.query(Users).filter_by(Email=Email).first()
              access_token = create_access_token(identity=user)
              response = jsonify({"access_token":access_token})
              set_access_cookies(response, access_token)
              user.updateActivity()
              return response
            else:
              return {'msg':'Passwords do not match.'}, 400
          else:
            return {'msg':'Email is already bound to an account.'},403
        else:
          return {'msg':'Password should contain atleast 8 characters, one digit, one capital and one small letter.'},422

      else:
        return {'msg':'Enter a valid email.'},422
    else:
      return {'msg':'Enter email/password/confimation-password.'},422

class Login(Resource):

  def post(self):
    credentials = reqparse.RequestParser()
    credentials.add_argument("email", type=str, help="Your email")
    credentials.add_argument("password", type=str, help="Password associated with this email id")
    [Email, Password] = credentials.parse_args().values()
    if Email != None and Password != None:
      if re.fullmatch(eregex,Email):
        Email = Email.lower()
        if re.fullmatch(pregex,Password):
          user=db.session.query(Users).filter_by(Email = Email).first()
          if user:
            if bcrypt.check_password_hash(user.Password,Password):
              access_token = create_access_token(identity=user)
              response = jsonify({"accessToken":access_token, "userLevel":user.Level})
              set_access_cookies(response, access_token)
              user.updateActivity()
              return response
            else:
              return {'msg':'Incorrect username or password.'}, 401
          else:
            return {'msg':'User does not exist, please sign up.'},404
        else:
          return {'msg':'Password should contain atleast 8 characters, one digit, one capital and one small letter.'},422
      else:
        return {'msg':'Enter a valid email.'},422
    else:
      return {'msg':'Enter email/password.'},422
    
class Logout(Resource):
  @jwt_required()
  def delete(self):
    user = db.session.query(Users).filter_by(Email=current_user.Email).first()
    user.updateActivity()
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=app.config["JWT_ACCESS_TOKEN_EXPIRES"])
    response = jsonify({"msg" : "Access token revoked"})
    unset_jwt_cookies(response)
    return {"msg" : "Access token revoked"}

class EditProfile(Resource):
  @jwt_required()
  def get(self):
    return {"username":current_user.Username,"email":current_user.Email}, 200

  @jwt_required()
  def patch(self):
    credentials = reqparse.RequestParser()
    credentials.add_argument("username", type=str, help="Your email")
    credentials.add_argument("email", type=str, help="Your email")
    credentials.add_argument("currentPassword", type=str, help="Current password used")
    credentials.add_argument("newPassword", type=str, help="Password associated with this email id")
    #credentials.add_argument("newPasswordCheck", type=str, help="Password associated with this email id")
    [Username, Email,CurrentPassword, NewPassword] = credentials.parse_args().values()
    user=db.session.query(Users).filter_by(User_ID=current_user.User_ID).first()
    
    if Username:
      if Username!="":
        user.Username=Username
        db.session.commit()
        return {'msg': f"Username changed to {user.Username}"},200
      else:
        return {'msg':'Username cannot be empty string'},400
      
    if Email:
      Email=Email.lower()
      if Email!="":
        if Email!=current_user.Email:
          Email = Email.lower()
          if re.search(eregex,Email):
            if not db.session.query(Users).filter_by(Email=Email).first():
              user.Email=Email
              db.session.commit()
              return {'msg': f"Email changed to {user.Email}."},200
            else:
              return {"msg":"Another account already exists with this email id."}, 403
          else:
            return {'msg':'Enter a valid email.'},422
        else:
          return {'msg':'No changes made.'},400
      else:
        return {'msg':'Email cannot be empty string.'},400

    if CurrentPassword:
      if bcrypt.check_password_hash(user.Password,CurrentPassword):
        if re.search(pregex,NewPassword):
          if CurrentPassword!=NewPassword:
            newpassword=bcrypt.generate_password_hash(NewPassword)
            user.Password=newpassword
            db.session.commit()
            return {"msg":"password changed successfully."},200
          else:
            return {"msg":"No changes made."},200
        else:
          return {'msg':'Password should contain atleast 8 characters, one digit, one capital and one small letter.'},422
      else:
        return {'msg':"Incorrect password."}, 401
    else:
      return {"msg":"No arguments passed."}, 400

"""
from . import db
from datetime import datetime


class Users(db.Model):
  __tablename__ = 'users'
  User_ID = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
  Username = db.Column(db.String, nullable=False)
  Email = db.Column(db.String, unique=True, nullable=False)
  Password = db.Column(db.String, nullable=False)
  Level = db.Column(db.CHAR, nullable=False)
  LastActive =db.Column(db.DateTime, nullable=False)
  
  def to_dict(self):
    return {
      'userID': self.User_ID,
      'username': self.Username,
      'email': self.Email,
      'Password': "Redacted",
      'level': self.Level,
      'lastlogin': self.lastActive
    }
"""