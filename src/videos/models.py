from urllib.parse import quote

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify

from django.conf import settings

# Create your models here.

class VideoQueryset(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def featured(self):
		return self.filter(featured=True)

	def has_embed(self):
		return self.filter(embed_code__isnull=False).exclude(embed_code__iexact="")

class VideoManager(models.Manager):
	def get_queryset(self):
		return VideoQueryset(self.model, using=self._db)

	def get_featured(self):
		# return super().filter(featured=True)
		return self.get_queryset().active().featured()

	def all(self):
		return self.get_queryset().active().has_embed()


DEFAULT_MESSAGE = """
Check me
"""

class Video(models.Model):
	title =  models.CharField(max_length=120)
	embed_code = models.CharField(max_length=500, null=True, blank=True)
	slug = models.SlugField(null=True, blank=True)
	share_message = models.TextField(default=DEFAULT_MESSAGE)
	active = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	free_preview = models.BooleanField(default=False)
	category = models.ForeignKey("Category", default=1)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

	objects = VideoManager()

	class Meta:
		unique_together = ('slug', 'category')

	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		try:
			return reverse("video_detail", kwargs={"slug": self.slug, "cat_slug": self.category.slug})
		except:
			return "/"

	def get_share_message(self):
		full_url = "{}{}".format(settings.FULL_DOMAIN_NAME, self.get_absolute_url())
		return quote("{}{}".format(self.share_message, full_url))

def video_signal_post_save_receiver(sender, instance, created, *args, **kwargs):

	print("nothing")
	print(args, kwargs, instance.title, instance.get_absolute_url(), created, sender)
	print(slugify(instance.title))
	# if created:
	# 	try:
	# 		instance.slug = slugify(instance.title)
	# 		instance.save()
	# 	except:
	# 		instance.slug = None

post_save.connect(video_signal_post_save_receiver, sender=Video)

class Category(models.Model):
	title = models.CharField(max_length=120)
	# videos = models.ManyToManyField(Video, null=True, blank=True)
	description = models.TextField(max_length=5000, null=True, blank=True)
	image = models.ImageField(upload_to="images/", null=True, blank=True)
	slug = models.SlugField(default="abc", unique=True)
	active = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		try:
			return reverse("project_detail", kwargs={"cat_slug": self.slug})
		except:
			return "/"

	def get_image_url(self):
		return "{}{}".format(settings.MEDIA_URL, self.image)

TAG_CHOICES = (
	("python", "python"),
	("django", "django"),
)
	
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class TaggedItem(models.Model):
	# category = models.ForeignKey(Category, null=True)
	# video = models.ForeignKey(Video)
	tag = models.SlugField(choices=TAG_CHOICES)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	def __str__(self):              # __unicode__ on Python 2
		return self.tag











