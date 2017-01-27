from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

from accounts.forms import RegisterForm
from accounts.models import MyUser
from analytics.models import PageView
from videos.models import Video
from comments.models import Comment

from .forms import LoginForm

from analytics.signals import page_view
# @login_required
# @login_required(login_url="/accounts/login/")
def home(request):
	# register_form = RegisterForm(request.POST or None)

	# if form.is_valid():
	# 	username = form.cleaned_data["username"]
	# 	email = form.cleaned_data["email"]
	# 	password = form.cleaned_data["password2"]

	# 	# MyUser.objects.create_user(username=username, email=email, password=password)
	# 	new_user = MyUser()
	# 	new_user.username = username
	# 	new_user.email = email
	# 	new_user.set_password(password)
	# 	new_user.save()
	# 	return redirect("login")
		# return HttpResponseRedirect(reverve('login'))


	# print(request.get_full_path() == "/")	
	# videos = Video.objects.all()
	# embeds = []

	# for video in videos:
	# 	safe_embed_code = format_html(mark_safe(video.embed_code))
	# 	embeds.append("{}".format(safe_embed_code))

	page_view.send(
		request.user,
		page_path = request.get_full_path(),
		
		)
	if request.user.is_authenticated():
		page_view_objs = request.user.pageview_set.get_videos()[:2]
		recent_videos = []
		for obj in page_view_objs:
			if not obj.primary_content_object in recent_videos:
				recent_videos.append(obj.primary_content_object)

		recent_comments = Comment.objects.recent()

		# top items
		video_type = ContentType.objects.get_for_model(Video)
		popular_videos_list = PageView.objects.filter(primary_content_type=video_type)\
		.values("primary_object_id")\
		.annotate(the_count=Count("primary_object_id"))\
		.order_by("-the_count")[:2]

		popular_videos = []
		for item in popular_videos_list:
			try:
				new_video = Video.objects.get(id=item["primary_object_id"])
				popular_videos.append(new_video)
			except:
				pass
		

		# one item
		# PageView.objects.filter(primary_content_type=video_type, primary_object_id=2).count()

		template = "home_logged_in.html"

		context = {
			"recent_videos": recent_videos,
			"recent_comments": recent_comments,
			"popular_videos": popular_videos,
		}
	else:
		login_form = LoginForm()
		register_form = RegisterForm()
		template = "home_visitor.html"
		context = {
			"login_form": login_form,
			"register_form": register_form,
			"action_value": "/",
			"submit_btn_value": "Register"
			# "videos": videos,
			# "number": videos.count(),
			# "embeds": embeds,
		}
	return render(request, template, context)
	
@login_required(login_url="/staff/login/")
def staff_home(request):
	context = {

	}
	return render(request, "home.html", context)



# def home(request):	
# 	if request.user.is_authenticated:
# 		videos = Video.objects.all()
# 		embeds = []

# 		for video in videos:
# 			safe_embed_code = format_html(mark_safe(video.embed_code))
# 			embeds.append("{}".format(safe_embed_code))

# 		context = {
# 			"videos": videos,
# 			"number": videos.count(),
# 			"embeds": embeds,
# 		}
# 		return render(request, "home.html", context)
# 	else:
# 		return HttpResponseRedirect('/login')

