from django.contrib import admin

from .models import Book, BookFullText, User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

class BookAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'created', 'type_book')
	list_display_links = ('id', 'title')
	search_fields = ('id', 'title')


class BookFullTextAdmin(admin.ModelAdmin):
	list_display = ('book', 'text')
	list_display_links = ('book', 'text')
	search_fields = ('book', )
	exclude = ('update', )



admin.site.register(Book, BookAdmin)
admin.site.register(BookFullText, BookFullTextAdmin)
admin.site.register(get_user_model(), UserAdmin)