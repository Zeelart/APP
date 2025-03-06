from django.db import models
from django.utils import timezone

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount),
            'category': self.category,
            'description': self.description,
            'date': self.date.strftime('%Y-%m-%d')
        }