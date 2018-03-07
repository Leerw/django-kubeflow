from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import login, logout, logout_then_login, password_change, password_change_done, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from . import views

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('logout_then_login', logout_then_login, name='logout_then_login'),

    path('password-change/', password_change, name='password_change'),
    path('password-change/done/', password_change_done, name='password_change_done'),

    url(r'^password-reset/$', password_reset, name='password_reset'), 
    url(r'^password-reset/done/$', password_reset_done, name='password_reset_done'), 

    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'), 

    url(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),

    path('', views.dashboard, name='dashboard'),

    path('register/', views.register, name='register'),

    path('init/', views.init, name='init'),
]
