from ntpath import join
from turtle import circle
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
    path('like/<str:check>/<str:name>', views.like_post, name='like-post'),
    path('like-previewpost/', views.like_previewpost, name='like-previewpost'),
    path('previewpost/<str:pk>', views.previewPost, name='previewpost'),
    path('post/<str:post_pk>/comment/<int:pk>/like', views.AddCommentLike.as_view(), name='comment-like'),
    path('post/<str:post_pk>/comment/<int:pk>/dislike', views.AddCommentDislike.as_view(), name='comment-dislike'),
    path('delete-comment/<str:pk>/<str:post_pk>', views.deleteComment, name='delete-comment'),
    path('post/<int:post_pk>/comment/<int:pk>/reply', views.CommentReplyView.as_view(), name='comment-reply'),
    path('userprofile/<str:username>', views.userProfile, name='userprofile'),
    path('updateprofile/<str:username>', views.updateprofile, name='updateprofile'),
    path('globalpage/', views.globalPostPage, name='globalpage'),
    path('createcircle/', views.createCircle, name='createcircle'),
    path('updatecircle/<str:circle>', views.updateCircle, name='updatecircle'),
    path('circle/<str:circle>', views.circle, name='circle'),
    path('create-circle-post/<str:circle>', views.createCirclePost, name='create-circle-post'),
    # path('join-circle/<str:circle>', views.joinCircle, name='join-circle'),
    path('all-circle/', views.allCircle, name='all-circle'),
    path('join/', views.join, name='join'),
    path('circle-chat/<str:circle>', views.circleChat, name='circle-chat'),
    path('private-chat/<str:friend>', views.privateChat, name='private-chat'),
    path('addfriend/<str:username>', views.addfriend, name='addfriend'),
    path('friend-requests/', views.friendRequests, name='friend-requests'),
    path('accept-request/<str:username>/<str:check>', views.acceptRequest, name='accept-request'),
    path('decline-request/<str:username>/<str:check>', views.declineRequest, name='decline-request'),
    path('cancel-request/<str:username>', views.cancelRequest, name='cancel-request'),
    path('unfriend/<str:username>', views.unFriend, name='unfriend'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
