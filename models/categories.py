from . import db


class Categories(db.Model):
  __tablename__='categories'
  Category=db.Column(db.String, nullable=False, primary_key=True)

  def to_dict(self):
    return {
      'category':self.Category
    }