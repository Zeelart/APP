from django.http import JsonResponse, HttpResponse, HttpRequest, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control, never_cache
from django.views.decorators.http import require_http_methods
import json
from .models import Expense

@cache_control(
    private=True,
    max_age=180 * 60,  # 6 часов
    no_cache=True,
    no_site=False
)
def expense_list(request: HttpRequest):
    if request.method == 'GET':
        expenses = Expense.objects.all()
        expenses_list = [expense.to_dict() for expense in expenses]
        return JsonResponse(expenses_list, safe=False)

@cache_control(
    private=True,
    max_age=720 * 60,  # 12 часов
    no_cache=False,
    no_site=False
)
def expense_detail(request: HttpRequest, expense_id: int):
    if request.method == 'GET':
        try:
            expense = Expense.objects.get(id=expense_id)
            return JsonResponse(expense.to_dict())
        except Expense.DoesNotExist:
            raise Http404("Expense not found")

@cache_control(
    private=True,
    max_age=720 * 60,  # 12 часов
    no_cache=True,
    no_site=False
)
def expenses_by_date(request: HttpRequest, date: str):
    if request.method == 'GET':
        expenses = Expense.objects.filter(date=date)
        expenses_list = [expense.to_dict() for expense in expenses]
        return JsonResponse(expenses_list, safe=False)

@cache_control(
    private=True,
    max_age=720 * 60,  # 12 часов
    no_cache=True,
    no_site=False
)
def expenses_by_category(request: HttpRequest, category: str):
    if request.method == 'GET':
        expenses = Expense.objects.filter(category__iexact=category)
        expenses_list = [expense.to_dict() for expense in expenses]
        return JsonResponse(expenses_list, safe=False)

@cache_control(
    private=True,
    max_age=1440 * 60,  # 24 часа
    no_cache=True,
    no_site=False
)
def category_list(request: HttpRequest):
    if request.method == 'GET':
        categories = Expense.objects.values_list('category', flat=True).distinct()
        return JsonResponse(list(categories), safe=False)

@never_cache
@csrf_exempt
def expense_create(request: HttpRequest):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            expense = Expense.objects.create(
                amount=data['amount'],
                category=data['category'],
                description=data.get('description', ''),
                date=data['date']
            )
            
            response_data = expense.to_dict()
            response_data['_links'] = {
                'self': {
                    'type': 'GET',
                    'url': f'{request.build_absolute_uri("/")}expenses/{expense.id}/'
                }
            }
            
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@never_cache
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_expense(request: HttpRequest, expense_id: int):
    try:
        expense = Expense.objects.get(id=expense_id)
        expense.delete()
        return HttpResponse("Expense deleted successfully")
    except Expense.DoesNotExist:
        return Http404("Expense not found")

@never_cache
@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_expense(request: HttpRequest, expense_id: int):
    try:
        expense = Expense.objects.get(id=expense_id)
        data = json.loads(request.body)
        
        if 'amount' in data:
            expense.amount = data['amount']
        if 'category' in data:
            expense.category = data['category']
        if 'description' in data:
            expense.description = data['description']
        if 'date' in data:
            expense.date = data['date']
            
        expense.save()
        return JsonResponse(expense.to_dict())
    except Expense.DoesNotExist:
        raise Http404("Expense not found")
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)