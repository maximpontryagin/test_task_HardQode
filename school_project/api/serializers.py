from django.db.models import Count
from django.utils import timezone
from rest_framework import serializers

from product.models import AccessUser, Group, Lesson, Product, User


class ProductListSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения списка продуктов доступных для
    покупки и отображения всей информации о них включая количество уроков."""

    author = serializers.StringRelatedField(read_only=True)
    num_lessons = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Product
        fields = '__all__'


class UserBuyAccessSerializer(serializers.ModelSerializer):
    """Сериализатор для покупки продукта аутенфицированным пользователем."""

    class Meta:
        model = AccessUser
        fields = ('product', )

    def validate(self, data):
        user_id = self.context['request'].user
        product_id = data.get('product').id
        if AccessUser.objects.filter(
            user=user_id,
            product=product_id,
            access=1
        ).exists():
            raise serializers.ValidationError('Вы уже купили данный продукт')
        sorted_groups = Group.objects.filter(product=product_id).annotate(
            num_users=Count('users')).order_by('num_users')
        num_users_per_group = [group.users.count() for group in sorted_groups]
        summa = sum(num_users_per_group)
        product = Product.objects.get(id=product_id)
        max_users_in_all_groups = (product.max_users_in_group
                                   * len(num_users_per_group))

        if summa >= max_users_in_all_groups:
            raise serializers.ValidationError(
                ('В группах данного продукта закончились места,'
                 'обратитесь в поддержку что бы создали новую группу'))

        datetime_start_product = product.start_datetime
        if timezone.now() > datetime_start_product:
            raise serializers.ValidationError(
                'Проект уже начался, добавляться в группы уже нельзя'
            )
        return data


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков отображения уроков
    по конкретному продукту доступному пользователю."""

    class Meta:
        model = Lesson
        fields = '__all__'


class ProductInfoSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения списка всех
    продуктов на платформе с дополнительными полями (доп задание)."""

    num_students = serializers.SerializerMethodField()
    group_fill_percentage = serializers.SerializerMethodField()
    product_purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_num_students(self, obj):
        num_students = AccessUser.objects.filter(product=obj).count()
        return num_students

    def get_group_fill_percentage(self, obj):
        groups = Group.objects.filter(product=obj)
        total_groups = len(groups)
        filled_groups = groups.annotate(
            num_users=Count('users')).filter(num_users__gt=0)
        if total_groups == 0:
            fill_percentage = 0
        else:
            fill_percentage = (filled_groups.count() / total_groups) * 100
        return fill_percentage

    def get_product_purchase_percentage(self, obj):
        total_users = User.objects.count()
        access_users = AccessUser.objects.filter(product=obj).count()
        purchase_percentage = (access_users / total_users) * 100
        return purchase_percentage
