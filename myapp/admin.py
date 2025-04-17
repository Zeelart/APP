from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'date')
    search_fields = ('category', 'description')
    list_filter = ('date', 'category')