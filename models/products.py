from . import db
from sqlalchemy import CheckConstraint


class Products(db.Model):
  __tablename__='products'
  P_ID=db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
  PName=db.Column(db.String, nullable=False)
  Qty=db.Column(db.Integer, nullable=False)
  PdtShot=db.Column(db.String)
  Category=db.Column(db.String, db.ForeignKey("categories.Category"), nullable=False)
  PPU=db.Column(db.Integer, nullable=False)
  Units=db.Column(db.String, nullable=False)
  __table_args__=(
    CheckConstraint(Units.in_(("g", "ml", "packs")), name="chk_units"),
  )

  def to_dict(self):
    return {
      'productID':self.P_ID,
      'productName':self.PName,
      'availableStock':self.Qty,
      'productImage':self.PdtShot,
      'category':self.Category,
      'pricePerUnit':self.PPU,
      'Unit':self.Units
    }