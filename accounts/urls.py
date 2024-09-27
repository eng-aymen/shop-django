from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns=[
     path('', views.dashboard, name='dashboard'),
    path( 'signin' , views.signin , name='signin' ),
    path('logout', views.logout,name='logout'),
    path( 'signup', views.signup , name='signup' ),
    # change password urls
    path('password-change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password-change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done')
    
    # path( 'profile', views.profile , name='profile' ),
    # path('product_favorite/<int:pro_id>',views.product_favorite, name='product_favorite'),
    # path('show_product_favorite',views.show_product_favorite, name='show_product_favorite'),
]