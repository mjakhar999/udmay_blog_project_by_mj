from django.db.models.query import QuerySet
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from datetime import date
from .models import Post,Author,Tag,Comment,Token
from django.views.generic import ListView,DetailView
from django.views import View
from django.http import HttpResponseRedirect
from blog.form import CommentsForm,UserRegisterForm,CreateBlogForm
from django.urls import reverse
import secrets
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

# class starting_page(View):
#     def get(self,request):
#         all_post = Post.objects.all().order_by('-date')
#         latest_post = all_post[:3]
#         return render(request, "blog/index.html",{"posts":latest_post})


def genrate_code():
    code = secrets.token_urlsafe(nbytes=4)
    return code

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data['username']
            messages.success(request,f"account created for {user_name}")
            return HttpResponseRedirect("home")
        return HttpResponseRedirect(reverse)        
    else:
        form = UserRegisterForm()
    return render(request, "blog/register.html",{"form":form})

# def login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             try:
#                 user = Persons.objects.get(username=form.cleaned_data['username'])  
#             except:
#                 messages.warning(request,"user is not registered, please regitser!!")
#                 return redirect('login')            
  
#             if check_password(form.cleaned_data['password'],user.password) and user is not None:
#                 token = secrets.token_hex(10)
#                 token = str(token)
#                 request.session['user'] = user.username
#                 request.session['email'] = user.email

#                 response = HttpResponseRedirect('home') 
#                 response.set_cookie("token", token)
#                 return response
#             else:
#                   return render(request, 'workout/login.html', {
#                     'form': form,
#                     'error_message': 'Passwords do not match'
#                 })               
#     else:
#         form = LoginForm()
#     return render(request,'workout/login.html',{'form':form})
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

@method_decorator(csrf_exempt , name='dispatch')    
def login_user(request):
    if request.method =="POST":
        
        if request.body:
            data = json.loads(request.body)
            username = data["username"]
            passw = data['password']
            print("ii",type(username),passw)

            # user = User.objects.filter(username =username).first()
            user = authenticate(request,username= username, password = passw)
            print("user",user)
            if user is not None:
                code = genrate_code()
                Token.objects.create(token=code, user= user).save()
                # request.session['id'] = user.id
                login(request,user)
                response = HttpResponseRedirect('home')
                response.set_cookie(key='token',value=code)
                return response
            else:
                return HttpResponse("user not found")

def logout_page(request):
    print('up')
    if request.COOKIES.get("token"):
        print('us')
        # id_s = request.session["id"]
        us = request.user

        print("user",type(us.id))
        tok = Token.objects.get(user__id = us.id)
        print(tok)
        tok.delete()
        print('deleted')
        logout(request)

        response = HttpResponseRedirect('home')
        # response.delete_cookie("token")
        # del request.session['id']
        # request.session.flush()
        print('redirect')
        return response
    else:
        return HttpResponse('error')
            
def checked(request):
    if request.COOKIES.get("token"):
        user = request.user
        print('user',user,user.username)

        # id_s = request.session["id"]
        # print("user",id_s)
        # token = Token.objects.get(user_id = id_s)
        return HttpResponse("mj")
    else:
        return HttpResponse('errors')


