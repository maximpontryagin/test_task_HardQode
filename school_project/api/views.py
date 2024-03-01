from rest_framework import status, viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Count

from api.permissions import AdminOrReadOnly
from product.models import Product, Lesson, Group, AccessUser
from api.serializers import (
    ProductListSerializer,
    ProductAddSerializer,
    GroupSerializer,
    UserBuyAccessSerializer,
    LessonSerializer
    )


class ProductViewSet(viewsets.ModelViewSet):
    """Создание продукта и весь их список."""

    queryset = Product.objects.all()
    serializer_class = ProductAddSerializer
    permission_classes = (AdminOrReadOnly, )


class AvailableProductsAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Список доступных для покупки продуктов."""

    permission_classes = (IsAuthenticated, )
    serializer_class = ProductListSerializer

    def get_queryset(self):
        user = self.request.user
        products_without_access = Product.objects.exclude(
            accessuser__user=user)
        queryset = products_without_access.annotate(
            num_lessons=Count('lessons'))
        return queryset


class GroupViewSet(viewsets.ModelViewSet):
    """Создание группы для продукта и их список."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminUser, )


class LessonViewSet(viewsets.ModelViewSet):
    """Создание Уроков для продукта и их список."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAdminUser, )


@api_view(['POST'])
@permission_classes([AllowAny])
def buy(request):
    """Пользователь покупает продукт и получает к нему доступ.
    После этого пользователя распределяет в учебную группу продукта."""
    serializer = UserBuyAccessSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    product_id = serializer.data.get('product')
    user_id = serializer.data.get('user')
    AccessUser.objects.create(
        product_id=product_id,
        user_id=user_id,
        access=1
    )

    product = Product.objects.get(pk=product_id)
    groups = Group.objects.filter(product=product)
    sorted_groups = groups.annotate(
        num_users=Count('users')).order_by('num_users')
    num_users_per_group = [group.users.count() for group in sorted_groups]
    max_users = product.max_users_in_group
    for i, group in enumerate(sorted_groups):
        if num_users_per_group[i] < max_users:
            group.users.add(user_id)
            break
    return Response(serializer.data, status=status.HTTP_200_OK)
