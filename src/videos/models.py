from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Video(models.Model):
	title =  models.CharField(max_length=120)
	embed_code = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		return reverse("video_detail", kwargs={"id": self.id})