from . import db

class SaleItems(db.Model):
  __tablename__='sale_items'
  SaleItem_ID=db.Column(db.Integer, primary_key=True, autoincrement=True)
  Sale_ID=db.Column(db.Integer, db.ForeignKey('sales.Sale_ID'), nullable=False)
  P_ID=db.Column(db.Integer, db.ForeignKey('products.P_ID'), nullable=False)
  QuantitySold=db.Column(db.Integer, nullable=False)
  UnitPrice=db.Column(db.Float, nullable=False)
  def to_dict(self):
    return {
      'purchasedItemID':self.SaleItem_ID,
      'saleID':self.Sale_ID,
      'productID':self.P_ID,
      'quantitySold':self.QuantitySold,
      'unitPrice':self.UnitPrice
    }