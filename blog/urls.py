from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import  views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('register',views.register,name='register-page'),
    path("home/",views.starting_page.as_view(),name="starting-page"),
    # path('post/',views.postsview,name="posts-page"),
    path("post/<slug:slug>",login_required(views.post_details.as_view()),name="post-detail-page"),
    path('read_later',views.Readlater.as_view(),name="read-later-page"),
    path('create/',login_required(views.Create_blog.as_view()),name="create-page"),
    path('test',views.tested),
    path('code',views.genrate_code),
    path('login',views.login_user),
    path('check',views.checked),
    path('logout',views.logout_page),
    path('cac',views.view_cached_books),
    # path("",views.starting_page,name="starting-page"),
    path('post/',views.posts,name="posts-page"),
    # path("post/<slug:slug>",views.post_details,name="post-detail-page"),
] + static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)    
