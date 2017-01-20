from django.db import models

from accounts.models import MyUser
from videos.models import Video

# Create your models here.
class CommentManager(models.Manager):
	def add_comment(self, user=None, comment=None, path=None, video=None):
		if not path:
			raise ValueError("Must include path when adding comment")

		if not user:
			raise ValueError("Must include user when adding comment")

		comment = self.model(
			user = user,
			path = path,
			comment = comment,
		)

		if video is not None:
			comment.video = video
		comment.save(using=self._db)
		return comment

class Comment(models.Model):
	user = models.ForeignKey(MyUser)
	path = models.CharField(max_length=350)
	video = models.ForeignKey(Video, null=True, blank=True)
	text = models.TextField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	active = models.BooleanField(default=True)

	objects = CommentManager()

	def __str__(self):
		return self.user.username

	@property
	def get_comment(self):
		return self.text

