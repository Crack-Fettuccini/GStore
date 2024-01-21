from flask_restful import Resource, reqparse
from .. import manager_required, cache, r, current_user
from models import db, Products,Categories, Expiry
from flask_jwt_extended import jwt_required
from ..CeleryTasks import asyncCSVExport
from datetime import datetime, timedelta
from sqlalchemy import asc
from io import BytesIO
import zipfile
import base64

class modifyProducts(Resource):
  @jwt_required()
  @cache.cached(timeout=60*60)
  def get(self):
    Available_Products = db.session.query(Products).filter(Products.Qty >= 0).all()
    Products_list = [product.to_dict() for product in Available_Products]
    Products_list.reverse()
    Products_list = sorted(Products_list, key=lambda product: product['availableStock'] == 0)
    return {'msg':Products_list}, 200
  
  @manager_required()
  def post(self):
    New_Product = reqparse.RequestParser()
    New_Product.add_argument('productName', type=str, help="Name of the product.", required=True)
    New_Product.add_argument('availableStock', type=int, help="Stock of new Product.", required=True)
    New_Product.add_argument('expiryDate',type=str, help="Expiry date of current stock", required=True)
    New_Product.add_argument('productImage', type=str, help="Image URL for product.", required=True)
    New_Product.add_argument('category', type=str, help="Cateogry product belongs to.", required=True)
    New_Product.add_argument('pricePerUnit', type=float, help="Price of product.", required=True)
    New_Product.add_argument('Unit', type=str, help="Unit in which product is measured.", required=True)
    exists = New_Product.parse_args().values()
    [PName, Qty, expiryDate, PdtShot, Category, PPU, Unit] = exists
    if all(exists):
      itemexists = db.session.query(Products).filter_by(PName = PName).first()
      if not itemexists:
        if Unit in ['ml','g','packs']:
          if Qty>=0:
            categories = db.session.query(Categories).all()
            categories = [category.Category for category in categories]
            if Category in categories:
              if PPU>=0:
                if expiryDate:
                  expiryDate = (datetime.strptime(expiryDate, '%Y-%m-%d')).replace(hour=23, minute=59, second=59)
                  if expiryDate >= datetime.now()+ timedelta(days=1):
                    newProduct=Products(PName = PName, Qty = Qty, PdtShot = PdtShot, Category = Category, PPU = PPU, Units = Unit)
                    db.session.add(newProduct)
                    db.session.commit()
                    newStock=Expiry(P_ID = newProduct.P_ID, Qty = Qty, expiryDate = expiryDate)
                    db.session.add(newStock)
                    db.session.commit()
                  else:
                    return {'msg':'Expiry date must be provided and should be later than current date.'}, 400
                else:
                  return {'msg':f"{newProduct.PName} has been added to list of products",'item':itemexists.to_dict()}, 200
                r.delete("flask_cache_view//modifyProducts")
                return {'msg':newProduct.to_dict()}, 200
              else:
                return {'msg':"Price cannot be negative."}, 400
            else:
              return {'msg':'Product category can only be in given list of categories.'}, 400
          else:
            return {'msg':"Quantity cannot be negative."}, 400
        else:
          return {'msg':"Units can only be 'ml', 'g', or 'packs'"}, 400
      elif itemexists.Qty<0:
        if Unit in ['ml','g','packs']:
          if Qty>=0:
            categories = db.session.query(Categories).all()
            categories = [category.Category for category in categories]
            if Category in categories:
              if PPU>=0:
                itemexists.PName = PName
                itemexists.Qty = Qty
                itemexists.PdtShot = PdtShot
                itemexists.Category = Category
                itemexists.PPU = PPU
                itemexists.Units = Unit
                db.session.commit()
                r.delete("flask_cache_view//modifyProducts")
                return {'msg':f"{itemexists.PName} has been added to list of products",'item':itemexists.to_dict()}, 200
              else:
                return {'msg':"Price cannot be negative."}, 400
            else:
              return {'msg':'Product category can only be in given list of categories.'}, 400
          else:
            return {'msg':"Quantity cannot be negative."}, 400
        else:
          return {'msg':"Units can only be 'ml', 'g', or 'packs'"}, 400
      else:
        return {'msg':itemexists.to_dict()}, 200

  @manager_required()
  def patch(self):
    New_Product = reqparse.RequestParser()
    New_Product.add_argument('productID', type=int, help="ID of product.", required=True)
    New_Product.add_argument('productName', type=str, help="Name of the product.")
    New_Product.add_argument('increasedStock', type=int, help="Stock added to inventory the product")
    New_Product.add_argument('expiryDate', type=str, help="Expiry date of current stock")
    New_Product.add_argument('productImage', type=str, help="Image URL to change current image of product.")
    New_Product.add_argument('category', type=str, help="Category which would suit the product more.")
    New_Product.add_argument('PricePerUnit', type=float, help="Price of product.")
    New_Product.add_argument('Unit', type=str, help="Unit in which product is measured.")
    [P_ID, PName, Qty,expiryDate, PdtShot, Category, PPU, Unit] = New_Product.parse_args().values()
    Product = db.session.query(Products).get(P_ID)
    print(expiryDate)
    if Product:
      if any([P_ID, PName, Qty, PdtShot, Category, PPU, Unit]):
        if PName:
          itemexists = db.session.query(Products).filter_by(PName = PName).filter(Products.P_ID != P_ID).first()
          if not itemexists:
            Product.PName=PName
          else:
            return {'msg':f"Product with name {PName} already exists."}, 400
        if Qty:
          if Qty+Product.Qty>=0:
            if Qty>=0:
              if expiryDate:
                expiryDate = (datetime.strptime(expiryDate, '%Y-%m-%d')).replace(hour=23, minute=59, second=59)
                if expiryDate >= datetime.now():
                  newStock=Expiry(P_ID = P_ID, Qty = Qty, expiryDate = expiryDate)
                  db.session.add(newStock)
                else:
                  return {'msg':'Expiry date must be later than today.'}, 400
              else:
                return {'msg':'Expiry date must be provided.'}, 400
            else:
              stocks = db.session.query(Expiry).filter_by(P_ID=P_ID).filter(Expiry.expiryDate>datetime.now()).order_by(asc(Expiry.expiryDate)).all()
              quantity_to_remove = Qty
              for entry in stocks:
                if quantity_to_remove < 0:
                  if entry.Qty <= abs(quantity_to_remove):
                    quantity_to_remove += entry.Qty
                    entry.Qty = 0
                  else:
                    entry.Qty += quantity_to_remove
                    quantity_to_remove = 0
                  print(entry.Qty)
            Product.Qty=Qty+Product.Qty
          else:
            return {'msg':'Product quantity cannot be zero.'}, 400
        if PdtShot:
          Product.PdtShot=PdtShot
          db.session.commit()
        categories = db.session.query(Categories).all()
        categories = [category.Category for category in categories]
        if Category:
          if Category in categories:
            Product.Category=Category
          else:
            return {'msg':'Product category can only be in given list of categories.'}, 400
        if PPU:
          if PPU>=0:
            Product.PPU=PPU
          else:
            return {'msg':'Product price cannot be lesser than zero.'}, 400
        if Unit:
          if Unit in ['g','ml','packs']:
            Product.Units=Unit
          else:
            return {'msg':"Product unit canonly be 'ml', 'g' or 'packs'."}, 400
        db.session.commit()
        r.delete("flask_cache_view//modifyProducts")
        return {'msg':f"{Product.PName} updated."}, 200
      else:
        return {'msg':f"{Product.PName} not modified."}, 400
    else:
      return {'msg':f"Product with P_ID {P_ID} does not exist"}, 404
  
  @manager_required()
  def delete(self, P_ID):
    Product = db.session.query(Products).get(P_ID)
    if Product:
      Product.Qty=-1
      db.session.commit()
      r.delete("flask_cache_view//modifyProducts")
      return {'msg':f'{Product.PName} deleted'}, 200
    else:
      return {'msg':f"Product with P_ID {P_ID} does not exist"}, 404

