from . import celery, r
from models import db, Products, Expiry
from datetime import datetime
from sqlalchemy import asc


@celery.task
def updateStock():
  products = db.session.query(Products).filter(Products.Qty>=0).all()
  for product in products:
    stocks = db.session.query(Expiry).filter_by(P_ID=product.P_ID).filter(Expiry.expiryDate>datetime.now()).order_by(asc(Expiry.expiryDate)).all()
    total=0
    if stocks:
      for stock in stocks:
        total += stock.Qty
        print(stock)
    product.Qty=total
    print(total)
    db.session.commit()
    r.delete("flask_cache_view//modifyProducts")
