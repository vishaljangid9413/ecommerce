from django.urls import path
from .views import category_form_view, category_list, delete_category, delete_product, product_detail, product_form_view, product_list, sub_category_list

urlpatterns = [
    path('categories/', category_list, name='category_list'),
    path('categories/<int:pk>/', sub_category_list, name='sub_category_list'),
    path('category/add/', category_form_view, name='add_category'),
    path('category/update/<int:category_id>/', category_form_view, name='update_category'),
    path('categories/<int:pk>/delete/', delete_category, name='category_delete'),

    path('products/<int:pk>/', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
   path('product/add/', product_form_view, name='add_product'),
    path('product/update/<int:product_id>/', product_form_view, name='update_product'),
    path('products/<int:pk>/delete/', delete_product, name='product_delete')
]
