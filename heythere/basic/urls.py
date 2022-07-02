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
    path('like/', views.like_post, name='like-post'),
    path('previewpost/<str:pk>', views.previewPost, name='previewpost'),
    path('post/<str:post_pk>/comment/<int:pk>/like', views.AddCommentLike.as_view(), name='comment-like'),
    path('post/<str:post_pk>/comment/<int:pk>/dislike', views.AddCommentDislike.as_view(), name='comment-dislike'),
    path('delete-comment/<str:pk>/<str:post_pk>', views.deleteComment, name='delete-comment'),
    path('post/<int:post_pk>/comment/<int:pk>/reply', views.CommentReplyView.as_view(), name='comment-reply'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
