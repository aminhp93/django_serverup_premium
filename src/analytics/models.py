from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.conf import settings
from django.utils import timezone

from .signals import page_view

class PageView(models.Model):
	path = models.CharField(max_length=350)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	# count = models.PositiveIntegerField(default=1)
	timestamp = models.DateField(default=timezone.now())

	primary_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="notify_primary", null=True, blank=True)
	primary_object_id = models.PositiveIntegerField(null=True, blank=True)
	primary_content_object = GenericForeignKey('primary_content_type', 'primary_object_id')

	secondary_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="notify_secondary", null=True, blank=True)
	secondary_object_id = models.PositiveIntegerField(null=True, blank=True)
	secondary_content_object = GenericForeignKey('secondary_content_type', 'secondary_object_id')

	def __str__(self):
		return self.path

def page_view_received(sender, **kwargs):
	kwargs.pop("signal", None)
	page_path = kwargs.pop("page_path", None)
	notify_primary = kwargs.pop("notify_primary", None)
	notify_secondary = kwargs.pop("notify_secondary", None)

	user = sender
	
	if user.is_anonymous:
		new_page_view = PageView.objects.create(path=page_path, timestamp = timezone.now())
	else:
		new_page_view = PageView.objects.create(path=page_path, user=user, timestamp = timezone.now())

	if notify_primary:
		new_page_view.primary_object_id = notify_primary.id
		new_page_view.primary_content_type = ContentType.objects.get_for_model(notify_primary)
		new_page_view.save()

	if notify_secondary:
		new_page_view.secondary_object_id = notify_secondary.id
		new_page_view.secondary_content_type = ContentType.objects.get_for_model(notify_secondary)
		new_page_view.save()
		
	# if not created:
	# 	new_page_view.count += 1
	# 	new_page_view.save()

page_view.connect(page_view_received)