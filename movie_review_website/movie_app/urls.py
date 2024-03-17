from django.urls import path

from movie_app import views

urlpatterns = [
    path('',views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('movie_grid_fw/', views.movie_grid_fw, name='movie_grid_fw'),
    path('movie_single/<int:id>', views.movie_single, name='movie_single'),
    path('user_favorite_grid/', views.user_favorite_grid, name='user_favorite_grid'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_rate/', views.user_rate, name='user_rate'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('delete_movie/<int:id>', views.delete_movie, name='delete_movie'),
    path('edit_movie/<int:id>', views.edit_movie, name='edit_movie'),
    path('fav_movie/<int:id>', views.fav_movie, name='fav_movie'),
    path('del_fav_movie/<int:id>', views.del_fav_movie, name='del_fav_movie'),
    path('rate_movie/<int:id>',views.rate_movie, name='rate_movie'),



]