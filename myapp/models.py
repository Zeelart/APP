from django.db import models

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.date})"

    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount),
            'category': self.category,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None
        }