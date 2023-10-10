from django.urls import path
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.Login, name="login"),
    path("signup/",views.SignUp,name="signup"),
    path("logout/", views.Logout, name="logout"),
    path('create_folder/', views.create_folder, name='create_folder'),  # Define the create_folder URL
    path('folder/<int:folder_id>/', views.folder_detail, name='folder_detail'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    path('file/download/<int:file_id>/', views.file_download, name='file_download'),
    path('folder/delete/<int:folder_id>/', views.folder_delete, name='folder_delete'),
]
