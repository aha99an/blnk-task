from django.contrib import admin

from .models import Balance
from solo.admin import SingletonModelAdmin


admin.site.register(Balance, SingletonModelAdmin)
