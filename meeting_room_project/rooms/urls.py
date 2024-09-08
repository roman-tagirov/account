from django.urls import path
from . import views
from .views import add_user_to_room
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('create_room/', views.create_room, name='create_room'),
    path('my_rooms/', views.my_rooms, name='my_rooms'),
    path('available_rooms/', views.available_rooms, name='available_rooms'),
    path('room/<int:room_id>/', views.room, name='room'),
    path('get_messages/<int:room_id>/', views.get_messages, name='get_messages'),
    path('accounts/profile/', views.home, name='home'),
    path('room/<int:room_id>/add_user/', views.add_user_to_room, name='add_user_to_room'),
    path('room/<int:room_id>/', views.room_view, name='room'),
    path('room/<int:room_id>/remove_user/<int:user_id>/', views.remove_user_from_room, name='remove_user_from_room'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
]
