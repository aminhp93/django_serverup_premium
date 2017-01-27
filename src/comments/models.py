from django.db import models
from django.core.urlresolvers import reverse

from accounts.models import MyUser
from videos.models import Video

# Create your models here.
class CommentManager(models.Manager):
	def all(self):
		return super().filter(active=True).filter(parent=None)

	def recent(self):
		return super().filter(active=True).filter(parent=None)[:3]

	def create_comment(self, user=None, text=None, path=None, video=None, parent=None):
		if not path:
			raise ValueError("Must include path when adding comment")

		if not user:
			raise ValueError("Must include user when adding comment")

		comment = self.model(
			user = user,
			path = path,
			text = text,
		)

		if video is not None:
			comment.video = video
		if parent is not None:
			comment.parent = parent
		comment.save(using=self._db)
		return comment

class Comment(models.Model):
	user = models.ForeignKey(MyUser)
	parent = models.ForeignKey("self", null=True, blank=True)
	path = models.CharField(max_length=350)
	video = models.ForeignKey(Video, null=True, blank=True)
	text = models.TextField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	active = models.BooleanField(default=True)

	objects = CommentManager()

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return self.text

	def get_absolute_url(self):
		return reverse("comment_thread", kwargs={"id": self.id})

	@property
	def get_origin(self):
		return self.path

	@property
	def get_preview(self):
		return self.text[:20]

	@property
	def get_comment(self):
		return self.text

	def is_child(self):
		if self.parent is not None:
			return True
		else:
			return False

	def get_children(self):
		if self.is_child == True:
			return None
		else:
			child_comments = Comment.objects.filter(parent=self)
			return child_comments

	def get_affected_user(self):
		comment_children = self.get_children()
		if comment_children is not None:
			users = []
			for comment in comment_children:
				if comment.user in users:
					pass
				else:
					users.append(comment.user)
			return users
		return None


	
	

