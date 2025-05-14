from django.apps import AppConfig  # Добавьте этот импорт

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        try:
            from .models import Category
            if not Category.objects.exists():
                default_categories = [
                    {'name': 'Еда', 'description': 'Продукты питания'},
                    {'name': 'Транспорт', 'description': 'Транспортные расходы'},
                    {'name': 'Жилье', 'description': 'Коммунальные платежи'},
                    {'name': 'Развлечения', 'description': 'Кино, рестораны и т.д.'},
                    {'name': 'Другое', 'description': 'Прочие расходы'},
                ]
                for cat_data in default_categories:
                    Category.objects.get_or_create(
                        name=cat_data['name'],
                        defaults=cat_data
                    )
        except:
            pass