from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
import os

class Tag(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/tag/{self.slug}/'

class Company(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(max_length=200, unique=True, allow_unicode=True)
    address = models.TextField()
    number = models.IntegerField()
    email=models.EmailField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/company/{self.slug}'

    class Meta:
        verbose_name_plural='Companies'


class Category(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/category/{self.slug}'

    class Meta:
        verbose_name_plural='Categories'

class Author(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/author/{self.slug}'



class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    price = models.IntegerField()
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    head_image = models.ImageField(upload_to='shop/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='shop/files/%Y/%m/%d/', blank=True)


    def get_absolute_url(self):
        return f'/shop/{self.pk}/'

    def get_file_name(self):  # 파일명 가져오기
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):  # 확장자 가져오기
        return self.get_file_name().split('.')[-1]

    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'

class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'