class starting_page(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
@method_decorator(csrf_exempt , name='dispatch')    
class Create_blog(View):
    def get(self,request):
        form = CreateBlogForm()
        return render(request, "blog/create.html", {"form":form})
    def post(self,request):
        print(request.POST)
        data = request.POST
        file = request.FILES['image_f']
        print("f",file)
        # print('title',data["image_f"])
        # data = json.loads(request.body)

        # form = CreateBlogForm(request.POST)
        # breakpoint()
        # if form.is_valid():
            # blog = form.save(commit=False)
        blog = Post.objects.create(title = data['title'],content =data['content'],excerpt= data['excerpt'],image_field =file)
        blog.author = request.user
        blog.save()
        return HttpResponse("home")
        # else:

            # print(form.errors)
            # for e,v in form.errors.items():
                # return HttpResponse(e)

        # blog = Post.objects.create(title = form.cleaned_data.get('title'),excerpt = form.cleaned_data.get('excerpt'),
        #         image = form.cleaned_data.get('image'),
        #         date = form.cleaned_data.get('date'),content = form.cleaned_data.get('content'),tags = form.cleaned_data.get('tags'))

        # blog.author = request.user

# from django.db.models import Avg, Max
from .models import Ormq
def tested(request):
    if request.method == 'POST':
        data = request.body

        # user = request.user
        # u = Ormq.objects.values("name").annotate(avg = Avg('num'))
        return HttpResponse("mj")

        # return HttpResponse([(i['name'],i['avg']) for i in u])
        # return HttpResponse([(k,v) for k,v in u.items()])



# @login_required
# class postsview(ListView):
#     model = Post
#     template_name = 'blog/all_post.html'
#     context_object_name = 'all_posts'
#     ordering =['-date']
    # queryset = Post.objects.all().order_by('-date')

    # def get_queryset(self):
    #     return Post.objects.all().order_by('-date')

    # def get_context_data(self, **kwargs):
    #     kwargs['all_posts'] =

class post_details(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
          is_saved_for_later = post_id in stored_posts
        else:
          is_saved_for_later = False

        return is_saved_for_later


    def get(self,request,slug):
        post = Post.objects.get(slug=slug)
        context={"post":post,
        "post_tags":post.tags.all(),
        "comment_form":CommentsForm(),
        'comments':Comment.objects.all().order_by('-pk'),
        "saved_for_later":self.is_stored_post(request,post.id)}
        return render(request,"blog/post-detail.html",context)

    def post(self,request,slug):
        commentform = CommentsForm(request.POST)
        post = Post.objects.get(slug=slug)

        if commentform.is_valid():
            comment = commentform.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-detail-page',args=[slug,]))

        context={"post":post,
        "post_tags":post.tags.all(),
        "comment_form":commentform,
        'comments':Comment.objects.all().order_by('-pk'),
        "saved_for_later":self.is_stored_post(request,post.id)}

        return render(request,"blog/post-detail.html",context)

class Readlater(View):
    def get(self,request):

        stored_posts = request.session.get('stored_posts')
        context = {}

        if stored_posts is None or len(stored_posts)==0:
            context['posts'] =[]
            context['has_post'] =False

        else:
            context['posts'] = Post.objects.filter(pk__in=stored_posts)
            context['has_post'] = True

        return render(request, "blog/readlater.html",context)
        



    def post(self,request):

        post_id = int(request.POST.get('post_id'))

        stored_posts = request.session['stored_posts']
        if stored_posts is None:
            stored_posts =[]

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            
        else:
            stored_posts.remove(post_id)

        request.session['stored_posts'] = stored_posts

        return HttpResponseRedirect("home")



# class post_details(DetailView):
#     model = Post
#     template_name ="blog/post-detail.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['post_tags'] = self.object.tags.all()
#         context['comment-form']  = CommentsForm()
#         return context  



# def starting_page(request):
#     all_post = Post.objects.all().order_by('-date')
#     latest_post = all_post[:3]
#     return render(request, "blog/index.html",{"posts":latest_post})

def posts(request):
    if request.cookies.get('token'):

        all_post = Post.objects.all().order_by('-date')
        return render(request, "blog/all_post.html",{'all_posts':all_post})
    else:
        return HttpResponseRedirect('404.html')



# def post_details(request,slug):
#     ide_post = Post.objects.get(slug=slug)
#     # ide_post = next(post for post in all_posts if post['slug'] == slug)
#     return render(request, "blog/post-detail.html" , {'post':ide_post, "post_tags":ide_post.tags.all()})


# def get_date(post):
#     return post['date']

# def starting_page(request):
#     sort_date = sorted(all_posts , key = lambda k:k['date'])
#     latest_post = sort_date[-3:]
#     return render(request, "blog/index.html",{"posts":latest_post})

# def posts(request):

#     return render(request, "blog/all_post.html",{'all_posts':all_posts})

# def post_details(request,slug):
#     ide_post = next(post for post in all_posts if post['slug'] == slug)
#     return render(request, "blog/post-detail.html" , {'post':ide_post})


from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
 
# CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def view_cached_books(request):
    if 'product' in cache:
        # get results from cache
        products = cache.get('product')
        print(cache,cache.get("product"))
        return HttpResponse(products+ "mj")
 
    else:
        user = request.user

        # results = [product.to_json() for product in products]
        # store data in cache
        cache.set("product", user.username, timeout=CACHE_TTL)
        return HttpResponse(user.username)