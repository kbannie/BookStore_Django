from django.shortcuts import render
from shop.models import Post, Comment

def landing(request):
    recent_posts=Post.objects.order_by('-pk')[:3]
    return render(request,'pages/landing.html',{
        'recent_posts' : recent_posts
    })

def about_me(request):
    return render(request,'pages/about_me.html')

def about_com(request):
    return render(request,'pages/about_com.html')