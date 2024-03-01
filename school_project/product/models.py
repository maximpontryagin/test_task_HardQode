from django.contrib.auth import get_user_model

from django.db import models


User = get_user_model()


class Product(models.Model):
    """Модель продукта."""

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='author_products')
    title = models.TextField(verbose_name='Название')
    start_datetime = models.DateTimeField('Дата и время старта продукта')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='цена в рублях')
    max_users_in_group = models.IntegerField(
        verbose_name='Максимальное количество людей в 1 группе')
    min_users_in_group = models.IntegerField(
        verbose_name='Минимальное количество людей в 1 группе')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.TextField(verbose_name='Название')
    video_url = models.URLField(max_length=500)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='lessons')


class Group(models.Model):
    title = models.TextField(verbose_name='Название группы')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Продукт',
                                related_name='groups')
    users = models.ManyToManyField(User, blank=False)


class AccessUser(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Продукт')
    access = models.BooleanField(default=True,
                                 verbose_name=('Разрешить/запретить \n'
                                               'доступ к продукту'))

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Покупатель')

    def __str__(self):
        return self.product
