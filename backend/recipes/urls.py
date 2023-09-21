from rest_framework import routers
from django.urls import path, include

from .views import TagViewSet


router = routers.SimpleRouter()
router.register('tags', TagViewSet, 'tags')

urlpatterns = [
    path('', include(router.urls)),
]
