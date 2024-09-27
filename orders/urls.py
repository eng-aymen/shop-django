from django.urls import path
from . import views

urlpatterns = [
    path('add_to_card' ,views.add_to_card , name='add_to_card'),
    path('card' ,views.card , name='card'),
    path('remove_from_card/<int:order_details_id>' , views.remove_from_card , name='remove_from_card' ),
    path('add_qty<int:order_details_id>' , views.add_qty , name='add_qty' ),
    path('sub_qty<int:order_details_id>' , views.sub_qty , name='sub_qty' ),
    path('payment/' , views.payment , name='payment' ),
    path('show_orders' , views.show_orders , name='show_orders' ),
    path('order/',views.show_orders,name='order'),
    path('order_details/<int:o_id>',views.showOrederDetails,name='od'),
]