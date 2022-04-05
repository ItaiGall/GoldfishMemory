from django.urls import path
from . import views

app_name = 'Accounts_App'
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change_cred/', views.change_credentials, name='change_credentials'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_userinfo/', views.change_userinfo, name='change_userinfo'),
    path('user_stats/', views.user_stats, name='user_stats'),
]