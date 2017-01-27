import random

from django.shortcuts import render

# Create your views here.

from .models import Transaction, Membership, UserMerchantId
from .signals import membership_dates_update
import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="gf7vc7vvr5ttnby8",
                                  public_key="xdm372xh9cyj8p4n",
                                  private_key="ac011869ffcf8f1c03a3b5696c5ebc8a")

PLAN_ID = "monthly_plan"

def upgrade(request):
	client_token = braintree.ClientToken.generate()

	if request.user.is_authenticated():
		try:
			# something to get the current customer id stored somewhere
			merchant_customer_id = UserMerchantId.objects.get(user=request.user).customer_id
		except UserMerchantId.DoesNotExist:
			new_customer_result = braintree.Customer.create({})
			if new_customer_result.is_success:
				merchant_customer_id = UserMerchantId.objects.create(user=request.user)
				merchant_customer_id.customer_id = new_customer_result.customer.id
				merchant_customer_id.save()

				print("Customer created with ID = {}".format(new_customer_result.customer.id))
			else:
				print("Error {}".format(new_customer_result.message))
				# redirect somewhere?
		except:
			# some other errors
			pass

		trans = Transaction.objects.create_new(request.user, "afsdaf{}".format(random.randint(1,100)), 25.00, "visa")
		if trans.success:
			membership_instance, created = Membership.objects.get_or_create(user=request.user)
			membership_dates_update.send(membership_instance, new_date_start=trans.timestamp)
	context = {
		"client_token": client_token,
	}
	return render(request, "upgrade.html", context)

def billing_history(request):
	history = Transaction.objects.filter(user=request.user).filter(success=True)
	context = {
		"history": history
	}
	return render(request, "history.html", context)	