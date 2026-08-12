"""
models.py = "ডাটাবেজের ব্লুপ্রিন্ট"।
এখানে যে class বানাবে, Django সেটাকে ডাটাবেজের একটা TABLE বানিয়ে দেবে।
প্রতিটা field (CharField, DecimalField...) টেবিলের একটা COLUMN হয়ে যায়।

Book class বানানোর পর যখন `makemigrations` আর `migrate` কমান্ড চালাবে,
তখন Django আসলেই "books_book" নামে একটা SQL table বানিয়ে ফেলবে।
"""
from django.db import models


class Book(models.Model):
    # ছোট টেক্সট এর জন্য CharField, max_length বাধ্যতামূলক
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)

    # টাকার মতো decimal সংখ্যার জন্য FloatField এর বদলে DecimalField ব্যবহার
    # করা ভালো (floating point precision সমস্যা এড়াতে)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    published_date = models.DateField()

    # id ফিল্ড আলাদা করে লিখতে হয় না — Django নিজে থেকেই একটা
    # auto-incrementing primary key "id" বানিয়ে দেয়।

    def __str__(self):
        # admin panel বা shell এ Book object টা কীভাবে দেখাবে তা ঠিক করে
        return f"{self.title} by {self.author}"

    class Meta:
        ordering = ['id']  # ডিফল্টভাবে id অনুযায়ী সাজানো থাকবে
