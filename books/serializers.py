"""
serializers.py — এইখানে "translation" হয়:
  Python object (Book model instance)  <-->  JSON (যেটা client পাঠায়/পায়)

GET request এর সময়: Book object -> JSON  (serialization)
POST/PUT request এর সময়: JSON -> Book object -> database এ save (deserialization)
এছাড়াও validation ও এখানে হয় (যেমন price ঋণাত্মক হলে error দেওয়া)।
"""
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # কোন কোন field API তে দেখানো/নেওয়া হবে
        fields = ['id', 'title', 'author', 'category', 'price', 'published_date']

    def validate_price(self, value):
        # extra validation: price ০ বা ঋণাত্মক হতে পারবে না
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
