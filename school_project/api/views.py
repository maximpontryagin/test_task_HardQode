from django.db.models import Count
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import (LessonSerializer, ProductInfoSerializer,
                             ProductListSerializer, UserBuyAccessSerializer)
from product.models import AccessUser, Group, Lesson, Product


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


class UserLessonsAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Выделение списка уроков по конкретному продукту
    к которому пользователь имеет доступ."""

    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        product = Product.objects.select_related(
            'author').prefetch_related('lessons').get(id=product_id)
        if not product.accessuser_set.filter(
             user=self.request.user, access=True).exists():
            return Lesson.objects.none()
        lessons = product.lessons.all()

        return lessons


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy(request):
    """Пользователь покупает продукт и получает к нему доступ.
    После этого пользователя распределяет в учебную группу продукта."""
    serializer = UserBuyAccessSerializer(data=request.data,
                                         context={'request': request})
    serializer.is_valid(raise_exception=True)
    product_id = serializer.validated_data['product'].id
    user_id = request.user.id
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


class ProductListViewSet(viewsets.ReadOnlyModelViewSet):
    """отображения списка всех продуктов на платформе
    с дополнительными полями (доп задание)."""
    queryset = Product.objects.all()
    serializer_class = ProductInfoSerializer
