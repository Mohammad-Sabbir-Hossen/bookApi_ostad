"""
books/urls.py — ModelViewSet ব্যবহার করলে DRF এর "Router" দিয়ে
সব URL pattern (list, detail, create, update, delete) automatic বানানো যায়,
নিজে হাতে path() লিখতে হয় না।

router.register('books', BookViewSet) করলেই নিচের সব URL তৈরি হয়ে যায়:
  GET/POST         /books/
  GET/PUT/PATCH/DELETE  /books/<id>/
"""
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = router.urls
