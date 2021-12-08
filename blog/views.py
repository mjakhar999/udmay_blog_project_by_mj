from django.db.models.query import QuerySet
from django.shortcuts import render
from datetime import date
from .models import Post,Author,Tag,Comment
from django.views.generic import ListView,DetailView
from django.views import View
from django.http import HttpResponseRedirect
from blog.form import CommentsForm
from django.urls import reverse
# Create your views here.

# class starting_page(View):
#     def get(self,request):
#         all_post = Post.objects.all().order_by('-date')
#         latest_post = all_post[:3]
#         return render(request, "blog/index.html",{"posts":latest_post})

class starting_page(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data



class posts(ListView):
    model = Post
    template_name = 'blog/all_post.html'
    context_object_name = 'all_posts'
    ordering =['-date']
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

# def posts(request):
    
#     all_post = Post.objects.all().order_by('-date')
#     return render(request, "blog/all_post.html",{'all_posts':all_post})



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
