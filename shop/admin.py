from django.contrib import admin
from .models import Post, Company, Tag,Category, Comment, Author

class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}

class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}


admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)