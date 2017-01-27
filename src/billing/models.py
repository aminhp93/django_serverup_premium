import random
import datetime
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save

from .signals import membership_dates_update

# Create your models here.
class Membership(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	date_start = models.DateTimeField(default=timezone.now(), verbose_name="Start date")
	date_end = models.DateTimeField(default=timezone.now(), verbose_name="End date")

	def __str__(self):
		return str(self.user.username)

	def update_status(self):
		if self.date_end >= timezone.now():
			self.user.is_member = True
			self.user.save()
		elif self.date_end < timezone.now():
			self.user.is_member = False
			self.user.save()
		else:
			pass


def update_membership_status(sender, instance, created, **kwargs):
	if not created:
		instance.update_status()

post_save.connect(update_membership_status, sender=Membership)

def update_membership_dates(sender, new_date_start, **kwargs):
	membership = sender
	current_date_end = membership.date_end

	if current_date_end > new_date_start:
		# append new start date plus offset ot date end of the instance
		membership.date_end = current_date_end + datetime.timedelta(days=30, hours=10)
		membership.save()

	else:
		# set a new start date and new end date with the same offset.
		membership.date_start = new_date_start
		membership.date_end = new_date_start + datetime.timedelta(days=30, hours=10)
		membership.save()

	membership.update_status()

membership_dates_update.connect(update_membership_dates)

class TransactionManager(models.Manager):
	def create_new(self, user, transaction_id, amount, card_type, success=None, transaction_status=None, last_four=None):
		if not user:
			raise ValueError("Must be a user")
		if not transaction_id:
			raise ValueError("Must complete transaction to add new")

		new_order_id = "{}{}{}".format(transaction_id[:2], random.randint(1,9), transaction_id[2:])
		new_trans = self.model(
			user = user,
			transaction_id = transaction_id,
			order_id = new_order_id,
			amount = amount,
			card_type = card_type,
			)
		new_trans.save(using=self._db)

		if success is not None:
			new_trans.success = success
			new_trans.transaction_status = transaction_status
			
		if last_four is not None:
			new_trans.last_four = last_four

		new_trans.save(using=self._db)
		return new_trans

class Transaction(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	transaction_id = models.CharField(max_length=120) #braintree or stripe
	order_id = models.CharField(max_length=120)
	amount = models.DecimalField(max_digits=100, decimal_places=2)
	success = models.BooleanField(default=True)
	transaction_status = models.CharField(max_length=220, null=True, blank=True)
	card_type = models.CharField(max_length=120)
	last_four = models.PositiveIntegerField(null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	objects = TransactionManager()

	def __str__(self):
		return self.order_id

	class Meta:
		ordering = ['-timestamp']
