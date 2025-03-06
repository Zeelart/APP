from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import Expense
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def expense_list(request):
    if request.method == "GET":
        expenses = Expense.objects.all()
        return JsonResponse([e.to_dict() for e in expenses], safe=False)
    
    elif request.method == "POST":
        data = json.loads(request.body)
        required_fields = ['amount', 'category']
        
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        try:
            expense = Expense.objects.create(
                amount=data['amount'],
                category=data['category'],
                description=data.get('description', ''),
                date=datetime.strptime(data.get('date'), '%Y-%m-%d').date() 
                    if data.get('date') else None
            )
            return JsonResponse(expense.to_dict(), status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def expense_detail(request, pk):
    try:
        expense = Expense.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    
    if request.method == "GET":
        return JsonResponse(expense.to_dict())
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        for field in ['amount', 'category', 'description']:
            if field in data:
                setattr(expense, field, data[field])
        if 'date' in data:
            expense.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        expense.save()
        return JsonResponse(expense.to_dict())
    
    elif request.method == "DELETE":
        expense.delete()
        return HttpResponse(status=204)

def expense_summary(request):
    period = request.GET.get('period', 'month').lower()
    today = timezone.now().date()
    
    if period == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif period == 'year':
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)
    else:
        start_date = today.replace(day=1)
        next_month = start_date.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)
    
    total = Expense.objects.filter(
        date__range=(start_date, end_date)
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    return JsonResponse({
        'period': period,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'total': float(total)
    })

def expense_by_category(request, category):
    expenses = Expense.objects.filter(category=category)
    return JsonResponse([e.to_dict() for e in expenses], safe=False)

def expense_by_date(request, date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    
    expenses = Expense.objects.filter(date=date)
    return JsonResponse([e.to_dict() for e in expenses], safe=False)