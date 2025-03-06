from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Expense  

def expense_list(request):
    expenses = Expense.objects.all()
    return JsonResponse([e.to_dict() for e in expenses], safe=False)