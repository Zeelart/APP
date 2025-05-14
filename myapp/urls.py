from django.urls import path
from .views import ExpenseAPIView, CategoryAPIView

urlpatterns = [
    # Для расходов
    path("expenses/", ExpenseAPIView.as_view(), name="expense_api"),
    path("expenses/<int:pk>/", ExpenseAPIView.as_view(), name="expense_detail_api"),
    
    # Для категорий
    path("categories/", CategoryAPIView.as_view(), name="category_api"),
    path("categories/<int:pk>/", CategoryAPIView.as_view(), name="category_detail_api"),
    
    # Дополнительные фильтры
    path("expenses/by_date/<str:date>/", ExpenseAPIView.as_view(), name="expenses_by_date"),
    path("expenses/by_category/<str:category>/", ExpenseAPIView.as_view(), name="expenses_by_category"),
]