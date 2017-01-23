from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.conf import settings

# Create your models here.
from .signals import notify

class NotificationQuerySet(models.query.QuerySet):
	def get_user(self, user):
		return self.filter(recipient=user)

	def mark_targetless(self, recipient):
		qs = self.unread().get_user(recipient)
		qs_no_target = qs.filter(target_object_id=None)
		if qs_no_target:
			qs_no_target.update(read=True)

	def mark_all_read(self, recipient):
		qs = self.unread().get_user(recipient)
		qs.update(read=True)

	def mark_all_unread(self, recipient):
		qs = self.read().get_user(recipient)
		qs.update(read=False)

	def unread(self):
		return self.filter(read=False)

	def read(self):
		return self.filter(read=True)

	def recent(self):
		return self.unread()[:5]

class NotificationManager(models.Manager):
	def get_queryset(self):
		return NotificationQuerySet(self.model, using=self._db)

	def all_unread(self, user):
		return self.get_queryset().get_user(user).unread()

	def all_read(self, user):
		return self.get_queryset().get_user(user).read()

	def all_for_user(self, user):
		# self.get_queryset().mark_all_unread(user)
		return self.get_queryset().get_user(user)

class Notification(models.Model):
	sender_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="notify_sender")
	sender_object_id = models.PositiveIntegerField()
	sender_content_object = GenericForeignKey('sender_content_type', 'sender_object_id')

	verb = models.CharField(max_length=255)

	action_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="notify_action", null=True, blank=True)
	action_object_id = models.PositiveIntegerField(null=True, blank=True)
	action_content_object = GenericForeignKey('action_content_type', 'action_object_id')

	target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="notify_target", null=True, blank=True)
	target_object_id = models.PositiveIntegerField(null=True, blank=True)
	target_content_object = GenericForeignKey('target_content_type', 'target_object_id')

	# sender = models.ForeignKey()
	recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications")
	# action = models.CharField(max_length=255)

	read = models.BooleanField(default=False)
	# unread = models.BooleanField(default=True)

	timestamp = models.DateTimeField(auto_now_add = True, auto_now=False)

	objects = NotificationManager()

	def __str__(self):
		# return str(self.verb)
		try:
			target_url = self.target_content_object.get_absolute_url()
		except:
			target_url = None

		a = self.sender_content_object
		b = self.verb
		c = self.action_content_object
		d = self.target_content_object
		e = target_url
		f = reverse("notifications_read", kwargs={"id": self.id})
		
		if self.target_content_object:
			if self.action_content_object and target_url:
				return "{a} {b} <a href='{f}?next={e}'>{d}</a> {c}".format(a=a, b=b, c=c, d=d, e=e, f=f)
			if self.action_content_object and not target_url:
				return "{a} {b} {c} {d}".format(a=a, b=b, c=c, d=d)
			return "{a} {b} {d}".format(a=a, b=b, d=d)
		return "{a} {b}".format(a=a, b=b)

	@property
	def get_links(self):
		try:
			target_url = self.target_content_object.get_absolute_url()
		except:
			target_url = reverse("notifications_all")

		sender = self.sender_content_object
		verb = self.verb
		action = self.action_content_object
		target = self.target_content_object
		target_url = target_url
		verify_read = reverse("notifications_read", kwargs={"id": self.id})
		
		if self.target_content_object:	
			return "<a href='{verify_read}?next={target_url}'>{sender} {verb} {target}</a>".format(sender=sender, verb=verb, action=action, target=target, target_url=target_url, verify_read=verify_read)
		else:
			return "<a href='{verify_read}?next={target_url}'>{sender}</a>".format(sender=sender, verb=verb, action=action, target=target, target_url=target_url, verify_read=verify_read)


def new_notification(sender, **kwargs):
	kwargs.pop("signal", None)
	recipient = kwargs.pop("recipient", None)
	verb = kwargs.pop("verb", None)
	# target = kwargs.pop("target", None)
	# action = kwargs.pop("action", None)

	new_note = Notification(
		recipient = recipient,
		verb = verb, 
		sender_content_type = ContentType.objects.get_for_model(sender),
		sender_object_id = sender.id,
		)

	for option in ("target", "action"):
		obj = kwargs.pop(option, None)
		if obj is not None:
			setattr(new_note, "{}_content_type".format(option), ContentType.objects.get_for_model(obj))
			setattr(new_note, "{}_object_id".format(option), obj.id)

	# if target is not None:
	# 	new_note.target_content_type = ContentType.objects.get_for_model(target)
	# 	new_note.target_object_id = target.id

	new_note.save()
	print(new_note)
	# if recipient is None:
	# 	recipient = 0
	# else:
	# 	new_notification_create = Notification.objects.create(recipient=recipient, action=action)


notify.connect(new_notification)