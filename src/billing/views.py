import random

from django.shortcuts import render

# Create your views here.

from .models import Transaction, Membership
from .signals import membership_dates_update


def upgrade(request):
	if request.user.is_authenticated():
		trans = Transaction.objects.create_new(request.user, "afsdaf{}".format(random.randint(1,100)), 25.00, "visa")
		if trans.success:
			membership_instance, created = Membership.objects.get_or_create(user=request.user)
			membership_dates_update.send(membership_instance, new_date_start=trans.timestamp)
	context = {
	
	}
	return render(request, "upgrade.html", context)

def billing_history(request):
	history = Transaction.objects.filter(user=request.user).filter(success=True)
	context = {
		"history": history
	}
	return render(request, "history.html", context)	