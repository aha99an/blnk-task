from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from users.models import User
from funds.models import Fund
from loans.models import Loan

def create_banker_group():

    add_fund = Permission.objects.get(codename="add_fund")
    update_fund = Permission.objects.get(codename="change_fund")
    delete_fund = Permission.objects.get(codename="delete_fund")
    view_fund = Permission.objects.get(codename="view_fund")
    
    add_loan = Permission.objects.get(codename="add_loan")
    update_loan = Permission.objects.get(codename="change_loan")
    delete_loan = Permission.objects.get(codename="delete_loan")
    view_loan = Permission.objects.get(codename="view_loan")
    
    banker_permissions = [
        add_fund, update_fund, delete_fund, view_fund,
        add_loan, update_loan, delete_loan, view_loan,
    ]

    customer_group = Group.objects.create(name='Banker')
    customer_group.permissions.set(banker_permissions)

def create_provider_group():
    add_providerfund = Permission.objects.get(codename="add_providerfund")
    update_providerfund = Permission.objects.get(codename="change_providerfund")
    delete_providerfund = Permission.objects.get(codename="delete_providerfund")
    view_providerfund = Permission.objects.get(codename="view_providerfund")
    

    providerfund_permissions = [
        add_providerfund, update_providerfund, delete_providerfund, view_providerfund,
    ]

    customer_group = Group.objects.create(name='Provider')
    customer_group.permissions.set(providerfund_permissions)
       

def create_customer_group():
    add_customerloan = Permission.objects.get(codename="add_customerloan")
    update_customerloan = Permission.objects.get(codename="change_customerloan")
    delete_customerloan = Permission.objects.get(codename="delete_customerloan")
    view_customerloan = Permission.objects.get(codename="view_customerloan")
    

    customerloan_permissions = [
        add_customerloan, update_customerloan, delete_customerloan, view_customerloan,
    ]

    customer_group = Group.objects.create(name='Customer')
    customer_group.permissions.set(customerloan_permissions)

def create_sample_users():

    customer_group = Group.objects.get(name='Customer') 
    provider_group = Group.objects.get(name='Provider') 
    banker_group = Group.objects.get(name='Banker') 

    customer = User.objects.create(username="customer", user_type="customer", is_staff=True)
    customer.set_password("Ahmed1153")
    customer.save()
    customer_group.user_set.add(customer)

    provider = User.objects.create(username="provider", user_type="provider", is_staff=True)
    provider.set_password("Ahmed1153")
    provider.save()
    provider_group.user_set.add(provider)

    banker = User.objects.create(username="banker", user_type="banker", is_staff=True)
    banker.set_password("Ahmed1153")
    banker.save()
    banker_group.user_set.add(banker)


class Command(BaseCommand):
    help = 'Create default groups'


    def handle(self, *args, **kwargs):
        create_banker_group()
        create_provider_group()
        create_customer_group()
        create_sample_users()

        self.stdout.write("Created default users and permissions")
