from flask_restful import Resource, reqparse
from .. import cache, r
from models import db, Products, Sales, SaleItems, Expiry
from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timedelta
from sqlalchemy import asc

class bill(Resource):
  @jwt_required()
  def get(self):
    Saleid = reqparse.RequestParser()
    Saleid.add_argument('purchaseList', type=dict, help="List of products bought.", required=True)
    [Sale_ID] = Saleid.parse_args().values()
    if Sale_ID:
      Sale = db.session.query(Sales).get(Sale_ID)
      if Sale and Sale.User_ID==current_user.User_ID:
        items = db.session.query(SaleItems).filter_by(Sale_ID = Sale_ID).all()
        sale_items_info = [item.to_dict for item in items]
        return {'msg':sale_items_info}, 200
      else:
        return {'msg':f"Order {Sale_ID} does not exist."}, 404
    else:
      return {'msg':f"Pass Sale_ID as URL parameter to get info"}, 400
  
class purchases(Resource):
  @jwt_required()
  def get(self):
    if current_user.Level=="U":
      cache_key = f"{current_user.User_ID}//purchases"
      cached_data = cache.get(cache_key)
      if cached_data is not None:
        return {'msg': cached_data}, 200
      else:
        purchases = db.session.query(Sales).filter_by(User_ID=current_user.User_ID).all()
        Purchases_list = [purchase.to_dict() for purchase in purchases]
        cache.set(cache_key, Purchases_list, timeout=60)
    elif current_user.Level in ['A','M']:
      purchases = db.session.query(Sales).all()
    Purchases_list = [purchase.to_dict() for purchase in purchases]
    print(Purchases_list)
    return {'msg':Purchases_list}, 200
  
  @jwt_required()
  def post(self):
    New_Purchase = reqparse.RequestParser()
    New_Purchase.add_argument('purchaseList', type=dict, help="List of products bought.", required=True)
    [PurchaseList] = New_Purchase.parse_args().values()
    print(PurchaseList)
    total=0
    for productId, Qtt in PurchaseList.items():
      print(productId)
      product=db.session.query(Products).get(productId)
      if not product:
        return {'msg':'Product with product ID doesnt exist.'}, 404
      print(Qtt,product.Qty)
      if Qtt:
        if int(Qtt)<=product.Qty:
          total = total+(product.PPU)*int(Qtt)
          product.Qty = product.Qty - int(Qtt)
        else:
          db.session.rollback()
          return {'msg':f"Stock for product {product.PName} is lesser than requested purchase amount."}, 422
      else:
        db.session.rollback()
        return {'msg':f"Quantity for product {productId} is missing."}, 422
    Sale=Sales(User_ID = current_user.User_ID, TotalAmount = total)
    db.session.add(Sale)
    db.session.commit()
    for productId, Qtt in PurchaseList.items():
      Sale_ID = Sale.Sale_ID
      Product = db.session.query(Products).get(productId)
      UnitPrice = Product.PPU
      db.session.add(SaleItems(Sale_ID=Sale_ID, P_ID=productId, QuantitySold = Qtt, UnitPrice = UnitPrice))
      stocks = db.session.query(Expiry).filter_by(P_ID=productId).filter(Expiry.expiryDate>datetime.now() + timedelta(days=1)).order_by(asc(Expiry.expiryDate)).all()
      quantity_to_remove = Qtt
      for entry in stocks:
        if quantity_to_remove > 0:
          if quantity_to_remove <= entry.Qty:
            entry.Qty -= quantity_to_remove
            quantity_to_remove = 0
          else:
            quantity_to_remove -= entry.Qty
            entry.Qty = 0
          print(entry.Qty)
    db.session.commit()
    r.delete(f"{current_user.User_ID}//purchases")
    r.delete("flask_cache_view//modifyProducts")
    return {'msg':f"Products created successfully with Sale_id {Sale.Sale_ID}"}, 200

  @jwt_required()
  def delete(self,Sale_ID=None):
    if Sale_ID:
      print(Sale_ID)
      Sale = db.session.query(Sales).get(Sale_ID)
      if Sale and Sale.User_ID==current_user.User_ID:
        if Sale.can_be_deleted:
          [items] = db.session.query(SaleItems).filter_by(Sale_ID = Sale_ID).all()
          sale_items_info = [(item.P_ID, item.QuantitySold) for item in items]
          for P_ID, QuantitySold in sale_items_info:
            stocks = db.session.query(Expiry).filter_by(P_ID=P_ID).filter(Expiry.expiryDate>datetime.now()+ timedelta(days=1)).order_by(asc(Expiry.expiryDate)).first()
            stocks.Qty +=QuantitySold
            db.session.query(Products).filter_by(P_ID=P_ID).update({"Qty": Products.Qty + QuantitySold})
          print(items)
          items = db.session.query(SaleItems).filter_by(Sale_ID = Sale_ID).delete()
          print(items)
          db.session.delete(Sale)
          db.session.commit()
          r.delete(f"{current_user.User_ID}//purchases")
          r.delete("flask_cache_view//modifyProducts")
          return {'msg':f"Order number {Sale_ID} has been deleted"}, 200
        else:
          return {'msg':f"Order {Sale_ID} cannot deleted as it has been longer than 1 day after placing order."}, 403
      else:
        return {'msg':f"Order {Sale_ID} does not exist."}, 404
    else:
      return {'msg':f"Pass Sale_ID as URL parameter to delete"}, 400