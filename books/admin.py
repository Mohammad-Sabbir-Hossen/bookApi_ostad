"""
admin.py — Book model কে Django এর built-in admin panel এ দেখানোর জন্য
register করা হচ্ছে। এতে http://127.0.0.1:8000/admin/ এ গিয়ে
browser থেকেই বই add/edit/delete করা যাবে (API না দিয়েও, শুধু টেস্টের সুবিধার্থে)।
"""
from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'price', 'published_date']
    list_filter = ['category']
    search_fields = ['title', 'author']
