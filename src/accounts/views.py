from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .models import MyUser
from .forms import LoginForm, RegisterForm
# Create your views here.

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
			if next_url is not None:
				return HttpResponseRedirect(next_url)
			return HttpResponseRedirect("/")

	context = {
		'form': form
	}
	return render(request, "login.html", context)

def auth_logout(request):
	logout(request)
	return HttpResponseRedirect("/")

def auth_register(request):
	
	form = RegisterForm(request.POST or None)

	if form.is_valid():
		username = form.cleaned_data["username"]
		email = form.cleaned_data["email"]
		password = form.cleaned_data["password2"]

		new_user = MyUser()
		new_user.username = username
		new_user.email = email
		new_user.set_password(password)
		new_user.save()
		return redirect("login")

	context = {
		"form": form,
		"action_value": "",
		"submit_btn_value": "Register",

	}
	return render(request, "register_form.html", context)


