from django.contrib import admin
from .models import Bank, Department, Employee

admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Bank)