class CSVExport(Resource):
  def get(self, task_id):
    task = asyncCSVExport.AsyncResult(task_id)
    print(task)
    if task:
      if task.state == 'PENDING':
        return {"msg":"task is still pending"}, 204
      if task.state == 'SUCCESS':
        sales_csv, stock_csv = task.result
        sales_buffer = BytesIO(sales_csv.encode())
        stock_buffer = BytesIO(stock_csv.encode())
        zip_buffer = BytesIO()
        with zipfile.ZipFile("zip_buffer.zip", 'w') as zip:
          sales_buffer.seek(0)
          stock_buffer.seek(0)
          zip.writestr('sales.csv', sales_buffer.getvalue())
          zip.writestr('stock.csv', stock_buffer.getvalue())
        """
        with zipfile.ZipFile(zip_buffer, 'w') as zip:
          sales_buffer.seek(0)
          stock_buffer.seek(0)
          zip.writestr('sales.csv', sales_buffer.getvalue())
          zip.writestr('stock.csv', stock_buffer.getvalue())
          zip_buffer.seek(0)
          """
        sales_buffer.seek(0)
        stock_buffer.seek(0)
        return {"file1":base64.b64encode(sales_buffer.read()).decode('utf-8'),"file2":base64.b64encode(stock_buffer.read()).decode('utf-8')}, 200
    else:
      return {"msg":"Task with task_id doesnt exist"}, 404

  @manager_required()
  def post(self):
    task = asyncCSVExport.apply_async(args=[current_user.Username, current_user.Email])
    print(task.id)
    return {'msg':task.id}, 200
