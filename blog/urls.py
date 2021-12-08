from django.urls import path
from . import  views
urlpatterns = [
    path("home/",views.starting_page.as_view(),name="starting-page"),
    path('posts/',views.posts.as_view(),name="posts-page"),
    path("post/<slug:slug>",views.post_details.as_view(),name="post-detail-page"),
    path('read_later',views.Readlater.as_view(),name="read-later-page"),
    # path("",views.starting_page,name="starting-page"),
    # path('posts/',views.posts,name="posts-page"),
    # path("post/<slug:slug>",views.post_details,name="post-detail-page"),
]
