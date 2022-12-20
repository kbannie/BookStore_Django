from django.urls import path
from . import views

urlpatterns=[
    path('',views.PostList.as_view()),  #views.모델명List.as_view()을 호출하기
    path('<int:pk>/',views.PostDetail.as_view()),  #views.모델명Detail.as_view()을 호출하기
    path('category/<str:slug>/', views.category_page),
    path('company/<str:slug>/', views.company_page),
    path('author/<str:slug>/', views.author_page),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('tag/<str:slug>/', views.tag_page), #IP주소/blog/tag/slug/
    path('create_post/', views.PostCreate.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment),

]