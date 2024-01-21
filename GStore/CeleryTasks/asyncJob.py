from . import celery
from GStore import mail
from flask_mail import Message
from models import db, Sales, SaleItems,Products
from datetime import datetime,timedelta
from flask import render_template
from sqlalchemy import func
from datetime import datetime
import pandas as pd

@celery.task(bind=True)
def asyncCSVExport(self, user, Email):
  one_month_ago = datetime.now() - timedelta(days=31, hours=5, minutes=30)
  with mail.connect() as conn:
    salesData =  (db.session.query(Sales.Sale_ID, Sales.SaleDate, Products.PName, func.round(SaleItems.QuantitySold,3), Products.Units, func.round((SaleItems.QuantitySold * SaleItems.UnitPrice),2).label('total'))
                  .join(SaleItems, Sales.Sale_ID == SaleItems.Sale_ID).join(Products, SaleItems.P_ID == Products.P_ID)
                  .order_by(Sales.SaleDate.asc()).all())
    sales_df = pd.DataFrame(salesData, columns=['Sale_ID', 'SaleDate', 'Product', 'QuantitySold', 'Unit', 'total'])
    print(sales_df)
    sales_csv=sales_df.to_csv()

    productdata=(db.session.query(Products.P_ID, Products.PName, Products.Qty, Products.Category, Products.PPU, Products.Units).all())
    totalsolddata = db.session.query(SaleItems.P_ID,func.sum(SaleItems.QuantitySold).label('total_quantity_sold')).join(Sales, Sales.Sale_ID == SaleItems.Sale_ID).filter(Sales.SaleDate >= one_month_ago).group_by(SaleItems.P_ID).all()
    productdf = pd.DataFrame(productdata, columns=['P_ID', 'PName', 'Qty', 'Category', 'PPU', 'Units'])
    totalsolddf = pd.DataFrame(totalsolddata, columns=['P_ID', 'total_quantity_sold'])
    Stock_df = pd.merge(productdf, totalsolddf, on='P_ID', how='left').fillna(0)
    print(Stock_df)
    stock_csv=Stock_df.to_csv()
    html_body = render_template('./CeleryTasks/templates/asyncJob.html', user=user)

    msg = Message(recipients=[Email], 
                  subject = "Monthly Report for GStore", 
                  body = "Here is your monthly report attached. You can download it as an HTML or a PDF.", html = html_body)
    msg.attach(filename='sales.csv', content_type="text/csv", data=sales_csv)
    msg.attach(filename='stock.csv', content_type="text/csv", data=stock_csv)
    conn.send(msg)
  return sales_csv, stock_csv
