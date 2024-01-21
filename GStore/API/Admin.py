from flask_restful import Resource, reqparse
from .. import admin_required, cache,r
from sqlalchemy.sql import text
from models import db, Authorization, Users, Categories, Products
from flask_jwt_extended import jwt_required, current_user


class requestAdminPrivilege(Resource):
  @admin_required()
  @cache.cached(timeout=0)
  def get(self):
    Open_Authorization = db.session.query(Authorization).all()
    authorization_list = [auth.to_dict() for auth in Open_Authorization]
    return {'msg':authorization_list}, 200
  
  @jwt_required()
  def post(self):
    if current_user.Level=="U":
      exists =db.session.query(Authorization).filter_by(Email=current_user.Email).first()
      if not exists:
        Increase_access_level=Authorization(Email = current_user.Email)
        db.session.add(Increase_access_level)
        db.session.commit()
        r.delete("flask_cache_view//requestAdminPrivilege")
        return {'msg':'Request sent.'}, 200
      else:
        return {'msg':'Request Already sent.'}, 200
    else:
      return {'msg':'Only basic users can apply for promotion.'}, 403


  @admin_required()
  def patch(self):
    Approval = reqparse.RequestParser()
    Approval.add_argument("email", type=str, help='Email of the corresponding user.', required=True)
    Approval.add_argument("approval", type=str, help='Value is "true" if approved and "false" if not approved', required=True, choices=('true', 'false'))
    [Email, Status] = Approval.parse_args().values()
    user=db.session.query(Authorization).filter_by(Email=Email).first()
    if user:
      user=db.session.query(Users).filter_by(Email=Email).first()
      if user and Status and Status.lower()=="true":
        entries_to_delete = db.session.query(Authorization).filter(Email == Email).first()
        db.session.delete(entries_to_delete)
        user.Level="M"
        db.session.commit()
        r.delete("flask_cache_view//requestAdminPrivilege")
        return {'msg':f"{Email} is promoted to manager and removed for pending approval list."}, 200
      if user and Status and Status.lower()=="false":
        entries_to_delete = db.session.query(Authorization).filter(Email == Email).first()
        db.session.delete(entries_to_delete)
        db.session.commit()        
        r.delete("flask_cache_view//requestAdminPrivilege")
        print('reached here')
        return {'msg':f"{Email}'s is not promoted to manager but removed from pending approval list."}, 200
    else:
      return {'msg':"user has not requested for status change or does not exist."}

class modifyCategory(Resource):
  @jwt_required()
  @cache.cached(0)
  def get(self):
    categories = db.session.query(Categories).all()
    categories = [category.Category for category in categories]
    return {'msg':categories}, 200

  @admin_required()
  def post(self):
    NewCategory = reqparse.RequestParser()
    NewCategory.add_argument("newCategory", type=str, help='Name of new category.', required=True)
    [Category] = NewCategory.parse_args().values()
    categoryExists = db.session.query(Categories).filter_by(Category=Category).first()
    if not categoryExists:
      newCat=Categories(Category=Category)
      db.session.add(newCat)
      db.session.commit()
      r.delete("flask_cache_view//modifyCategory")
      return {'msg':f"New category {Category} added"}, 200
    else:
      return {'msg':'Category already exists.'}, 200

  @admin_required()
  def patch(self):
    UpdateCategory = reqparse.RequestParser()
    UpdateCategory.add_argument("categoryOld", type=str, help='Name of category to replace.', required=True)
    UpdateCategory.add_argument("categoryNew", type=str, help='Name of category replacing old category.', required=True)
    [oldCategory, newCategory] = UpdateCategory.parse_args().values()
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
        return {'msg':f"category updated from {oldCategory} to {newCategory} and products with the old category have been updated."}, 200
      else:
        return {'msg':'New category exists, use delete request if you want for category migration. then recreate the category'}, 400
    else:
      return {'msg':'Category does not exist.'}, 404

  @admin_required()
  def delete(self, oldCategory, newCategory):
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
        return {'msg':f"category '{oldCategory}' deleted and products with the old category are set to {newCategory}."}, 200
      else:
        return {'msg':'New category does not exist, use patch request if you want to update.'}, 400
    else:
      return {'msg':'Category to be deleted does not exist.'}, 404
    


#make_template_fragment_key