from django.urls import path
from . import views

urlpatterns = [
    path('expenses/', views.expense_list, name='expense-list')
]