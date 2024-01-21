from . import db
from sqlalchemy.sql import func
from datetime import timedelta
class Sales(db.Model):
  __tablename__ = 'sales'
  Sale_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
  User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
  SaleDate = db.Column(db.DateTime, nullable=False, default=func.now())
  TotalAmount = db.Column(db.Float, nullable=False)

  def to_dict(self):
    return {
      'saleID' : self.Sale_ID,
      'userID' : self.User_ID,
      'saleDate' : self.SaleDate.isoformat(),
      'totalAmount' : self.TotalAmount,
    }
  
  def can_be_deleted(self):
        time_difference = func.now() - self.SaleDate
        one_day = timedelta(days=1)
        return time_difference <= one_day