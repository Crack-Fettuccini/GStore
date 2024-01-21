from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from .authorize import Authorization
from .categories import Categories
from .products import Products
from .requests import Requests
from .saleitems import SaleItems
from .sales import Sales
from .users import Users
from .expiry import Expiry