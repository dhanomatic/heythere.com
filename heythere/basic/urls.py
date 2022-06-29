from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('create-post/<str:pk>', views.createPost, name='create-post'),
    path('update-post/<str:pk>', views.updatePost, name='update-post'),
    path('delete-post/<str:pk>', views.deletePost, name='delete-post'),
    path('upvote/<str:postid>', views.upVote, name='upvote'),
    path('downvote/<str:postid>', views.downVote, name='downvote'),
    path('like/<str:pk>', views.likeView, name='like_post'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
