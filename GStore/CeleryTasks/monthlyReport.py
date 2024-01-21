from . import celery
from GStore import mail
from flask_mail import Message
from models import db, Users, Sales, SaleItems,Products
from datetime import datetime,timedelta
from datetime import datetime
from sqlalchemy import func
from flask import render_template
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import func, case
import plotly.express as px
import plotly.io as pio
import pandas as pd
from weasyprint import HTML
import base64


@celery.task
def monthlyMailer():
  one_month_ago = datetime.now() - timedelta(days=31, hours=5, minutes=30)
  users=db.session.query(Users).filter_by(Level='U').all()
  with mail.connect() as conn:
    for user in users:
      salesData =  db.session.query(Sales.Sale_ID, Sales.SaleDate, Products.PName, func.round(SaleItems.QuantitySold,3), Products.Units, func.round((SaleItems.QuantitySold * SaleItems.UnitPrice),2).label('total')).filter(Sales.User_ID == user.User_ID).\
                      filter(Sales.SaleDate >= one_month_ago).join(SaleItems, Sales.Sale_ID == SaleItems.Sale_ID).join(Products, SaleItems.P_ID == Products.P_ID).order_by(Sales.SaleDate.asc()).all()
      salesData_df = pd.DataFrame(salesData, columns=['Sale_ID', 'SaleDate', 'Product', 'QuantitySold', 'Unit', 'total'])

      expenseOverTime =  db.session.query(Sales.Sale_ID, Sales.SaleDate, Products.PName, func.round(SaleItems.QuantitySold,3), Products.Units, func.round((SaleItems.QuantitySold * SaleItems.UnitPrice),2).label('total')).filter(Sales.User_ID == user.User_ID).\
                      filter(Sales.SaleDate >= one_month_ago).join(SaleItems, Sales.Sale_ID == SaleItems.Sale_ID).join(Products, SaleItems.P_ID == Products.P_ID).group_by(Sales.Sale_ID).order_by(Sales.SaleDate.asc()).all()
      expenseOverTime_df = pd.DataFrame(expenseOverTime, columns=['Sale_ID', 'SaleDate', 'Product', 'QuantitySold', 'Unit', 'total'])
      expenseOverTime_df['cumulative_total'] = expenseOverTime_df.groupby('SaleDate')['total'].cumsum()
      overtime = px.line(expenseOverTime_df, x='SaleDate', y='cumulative_total', 
                    labels={'cumulative_total': 'Cumulative Expense', 'SaleDate': 'Sale Date'},
                    title='Cumulative Expenditure')
      expenditure = expenseOverTime_df['total'].sum()

      categoryExpenditure = db.session.query(Products.Category, func.round(func.sum(SaleItems.QuantitySold * SaleItems.UnitPrice),2).label('total_per_category')).filter(Sales.User_ID == user.User_ID).\
                join(SaleItems).join(Sales).filter(Sales.SaleDate >= one_month_ago).group_by(Products.Category).all()
      pie_df = pd.DataFrame(categoryExpenditure, columns=['Category', 'total_per_category'])
      category_pie = px.pie(pie_df, names='Category', values='total_per_category',title='Expenditure by Category',
                                labels={'total_per_category': 'Amount Spent', 'Category': 'Category'})

      dayCategoryExpenditure = db.session.query(func.date(Sales.SaleDate).label('soldDate'),(Products.PName).label('ProductName'), Products.Category, func.sum(case((Products.Units == 'g', func.round((SaleItems.QuantitySold / 1000),3)),else_=SaleItems.QuantitySold)),
                                  func.sum(func.round(SaleItems.QuantitySold * SaleItems.UnitPrice,3)).label('total')).join(SaleItems, SaleItems.Sale_ID==Sales.Sale_ID).\
                                  join(Products,Products.P_ID==SaleItems.P_ID).filter(func.date(Sales.SaleDate) >= one_month_ago.date()).group_by(func.date(Sales.SaleDate), Products.PName).all()
      bubble_df = pd.DataFrame(dayCategoryExpenditure, columns=['soldDate','ProductName', 'Category', 'QuantitySold', 'total'])
      print(bubble_df)
      spent_bubble = px.scatter(bubble_df, x='soldDate', y='QuantitySold', log_y=True, size_max=40, size='total', color='Category', hover_name="ProductName",
                                    labels={'soldDate': 'Sold Date', 'QuantitySold': 'Quantity bought'}, title='Summary of expenditure in the last 30 days')
      #Create HTML
      raw_data_html = salesData_df.to_html(index=False, classes=["table", "table-striped"], justify="left")
      overtime_html = pio.to_html(overtime, full_html=False, include_plotlyjs=True)
      category_pie_html = pio.to_html(category_pie, full_html=False, include_plotlyjs=True)
      spent_bubble_html = pio.to_html(spent_bubble, full_html=False, include_plotlyjs=True)
      html_body = render_template('./CeleryTasks/templates/monthlyReportHTML.html', expenditure=expenditure,
                                  overtime=overtime_html, category_pie=category_pie_html, 
                                  spent_bubble=spent_bubble_html, raw_data=raw_data_html)
      #easier to visualise on non interactive images (better visibilty when plotly.js module cannot be used)
      dayCategoryExpenditure = db.session.query(func.date(Sales.SaleDate).label('soldDate'),(Products.PName).label('ProductName'), Products.Category, func.sum(case((Products.Units == 'g', func.round((SaleItems.QuantitySold / 1000),3)),else_=SaleItems.QuantitySold)),
                                  func.sum(func.round(SaleItems.QuantitySold * SaleItems.UnitPrice,3)).label('total')).join(SaleItems, SaleItems.Sale_ID==Sales.Sale_ID).\
                                  join(Products,Products.P_ID==SaleItems.P_ID).filter(func.date(Sales.SaleDate) >= one_month_ago.date()).group_by(func.date(Sales.SaleDate), Products.Category).all()
      #Create PDF
      overtime_image = "data:image/svg+xml;base64,{}".format(base64.b64encode(pio.to_image(overtime, format="svg", width=385, height=390)).decode('utf-8'))
      category_pie_image = "data:image/svg+xml;base64,{}".format(base64.b64encode(pio.to_image(category_pie, format="svg", width=385, height=390)).decode('utf-8'))
      spent_bubble_image = "data:image/png;base64,{}".format(base64.b64encode(pio.to_image(spent_bubble, format="png", width=770, height=525)).decode('utf-8'))
      pdfembed = render_template('./CeleryTasks/templates/monthlyReportPDF.html', expenditure=expenditure,
                                 overtime=overtime_image, category_pie=category_pie_image,
                                 spent_bubble=spent_bubble_image, raw_data=raw_data_html)
      pdf = HTML(string=pdfembed).write_pdf()

      #Create EMAIL HTML
      overtime_image = pio.to_image(overtime, format="png")
      category_pie_image = pio.to_image(category_pie, format="png")
      spent_bubble_image = pio.to_image(spent_bubble, format="png")
      html_embed = render_template('./CeleryTasks/templates/monthlyReportEmail.html', expenditure=expenditure,
                                              overtime_cid='overtime_cid', category_pie_cid='category_pie_cid',
                                              spent_bubble_cid='spent_bubble_cid', raw_data=raw_data_html)
      msg = Message(recipients=[user.Email], 
                    subject = "Monthly Report for GStore", 
                    body = "Here is your monthly report attached. You can download it as an HTML or a PDF.", html = html_embed)
      msg.attach(filename='report.html', content_type="text/html", data=html_body)
      msg.attach(filename='report.pdf', content_type="application/pdf", data=pdf)
      msg.attach(filename="expenditure_over_time.png", content_type="image/png", data=overtime_image, disposition="inline",  headers=[['Content-ID', '<overtime_cid>']])
      msg.attach(filename="percent_expenditure.png", content_type="image/png", data=category_pie_image, disposition="inline", headers=[['Content-ID', '<category_pie_cid>']])
      msg.attach(filename="bubble_expenditure.png", content_type="image/png", data=spent_bubble_image, disposition="inline",  headers=[['Content-ID', '<spent_bubble_cid>']])


      conn.send(msg)