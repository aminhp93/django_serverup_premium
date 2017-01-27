import random

from django.shortcuts import render

# Create your views here.

from .models import Transaction

def upgrade(request):
	Transaction.objects.create_new(request.user, "afsdaf{}".format(random.randint(1,100)), 25.00, "visa")
	context = {
	
	}
	return render(request, "upgrade.html", context)

def billing_history(request):
	history = Transaction.objects.filter(user=request.user).filter(success=True)
	context = {
		"history": history
	}
	return render(request, "history.html", context)	