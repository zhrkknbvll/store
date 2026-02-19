from mysite.database.models import UserProfile, Category, Product, Review, RefreshToken

from sqladmin import ModelView

class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.product_name]