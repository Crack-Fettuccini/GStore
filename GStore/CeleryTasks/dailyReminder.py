from . import celery
from GStore import mail
from flask_mail import Message
from models import db, Users, Sales
from datetime import datetime,timedelta
from datetime import datetime
from flask import render_template


@celery.task
def logTimer():
  time=datetime.now()
  print(f"the time is {time.strftime('%H:%M:%S')}")

@celery.task
def mailer():
  users=db.session.query(Users).filter_by(Level='U').all()
  with mail.connect() as conn:
    for user in users:
      most_recent_sale = db.session.query(Sales).filter_by(User_ID=user.User_ID).order_by(Sales.SaleDate.desc()).first()
      html_body = render_template(
                './CeleryTasks/templates/dailyReminder.html',
                user=user,
                most_recent_sale=most_recent_sale,
                datetime=datetime,
                timedelta=timedelta
            )
      if most_recent_sale:
        if (datetime.now() - most_recent_sale.SaleDate)>timedelta(days=1,hours=12):
          subject = f"Thank you for your purchase at GStore, {user.Username}"
        else:
          subject = f"We miss you, {user.Username}"
      else:
          subject = f"Welcome to GStore, {user.Username}"
      msg = Message(recipients=[user.Email],
                    html=html_body,
                    body=html_body,
                    subject=subject)
      conn.send(msg)
