"""
filters.py — django-filter লাইব্রেরি ব্যবহার করে আমরা বলে দিচ্ছি
কোন কোন query parameter দিয়ে filter করা যাবে।

/books/?category=Programming  -> category exact match করবে
/books/?author=Rowling        -> author exact match করবে

চাইলে এখানে icontains (case-insensitive partial match) ও ব্যবহার করা যায়,
নিচে দেখানো হলো।
"""
import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    # exact match এর বদলে "contains" টাইপ filter দিলে ব্যবহারকারীর জন্য সুবিধা হয়
    # যেমন category=Prog লিখলেও "Programming" match করবে
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['category', 'author']
