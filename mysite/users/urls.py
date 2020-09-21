from django.urls import path
from . import views

urlpatterns = [
    path('edit/', views.edit, name='edit'),
    path('', views.profile, name='profile'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('edit/update', views.update, name='update'),
    path('edit/main_photo', views.avatar_update, name='avatar_update'),
    path('add/post', views.add_post, name='add_post'),
    path('add/comment/', views.CommentView.as_view(), name='add_comment'),
    path('<str:username>', views.other_profile, name='other_profile'),
    path('post/like/', views.LikeView.as_view(), name='add_like'),
    path('news/post/like/', views.LikeView.as_view(), name='add_like'),
    path('news/add/comment/', views.CommentView.as_view()),
    path('news/filtered', views.SearchView.as_view(), name='search'),
    path('game/', views.SearchView.as_view(), name='game'),
    # path('game/create/', views.create_game, name='create_game'),
    # path('game/connect/', views.connect2game, name='connect_game'),

]

