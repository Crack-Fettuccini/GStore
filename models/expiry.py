from . import db
from sqlalchemy import CheckConstraint


class Expiry(db.Model):
  __tablename__='expiry'
  S_ID=db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
  P_ID=db.Column(db.Integer, db.ForeignKey('products.P_ID'), nullable=False)
  Qty=db.Column(db.Integer, nullable=False)
  expiryDate = db.Column(db.DateTime, nullable=False)

  def to_dict(self):
    return {
      'Stock_ID':self.S_ID,
      'Product_ID':self.P_ID,
      'Quantity':self.Qty,
      'ExpiryDate':self.ExpiryDate,
    }