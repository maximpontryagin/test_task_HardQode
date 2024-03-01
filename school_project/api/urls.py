from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (AvailableProductsAPIView, GroupViewSet, LessonViewSet,
                       ProductViewSet, buy)

app_name = 'api'
v1_router = DefaultRouter()

v1_router.register('products', ProductViewSet, basename='products')
v1_router.register('groups', GroupViewSet, basename='groups')
v1_router.register('products_list',
                   AvailableProductsAPIView, basename='products_list')
v1_router.register('add_lesson', LessonViewSet, basename='add_lesson')

v1_patterns = [
    path('buy/', buy, name='buy'),
    path('', include(v1_router.urls)),
]


urlpatterns = [
    path('v1/', include(v1_patterns)),
]
