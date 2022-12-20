from django.shortcuts import render, redirect
from .models import Post, Category, Company, Tag, Comment, Author
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

class PostList(ListView):
    model = Post
    ordering = 'pk'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model=Post
    fields=['title', 'content','price','head_image','file_upload','category','company']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff




    #템플릿 : 모델명_form.html
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(PostCreate, self).get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count']=Post.objects.filter(category=None).count
        return context

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields=['title', 'content','price','head_image','file_upload','category','company']

    template_name = 'shop/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied



    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(PostUpdate, self).get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count']=Post.objects.filter(category=None).count
        return context


class PostDetail(DetailView):
    model=Post

    def get_context_data(self, **kwargs):
        context=super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        context['comment_form'] = CommentForm
        return context

def tag_page(request, slug):
    tag=Tag.objects.get(slug=slug)
    post_list=tag.post_set
    return render(request, 'shop/post_list.html', {
        'tag':tag,
        'post_list':post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count
    })



def category_page(request, slug):
    if slug=='no_category' :
        category ='미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category=Category.objects.get(slug=slug)
        post_list=Post.objects.filter(category=category)
    return render(request, 'shop/post_list.html',{
        'category':category,
        'post_list':post_list,
        'categories':Category.objects.all(),
        'no_category_post_count':Post.objects.filter(category=None).count
    })

def company_page(request, slug):
    if slug=='no_company' :
        company ='미출판사'
        post_list = Post.objects.filter(company=None)
    else:
        company=Company.objects.get(slug=slug)
        post_list=Post.objects.filter(company=company)
    return render(request, 'shop/post_list.html',{
        'company':company,
        'post_list':post_list,
        'companies':Company.objects.all(),
        'no_company_post_count':Post.objects.filter(company=None).count
    })

def author_page(request, slug):
    if slug=='no_author' :
        author ='미분류'
        post_list = Post.objects.filter(author=None)
    else:
        author=Author.objects.get(slug=slug)
        post_list=Post.objects.filter(author=author)
    return render(request, 'shop/post_list.html',{
        'author':author,
        'post_list':post_list,
        'authors':Author.objects.all(),
        'no_author_post_count':Post.objects.filter(author=None).count
    })


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post=post
                comment.author=request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else: #GET
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    #CreateView, UpdateView, form을 사용하면
    #텝플릿 모델명_forms : comment_form 이 자동으로 생성

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user==self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post=comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        PermissionDenied

class PostSearch(PostList):  # ListView 상속, post_list, post_list.html
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q)|Q(tags__name__contains=q)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context