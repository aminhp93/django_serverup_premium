from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from accounts.forms import RegisterForm
from accounts.models import MyUser
from videos.models import Video

from .forms import LoginForm


# @login_required
# @login_required(login_url="/accounts/login/")
def home(request):
	form = RegisterForm(request.POST or None)

	if form.is_valid():
		username = form.cleaned_data["username"]
		email = form.cleaned_data["email"]
		password = form.cleaned_data["password2"]

		# MyUser.objects.create_user(username=username, email=email, password=password)
		new_user = MyUser()
		new_user.username = username
		new_user.email = email
		new_user.set_password(password)
		new_user.save()
		return redirect("login")
		# return HttpResponseRedirect(reverve('login'))


	# print(request.get_full_path() == "/")	
	# videos = Video.objects.all()
	# embeds = []

	# for video in videos:
	# 	safe_embed_code = format_html(mark_safe(video.embed_code))
	# 	embeds.append("{}".format(safe_embed_code))

	context = {
		"form": form,
		"action_value": "/",
		"submit_btn_value": "Register"
		# "videos": videos,
		# "number": videos.count(),
		# "embeds": embeds,
	}
	return render(request, "form.html", context)
	
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

