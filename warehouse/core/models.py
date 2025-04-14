from django.db import models
from django.utils.translation import gettext_lazy as _

from warehouse.users.models import Supplier, User


class Product(models.Model):
    product_name = models.CharField(verbose_name=_("Name of product"), max_length=255)
    cost = models.DecimalField(verbose_name=_("Cost of one product"), max_digits=20, decimal_places=2)
    description = models.TextField(verbose_name=_("Description of product"))
    total_quantity = models.IntegerField(verbose_name=_("Total count of product in warehouse"), default=0)
    supplier = models.ForeignKey(Supplier,verbose_name=_("Supplier of product"), on_delete=models.PROTECT)

    def increase(self, quantity: int):
        self.total_quantity += quantity
        self.save()

    def decrease(self, quantity: int):
        self.total_quantity -= quantity
        self.save()

    def __str__(self):
        return f"{self.product_name} - {self.total_quantity}"


class Order(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=_("Customer of order"), on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="OrderItem")
    is_confirmed = models.BooleanField(verbose_name=_("Confirmation of order"), default=False)

    def __str__(self):
        return f"{self.user.username} - {self.date_created}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

