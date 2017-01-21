from django.db import models
from django.conf import settings

# Create your models here.
from .signals import notify


class Notification(models.Model):
	# sender = models.ForeignKey()
	recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications")
	action = models.CharField(max_length=255)

	timestamp = models.DateTimeField(auto_now_add = True, auto_now=False)

	def __str__(self):
		return str(self.action)

def new_notification(sender, recipient, action, *args, **kwargs):
	print(args)
	print(kwargs)
	if recipient is None:
		recipient = 0
	else:
		new_notification_create = Notification.objects.create(recipient=recipient, action=action)




notify.connect(new_notification)