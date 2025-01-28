from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Expense(models.Model):
    CATEGORY = [
        ('electricity', 'ток'),
        ('water', 'вода'),
        ('mobile', 'телефон'),
        ('heating', 'топлофикация'),
        ('food', 'храна'),
        ('fuel-car', 'гориво-кола'),
        ('fuel-moto', 'гориво-мотор'),
        ('entertainment', 'забавление'),
        ('orders', 'поръчки'),
        ('other', 'друго'),
        ('mortgage', 'ипотека'),
        ('loan', 'потребителски'),
        ('car-parts', 'части за колата'),
        ('moto-parts', 'части за мотора'),
        ('cash', 'теглене кеш'),
        ('revolut', 'револют'),
        ('saving', 'спестяване')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY, blank=True, null=True)  # Use CharField for choices
    comment = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.category} - {self.date} - {self.amount}"