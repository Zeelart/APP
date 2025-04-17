from django.urls import path
from .views import (
    expense_list, expense_detail, expense_create,
    delete_expense, update_expense,
    expenses_by_date, expenses_by_category,
    category_list
)

urlpatterns = [
    
    path('expenses/', expense_list, name='expense-list'),
    path('expenses/create/', expense_create, name='expense-create'),
    path('expenses/<int:expense_id>/', expense_detail, name='expense-detail'),
    path('expenses/<int:expense_id>/delete/', delete_expense, name='expense-delete'),
    path('expenses/<int:expense_id>/update/', update_expense, name='expense-update'),
    
    
    path('expenses/by_date/<str:date>/', expenses_by_date, name='expenses-by-date'),
    path('expenses/by_category/<str:category>/', expenses_by_category, name='expenses-by-category'),
    path('expenses/categories/', category_list, name='category-list'),
]