from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import json
from datetime import datetime
from .models import Expense, Category

@method_decorator(csrf_exempt, name='dispatch')
class ExpenseAPIView(View):
    
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            try:
                expense = Expense.objects.get(id=pk)
                return JsonResponse(expense.to_dict())
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Expense not found"}, status=404)
        
        expenses = Expense.objects.all()
        
        # Фильтрация
        if 'date' in request.GET:
            try:
                date_obj = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
                expenses = expenses.filter(date=date_obj)
            except ValueError:
                return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
        
        if 'category_id' in request.GET:
            try:
                expenses = expenses.filter(category_id=int(request.GET['category_id']))
            except ValueError:
                return JsonResponse({"error": "Category ID must be integer"}, status=400)
        
        return JsonResponse([e.to_dict() for e in expenses], safe=False)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            # Валидация
            required_fields = ['amount', 'category_id', 'date']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({"error": f"Field '{field}' is required"}, status=400)
            
            try:
                category = Category.objects.get(id=data['category_id'])
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Category not found"}, status=404)
            
            with transaction.atomic():
                expense = Expense.objects.create(
                    amount=data['amount'],
                    category=category,
                    description=data.get('description', ''),
                    date=datetime.strptime(data['date'], '%Y-%m-%d').date()
                )
                
                response_data = expense.to_dict()
                response_data['_links'] = {
                    'self': {
                        'type': 'GET',
                        'url': f'/api/expenses/{expense.id}/'
                    }
                }
                
                return JsonResponse(response_data, status=201)
                
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def put(self, request, pk=None, *args, **kwargs):
        if not pk:
            return JsonResponse({"error": "Expense ID required"}, status=400)
        
        try:
            data = json.loads(request.body)
            expense = Expense.objects.get(id=pk)
            
            # Обновление полей
            if 'amount' in data:
                expense.amount = data['amount']
            if 'date' in data:
                expense.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            if 'description' in data:
                expense.description = data['description']
            if 'category_id' in data:
                try:
                    expense.category = Category.objects.get(id=data['category_id'])
                except ObjectDoesNotExist:
                    return JsonResponse({"error": "Category not found"}, status=404)
            
            expense.save()
            return JsonResponse(expense.to_dict())
            
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Expense not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request, pk=None, *args, **kwargs):
        if not pk:
            return JsonResponse({"error": "Expense ID required"}, status=400)
        
        try:
            expense = Expense.objects.get(id=pk)
            expense.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Expense not found"}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryAPIView(View):
    
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            try:
                category = Category.objects.get(id=pk)
                return JsonResponse(category.to_dict())
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Category not found"}, status=404)
        
        categories = Category.objects.all()
        return JsonResponse([c.to_dict() for c in categories], safe=False)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            if 'name' not in data or not data['name'].strip():
                return JsonResponse({"error": "Field 'name' is required"}, status=400)
            
            if Category.objects.filter(name__iexact=data['name'].strip()).exists():
                return JsonResponse({"error": "Category already exists"}, status=400)
            
            category = Category.objects.create(
                name=data['name'].strip(),
                description=data.get('description', '').strip()
            )
            
            return JsonResponse(category.to_dict(), status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def put(self, request, pk=None, *args, **kwargs):
        if not pk:
            return JsonResponse({"error": "Category ID required"}, status=400)
        
        try:
            data = json.loads(request.body)
            category = Category.objects.get(id=pk)
            
            if 'name' in data:
                new_name = data['name'].strip()
                if Category.objects.exclude(id=pk).filter(name__iexact=new_name).exists():
                    return JsonResponse({"error": "Category name already taken"}, status=400)
                category.name = new_name
            
            if 'description' in data:
                category.description = data['description'].strip()
            
            category.save()
            return JsonResponse(category.to_dict())
            
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Category not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request, pk=None, *args, **kwargs):
        if not pk:
            return JsonResponse({"error": "Category ID required"}, status=400)
        
        try:
            category = Category.objects.get(id=pk)
            
            if Expense.objects.filter(category=category).exists():
                return JsonResponse(
                    {"error": "Cannot delete category with linked expenses"}, 
                    status=400
                )
                
            category.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Category not found"}, status=404)