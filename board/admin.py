from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Board

admin.site.register(Board)


#
# class BoardAdmin(SummernoteModelAdmin):
#     summernote_fields = ('content',)
#
# admin.site.register(Board, BoardAdmin)