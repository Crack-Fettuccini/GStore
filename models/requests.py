from . import db
from sqlalchemy import CheckConstraint


class Requests(db.Model):
  __tablename__='Requests'
  R_ID=db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
  User_ID=db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
  RTitle=db.Column(db.String, nullable=False)
  RMessage=db.Column(db.Integer, nullable=False)
  Resolution=db.Column(db.String, nullable=False)
  AdminMessage=db.Column(db.String, nullable=False)
  __table_args__=(
    CheckConstraint(Resolution.in_(("Pending", "Approved", "Rejected")), name="chk_resolution"),
  )

  def to_dict(self):
    return {
      'requestID':self.R_ID,
      'userID':self.User_ID,
      'requestTitle':self.RTitle,
      'requestMessage':self.RMessage,
      'status':self.Resolution,
      'adminMessge':self.AdminMessage,
    }