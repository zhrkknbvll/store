from .views import UserProfileAdmin, CategoryAdmin, ProductAdmin
from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine



def setup_admin(mysite: FastAPI):
    admin = Admin(mysite, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ProductAdmin)
