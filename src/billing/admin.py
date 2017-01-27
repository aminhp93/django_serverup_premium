from django.contrib import admin

# Register your models here.
from .models import Membership, Transaction

admin.site.register(Membership)
admin.site.register(Transaction)