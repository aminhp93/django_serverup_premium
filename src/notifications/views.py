from django.core.urlresolvers import reverse
from django.shortcuts import render, Http404, HttpResponseRedirect

# Create your views here.
from .models import Notification

def all(request):
	# notifications = Notification.objects.all().get_user(request.user)
	notifications = Notification.objects.all_for_user(request.user)
	context = {
		"notifications": notifications
	}
	return render(request, "all.html", context)

def unread(request):
	pass

def read(request, id):
	print("fasd")
	next = request.GET.get('next', None)
	notification = Notification.objects.get(id=id)
	print(notification)
	if notification.recipient == request.user:
		notification.read = True
		notification.save()
		if next is not None:
			return HttpResponseRedirect(next)
		else:
			return HttpResponseRedirect(reverse("notifications_all"))
	else:
		raise Http404