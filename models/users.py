from . import db
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint

class Users(db.Model):
  __tablename__='users'
  User_ID=db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
  Username=db.Column(db.String, nullable=False)
  Email=db.Column(db.String, unique=True, nullable=False)
  Password=db.Column(db.String, nullable=False)
  Level=db.Column(db.CHAR, nullable=False)
  LastActive=db.Column(db.DateTime, nullable=False, onupdate=func.now())
  __table_args__=(
    CheckConstraint(Level.in_(("U", "M", "A")), name="chk_level"),
  )
  def to_dict(self):
    return {
      'userID':self.User_ID,
      'username':self.Username,
      'email':self.Email,
      'Password':"Redacted",
      'level':self.Level,
    }
  
  def updateActivity(self):
    self.LastActive = func.now()
    db.session.commit()