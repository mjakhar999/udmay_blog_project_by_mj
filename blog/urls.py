from django.urls import path
from . import  views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('register',views.register,name='register-page'),
    path("home/",views.starting_page.as_view(),name="starting-page"),
    # path('post/',views.postsview,name="posts-page"),
    path("post/<slug:slug>",login_required(views.post_details.as_view()),name="post-detail-page"),
    path('read_later',views.Readlater.as_view(),name="read-later-page"),
    path('create',views.Create_blog.as_view(),name="create-page"),
    path('test',views.tested),
    # path("",views.starting_page,name="starting-page"),
    path('post/',views.posts,name="posts-page"),
    # path("post/<slug:slug>",views.post_details,name="post-detail-page"),
]
