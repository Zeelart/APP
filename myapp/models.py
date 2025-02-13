from django.db import models
from django.utils import timezone

class Expense(models.Model):
    # Поля модели
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма расхода
    category = models.CharField(max_length=100)  # Категория расхода
    description = models.TextField(blank=True, null=True)  # Описание (необязательное поле)
    date = models.DateTimeField(default=timezone.now)  # Дата расхода (по умолчанию текущая)

    def __str__(self):
        return f"{self.category} - {self.amount} руб. ({self.date.strftime('%Y-%m-%d')})"