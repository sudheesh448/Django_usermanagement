
from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.home, name='home' ),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('adminlogin', views.adminlogin, name="adminlogin"),
    path('dashboard', views.dashboard, name='dashboard'),
    path('adminlogout/', views.admin_logout, name='admin_logout'),
    path('create_user', views.create, name='create'),
    path('update/<int:user_id>', views.update, name='update'),
    path('delete/<int:user_id>', views.delete, name='delete'),
    path('search', views.search, name='search'),

]