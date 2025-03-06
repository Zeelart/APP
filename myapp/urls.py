from django.urls import path
from . import views

urlpatterns = [
    path('expenses/', views.expense_list, name='expense-list'),
    path('expenses/<int:pk>/', views.expense_detail, name='expense-detail'),
    path('expenses/summary/', views.expense_summary, name='expense-summary'),
    path('expenses/category/<str:category>/', views.expense_by_category, name='expense-by-category'),
    path('expenses/date/<str:date_str>/', views.expense_by_date, name='expense-by-date'),
]