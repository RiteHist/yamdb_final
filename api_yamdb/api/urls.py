from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from api.views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews'
                r'/(?P<review_id>\d+)/comments', CommentsViewSet,
                basename='comments')
router.register('users', UserViewSet)
urlpatterns = [
    path('v1/', include(router.urls)),
]
