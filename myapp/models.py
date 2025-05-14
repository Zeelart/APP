from django.db import models
from django.core.exceptions import ValidationError

def validate_positive(value):
    if value <= 0:
        raise ValidationError('Сумма должна быть положительной')

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive])
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='expenses')
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount} ({self.date})"

    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount),
            'category': self.category.to_dict(),
            'description': self.description,
            'date': self.date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def clean(self):
        if self.date and self.date.year < 2000:
            raise ValidationError('Дата не может быть раньше 2000 года')