from GStore import api, app #keep app here so that this subpackage is imported properly but also keeps unnecessary cruft out
from .Admin import requestAdminPrivilege, modifyCategory
from .Authenticate import Login, Logout, Register, EditProfile, RefreshJWTToken, TestNode
from .Requests import Ticket
from .StoreManager import modifyProducts, CSVExport
from .User import purchases, bill

api.add_resource(requestAdminPrivilege, '/requestAdminPrivilege')
api.add_resource(modifyCategory, '/modifyCategory','/modifyCategory/<oldCategory>/<newCategory>' )

api.add_resource(RefreshJWTToken, "/refreshJWTToken")
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Register, '/register')
api.add_resource(EditProfile, '/editProfile')
api.add_resource(TestNode, '/TestNode')

api.add_resource(Ticket, '/tickets', '/tickets/<int:R_ID>')

api.add_resource(modifyProducts, '/modifyProducts', '/modifyProducts/<int:P_ID>')
api.add_resource(CSVExport, '/CSVExport', '/CSVExport/<task_id>')
api.add_resource(purchases, '/purchases', '/purchases/<int:Sale_ID>')
api.add_resource(bill, '/bill')