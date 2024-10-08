from django.db import models

from shop.models import Products


class Order(models.Model):
    first_name = models.CharField(max_length=50,verbose_name='Имя')
    last_name = models.CharField(max_length=50,verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(max_length=250,verbose_name='Адрес')
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100,verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True,verbose_name='Дата обновлен')
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,verbose_name='Заказ',
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name='Товар', related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,verbose_name='Цена',
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1,verbose_name='Колличество',)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
