from django.urls import path
from .import views


urlpatterns = [
    
    path('',views.loginPage,name='login'),
    path('signup',views.signup,name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('index',views.feeds,name='index'),
    path('profile/<int:user_id>',views.profile,name='view_profile'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('followers',views.follow,name="followers"),
    path('view_followers/<int:user_id>',views.view_followers,name="view_followers"),
    path('privacy',views.privacy_settings,name='privacy_settings'),
    path('add_posts',views.upload_post,name='add_posts'),
    path('like_post',views.like_post,name="like_post"),
    path('delete_post/<uuid:post_id>',views.delete_post,name="delete_post"),
    path('comments/<uuid:post_id>',views.postComments,name='comments'),
     path('search',views.search,name="search")
    

  
]
