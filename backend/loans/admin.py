from django.contrib import admin
from .models import Loan, CustomerLoan


admin.site.register(Loan)
admin.site.register(CustomerLoan)
