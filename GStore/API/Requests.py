from flask_restful import Resource, reqparse
import re
from .. import admin_required, manager_required, cache,r
from models import db, Requests, Categories, Products
from flask_jwt_extended import current_user

class Ticket(Resource):
  @manager_required()
  def get(self):
    if current_user.Level=="A":
      Open_Requests = db.session.query(Requests).filter_by(Resolution='Pending').all()
    elif current_user.Level=="M":
      cache_key = f"{current_user.User_ID}//Ticket"
      cached_data = cache.get(cache_key)
      if cached_data is not None:
        return {'msg': cached_data}, 200
      else:
        Open_Requests = db.session.query(Requests).filter_by(User_ID=current_user.User_ID).all()
    if Open_Requests:
      Open_Requests = [request.to_dict() for request in Open_Requests]
      Open_Requests.reverse()
    if current_user.Level=="M":
      cache.set(cache_key, Open_Requests)
    return {'msg':Open_Requests}, 200
    
  
  @manager_required()
  def post(self):
    New_ticket = reqparse.RequestParser()
    New_ticket.add_argument("title", type=str, help="Title of the request ticket.", required=True)
    New_ticket.add_argument("request", type=str, help="Explanation of the requested change.", required=True)
    [title, request] = New_ticket.parse_args().values()
    if title and request:
      newTicket=Requests(User_ID = current_user.User_ID, RTitle = title, RMessage = request, Resolution = "Pending", AdminMessage="")
      db.session.add(newTicket)
      db.session.commit()
      r.delete(f"flask_cache_{current_user.User_ID}//Ticket")
      return {'msg':'Request sent'}, 200
    else:
      return {'msg':"internal error"}, 500
  @admin_required()
  def patch(self):
    New_ticket = reqparse.RequestParser()
    New_ticket.add_argument("requestID", type=str, help="ID fo the requested Ticket.", required=True)
    New_ticket.add_argument("Resolution", type=str, help='Resolution of thr ticket, "Approved" or "Rejected".', required=True)
    New_ticket.add_argument("AdminMessage", type=str, help="Explanation for rejection or approval.", required=True)
    [R_ID, Resolution, AdminMessage] = New_ticket.parse_args().values()
    Request = db.session.query(Requests).get(R_ID)
    if Request:
      if Resolution == "Approved":
        Request.Resolution = "Approved"
        if AdminMessage:
          Request.AdminMessage = AdminMessage
        else:
          Request.AdminMessage = "Request marked as Closed."

        createpattern = r'Create category ([\w\s]+)'
        renamepattern = r'Rename category ([\w\s]+) to ([\w\s]+)'
        deletepattern = r'Delete category ([\w\s]+) and move products to ([\w\s]+)'
        match1 = re.search(createpattern, Request.RTitle)
        match2 = re.search(renamepattern, Request.RTitle)
        match3 = re.search(deletepattern, Request.RTitle)

        if match1:
          Category = match1.group(1)
          categoryExists = db.session.query(Categories).filter_by(Category=Category).first()
          if not categoryExists:
            newCat=Categories(Category=Category)
            db.session.add(newCat)
            db.session.commit()
            r.delete("flask_cache_view//modifyCategory")
            r.delete(f"flask_cache_{Request.User_ID}//Ticket")
            return {'msg':f"New category {Category} added"}, 200
          else:
            return {'msg':'Category already exists.'}, 200

        elif match2:
          oldCategory = match2.group(1)
          newCategory = match2.group(2)
          categoryExists = db.session.query(Categories).filter_by(Category=oldCategory).first()
          newCategoryExists = db.session.query(Categories).filter_by(Category=newCategory).first()
          if categoryExists:
            if not newCategoryExists:
              categoryExists.Category =  newCategory
              products = db.session.query(Products).filter_by(Category=oldCategory).all()
              for product in products:
                product.Category = newCategory
              db.session.commit()
              r.delete("flask_cache_view//modifyCategory")
              r.delete(f"flask_cache_{Request.User_ID}//Ticket")
              return {'msg':f"category updated from {oldCategory} to {newCategory} and products with the old category have been updated."}, 200
            else:
              return {'msg':'New category exists, use delete request if you want for category migration. then recreate the category'}, 400
          else:
            return {'msg':'Category does not exist.'}, 404

        elif match3:
          oldCategory = match3.group(1)
          newCategory = match3.group(2)
          oldCategoryExists = db.session.query(Categories).filter_by(Category=oldCategory).first()
          newCategoryExists = db.session.query(Categories).filter_by(Category=newCategory).first()
          if oldCategoryExists:
            if newCategoryExists:
              products = db.session.query(Products).filter_by(Category=oldCategory).all()
              for product in products:
                product.Category = newCategory
              db.session.delete(oldCategoryExists)
              db.session.commit()
              r.delete("flask_cache_view//modifyCategory")
              r.delete(f"flask_cache_{Request.User_ID}//Ticket")
              return {'msg':f"category '{oldCategory}' deleted and products with the old category are set to {newCategory}."}, 200
            else:
              return {'msg':'New category does not exist, use patch request if you want to update.'}, 400
          else:
            return {'msg':'Category to be deleted does not exist.'}, 404
        else:
          print("Pattern not found in the input string")
      elif Resolution == "Rejected":
        Request.Resolution = "Rejected"
        if AdminMessage:
          Request.AdminMessage = AdminMessage
        else:
          Request.AdminMessage = "Request marked as Closed."
        r.delete("flask_cache_view//modifyCategory")
        r.delete(f"flask_cache_{Request.User_ID}//Ticket")
        db.session.commit()
        return {'msg':'Request rejected'}, 200
      else:
        return {'msg':'Resolution can only be either "Approved" or "Rejected"'}, 400
    else:
      return {'msg':f"Request with request ID {R_ID} does not exist"}, 404
  
  @manager_required()
  def delete(self,R_ID):
    if current_user.Level=="M":
      Request = db.session.query(Requests).get(R_ID)
      if current_user.User_ID == Request.User_ID:
        db.session.delete(Request)
        r.delete(f"flask_cache_{Request.User_ID}//Ticket")
        return {'msg':'Request deleted successfully'}, 200

"""
R_ID = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
  User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
  RTitle = db.Column(db.String, nullable=False)
  RMessage = db.Column(db.Integer, nullable=False)
  Resolution = db.Column(db.String, nullable=False)
  AdminMessage = db.Column(db.String)
  __table_args__ = (
    CheckConstraint(Resolution.in_(("Pending", "Approved", "Rejected")), name="chk_resolution"),
  )
"""