# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.utils import timezone

from notifications.signals import notify

class MyUserManager(BaseUserManager):
	def create_user(self, username=None, email=None, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""

		if not username:
			raise ValueError("Must include username")
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			username=username,
			email=self.normalize_email(email),
			# date_of_birth=date_of_birth,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(
			username=username,
			email=email,
			password=password,
			# date_of_birth=date_of_birth,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user


class MyUser(AbstractBaseUser):
	username = models.CharField(
		max_length=255,
		unique = True,
	)

	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)

	first_name = models.CharField(
		max_length=120,
		null=True,
		blank=True
	)

	last_name = models.CharField(
		max_length=120,
		null=True,
		blank=True
	)
	# date_of_birth = models.DateField()
	is_member = models.BooleanField(default=False, verbose_name="Is Paid Member")
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def get_full_name(self):
		# The user is identified by their email address
		# return self.email
		return "{} {}".format(self.first_name, self.last_name)

	def get_short_name(self):
		# The user is identified by their email address
		return self.first_name

	def __str__(self):              # __unicode__ on Python 2
		return self.username

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin


class Membership(models.Model):
	user = models.OneToOneField(MyUser)
	date_start = models.DateTimeField(default=timezone.now(), verbose_name="Start date")
	date_end = models.DateTimeField(default=timezone.now(), verbose_name="End date")

	def __str__(self):
		return str(self.user.username)

	def update_membership_status(self):
		if membership_ojb.date_end >= timezone.now():
			self.user.is_member = True
			self.user.save()
		elif membership_ojb.date_end < timezone.now():
			self.user.is_member = False
			self.user.save()
		else:
			pass

def user_logged_in_signal(sender, signal, request, user, **kwargs):
	print(sender, kwargs, "119")
	request.session.set_expiry(30000)
	membership_ojb, created = Membership.objects.get_or_create(user=user)
	if created:
		membership_ojb.date_start = timezone.now()
		membership_ojb.save()
		user.is_member = True
		user.save()
	membership_ojb.update_membership_status()
	
user_logged_in.connect(user_logged_in_signal)

class UserProfile(models.Model):
	user = models.OneToOneField(MyUser)
	bio = models.TextField(null=True, blank=True)
	facebook_link = models.CharField(
		max_length=320,
	 	null=True, 
	 	blank=True, 
	 	verbose_name="Facebook profile url"
	)

	def __str__(self):
		return self.user.username

def new_user_receiver(sender, instance, created, *args, **kwargs):
	if created:
		new_profile, is_created = UserProfile.objects.get_or_create(user=instance)
		notify.send(instance, 
					recipient=MyUser.objects.get(username="amin3"), 
					verb="New user created")

post_save.connect(new_user_receiver, sender=MyUser)
