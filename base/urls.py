
from . import views
from django.urls import path

urlpatterns = [
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),
    path('',views.home, name="home"),
    path('room/<str:pk>/',views.room, name="room"),
    path('create.room/',views.createRoom,name="create-room"),
    path('update.room/<str:pk>/',views.updateRoom,name="update-room"),
    path('delete.room/<str:pk>/',views.deleteRoom,name="delete-room"),

]
