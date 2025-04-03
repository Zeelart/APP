from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_cntrol, never_cache
from django.views.decorators.cache import csrf_exempt
from .models import Expense  
import json

#def expense_list(request):
 #   expenses = Expense.objects.all()
  #  return JsonResponse([e.to_dict() for e in expenses], safe=False)

@cache_cntrol(
    private = True,
    max_age = 15 * 60,
    no_cache = True,
    no_siste = False
) 
def expense_list(request):
    if request.method == 'GET':
        expenses = Expense.objects.all()
        data = [expense.to_dict() for expense in expenses]
        return JsonResponse(data, safe=False)
@never_cache     

@csrf_exempt  
def expense_create(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)  
            amount = body.get('amount')
            category = body.get('category')
            description = body.get('description', '')
            date = body.get('date')


            if not amount or not category or not date:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            expense = Expense(
                amount=amount,
                category=category,
                description=description,
                date=date
            )
            expense.full_clean() 
            expense.save()

            return JsonResponse(expense.to_dict(), status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)