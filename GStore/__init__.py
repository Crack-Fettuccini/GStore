import re
import os
import redis
from celery import Celery
from functools import wraps
from flask import Flask
from datetime import datetime, timedelta
from flask_mail import Mail
from flask_caching import Cache
from pytz import timezone
from flask_cors import CORS
from models import db, Users
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity, create_access_token,set_access_cookies
from flask_jwt_extended import verify_jwt_in_request, current_user

current_dir = os.path.abspath(os.path.dirname(__file__))
IST = timezone('Asia/Kolkata')
app = Flask(__name__,template_folder='.', static_folder=".")
instance_path = app.instance_path

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(current_dir,"instance/GStoreDB.sqlite3")
app.config["SECRET_KEY"]=os.environ['signed_cookie']

app.config["JWT_SECRET_KEY"] = os.environ['signed_cookie']
app.config["JWT_COOKIE_SECURE"] = bool(True)
app.config["JWT_COOKIE_CSRF_PROTECT"]=bool(True)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1) #preferable set it to minutes=30 just check if it is possible to use jwt using cookies
app.config["JWT_TOKEN_LOCATION"]=["headers", "cookies", "json", "query_string"]
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379"
app.config['result_backend'] = 'redis://localhost:6379'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

db.init_app(app)
app.app_context().push()
with app.app_context():
    db.create_all()
jwt = JWTManager(app)
bcrypt=Bcrypt(app)
mail = Mail(app)
api = Api(app)

cache=Cache(config={'CACHE_TYPE':"RedisCache", 'CACHE_REDIS_HOST':"127.0.0.1", 'CACHE_REDIS_PORT':"6379"})
cache.init_app(app)
CORS(app, supports_credentials=True, origins="*")
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)
celery.conf.update(
    broker_connection_retry_on_startup=True
)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


IST = timezone('Asia/Kolkata')
eregex=re.compile("^[^\s@]+@[^\s@]+\.[^\s@]+$")
pregex=re.compile("^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$")

@jwt.user_identity_loader
def user_identity_lookup(user):
  return user.User_ID

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
  User_ID = jwt_data["sub"]
  return Users.query.get(int(User_ID))

@app.after_request
def refresh_expiring_jwts(response):
  try:
    exp_timestamp = get_jwt()["exp"]
    now = datetime.utcnow()
    target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
    if target_timestamp > exp_timestamp:
      access_token = create_access_token(identity=get_jwt_identity())
      set_access_cookies(response, access_token)
    current_user.updateActivity()
    return response
  except (RuntimeError, KeyError):
    return response # Case where there is not a valid JWT. Just return the original response

def admin_required():
  def wrapper(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
      verify_jwt_in_request()
      if current_user.Level=="A":
        return fn(*args, **kwargs)
      else:
        return {"msg":"Admins only"}, 403
    return decorator
  return wrapper

def manager_required():
  def wrapper(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
      verify_jwt_in_request()
      if current_user.Level in ["M","A"]:
        return fn(*args, **kwargs)
      else:
        return {"msg":"Managers and admins only"}, 403
    return decorator
  return wrapper

jwt_redis_blocklist = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
  jti = jwt_payload["jti"]
  token_in_redis = jwt_redis_blocklist.get(jti)
  return token_in_redis is not None
