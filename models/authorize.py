from . import db


class Authorization(db.Model):
  __tablename__='authorization'
  Email=db.Column(db.String, db.ForeignKey("users.Email"), nullable=False, primary_key=True)

  def to_dict(self):
    return {
      'email':self.Email
    }