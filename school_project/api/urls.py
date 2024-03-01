from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (AvailableProductsAPIView, ProductListViewSet,
                       UserLessonsAPIView, buy)


app_name = 'api'
v1_router = DefaultRouter()


v1_router.register(
    'available_products',
    AvailableProductsAPIView,
    basename='available_products'
)
v1_router.register(r'user_lessons/(?P<product_id>\d+)',
                   UserLessonsAPIView, basename='user_lessons')
v1_router.register('products',
                   ProductListViewSet, basename='products')

v1_patterns = [
    path('buy/', buy, name='buy'),
    path('', include(v1_router.urls)),
]


urlpatterns = [
    path('v1/', include(v1_patterns)),
]
