from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.products,name='products'),
    path('<int:p_id>/',views.product,name='detail'),
    path('dept/<int:d_id>/',views.products_dept,name='products_dept'),
    path('branch/<int:b_id>/',views.products_branch,name='products_branch'),
    path('category/<int:c_id>/',views.products_category,name='products_category'),
    path('cart/',views.cart,name='cart'),

]
