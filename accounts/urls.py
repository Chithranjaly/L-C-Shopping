
from django.urls import path
from accounts import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot_password/',views.forgot_password,name="forgot_password"),
    path('resetpassword_validate/',views.resetpassword_validate,name="resetpassword_validate"),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
