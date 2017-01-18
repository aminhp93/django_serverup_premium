from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from videos.models import Video

from .forms import LoginForm

@login_required
# @login_required(login_url="/accounts/login/")
def home(request):
	print(request.get_full_path() == "/")	
	videos = Video.objects.all()
	embeds = []

	for video in videos:
		safe_embed_code = format_html(mark_safe(video.embed_code))
		embeds.append("{}".format(safe_embed_code))

	context = {
		"videos": videos,
		"number": videos.count(),
		"embeds": embeds,
	}
	return render(request, "home.html", context)
	
@login_required(login_url="/staff/login/")
def staff_home(request):
	context = {

	}
	return render(request, "home.html", context)


def auth_login(request):
	form = LoginForm(request.POST or None)
	next_url = request.GET.get('next')
	print(next_url)
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		print(username, password)
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(next_url)

	context = {
		'form': form
	}
	return render(request, "login.html", context)

def auth_logout(request):
	logout(request)
	return HttpResponseRedirect("/")

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

