from django.urls import path
from products import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('view/<int:pk>', views.ProductDetail.as_view(), name='product_view'),
    path('new', views.ProductCreate.as_view(), name='product_new'),
    path('edit/<int:pk>', views.ProductUpdate.as_view(), name='product_edit'),
    path('delete/<int:pk>', views.ProductDelete.as_view(), name='product_delete'),
    path('export-books-csv/', views.export_books_csv, name='export_books_csv'),
    path('reserve/<int:pk>', views.reserve_book, name='reserve_book'),
]