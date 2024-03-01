from rest_framework import serializers
from django.utils import timezone

from product.models import Product, Lesson, Group, AccessUser
from django.db.models import Count


class ProductListSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения списка продуктов доступных для
    покупки и отображения всей информации о них включая количество уроков"""

    author = serializers.StringRelatedField(read_only=True)
    num_lessons = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Product
        fields = '__all__'


class ProductAddSerializer(serializers.ModelSerializer):
    """Сериализатор для создания продуктов"""

    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        datetime_start_product = data.get('start_datetime')
        if timezone.now() < datetime_start_product:
            raise Exception(
                'Нельзя начать продукт в прошедшем времени'
            )
        return data

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('title', 'product')

    # def validate(self, data):
    #     groups = Group.objects.filter(product=data.get('product'))
    #     for group in groups:
    #         if group.users == data.get('users')[0]:
    #             raise Exception('Данный пользователь уже находится'
    #                             'в другой группе по этому продукту')

    #     if groups.filter(product=data.get('product'),
    #                      title=data.get('title')).exists():
    #         raise Exception('В данном продукте группа с таким названием'
    #                         'уже существует. Придумаете новое название')
    #     return data


    def validate(self, data):
        # if Group.objects.filter(product=data.get('product'),
        #                         users=data.get('users')[0]).exists():
        #     raise Exception('Данный пользователь уже находится'
        #                     'в другой группе по этому продукту')
        if Group.objects.filter(product=data.get('product'),
                                title=data.get('title')).exists():
            raise Exception('В данном продукте группа с таким названием'
                            'уже существует. Придумаете новое название')
        return data


class UserBuyAccessSerializer(serializers.ModelSerializer):
    """Сериализатор для покупки продукта аутенфицированным пользователем"""

    class Meta:
        model = AccessUser
        fields = ('product', 'user')

    def validate(self, data):
        user_id = data.get('user')
        product_id = data.get('product').id
        if AccessUser.objects.filter(
            user=user_id,
            product=product_id,
            access=1
        ).exists():
            raise serializers.ValidationError('Вы уже купили данный продукт')

        groups = Group.objects.filter(product=product_id)
        sorted_groups = groups.annotate(
            num_users=Count('users')).order_by('num_users')
        num_users_per_group = [group.users.count() for group in sorted_groups]
        summa = sum(num_users_per_group)
        product = Product.objects.get(id=product_id)
        max_users = product.max_users_in_group
        max_users_in_groups = max_users * len(num_users_per_group)

        if summa >= max_users_in_groups:
            raise serializers.ValidationError(
                ('В группах данного продукта закончились места,'
                  'создайте еще 1 новую группу'))

        datetime_start_product = data.get('start_datetime')
        if timezone.now() > datetime_start_product:
            raise Exception(
                'Проект уже начался, добавляться в группы уже нельзя'
            )
        return data


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    class Meta:
        model = Lesson
        fields = '__all__'



    #     user_id = data.get('user')
    #     product_id = data.get('product')
    #     if AccessUser.objects.filter(user=user_id,
    #                                  product=product_id,
    #                                  access=1).exists():
    #         raise Exception('Вы уже купили данный продукт')

    # #     groups = Group.objects.filter(product=product_id)
    # #     sorted_groups = groups.annotate(num_users=Count('users')).order_by('num_users')
    # # # Получаем количество участников в каждой группе
    # #     num_users_per_group = [group.users.count() for group in sorted_groups]
    # #     summa = sum(num_users_per_group)
    # #     #НАДО РАСШИРИТЬ ВАЛИДАЦИЮ НА ТО ЧТО КОНЧИЛИСЬ МЕСТА В ГРУППАХ
    # #     product = Product.objects.get(pk=data.get('product').id).max_users_in_group
    # #     max_users_in_groups = product * len(num_users_per_group)
    # #     if summa > max_users_in_groups:
    # #         raise Exception('В группах данного продукта закончились места,'
    # #                         'создайте еще 1 новую группу')
    # #     return data