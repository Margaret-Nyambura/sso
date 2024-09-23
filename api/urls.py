from django.urls import path
from . import views
from .views import PlayerListView, PlayerDetailView
from api.views import RegisterUser, LoginUser, ResetPasswordView, UserListView, UserDetailView


urlpatterns = [
    path('players/', PlayerListView.as_view(), name='player_list'),  # URL pattern for listing and creating players
    path('players/<int:player_id>/', PlayerDetailView.as_view(), name='player_detail'),  # URL pattern for retrieving, updating, and deleting a player
    path('user/', UserListView.as_view(), name='user_list'),  
    path('user/<int:id>/', UserDetailView.as_view(), name='user_detail'),
    path('user/register/', RegisterUser.as_view(), name='register'),
    path('user/login/', LoginUser.as_view(), name='login'), 
    path('user/reset_password/', ResetPasswordView.as_view(), name='reset_password'), 
    path('api/user/', UserListView.as_view(), name='user-list'),  

]
