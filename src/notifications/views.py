import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, Http404, HttpResponseRedirect

# Create your views here.
from .models import Notification


@login_required
def all(request):
	# notifications = Notification.objects.all().get_user(request.user)
	notifications = Notification.objects.all_for_user(request.user)
	context = {
		"notifications": notifications
	}
	return render(request, "all.html", context)

@login_required
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

@login_required
def get_notifications_ajax(request):
	print("ajax")
	if request.is_ajax() and request.method=="POST":
		notifications = Notification.objects.all_for_user(request.user).recent()
		notes = []
		count = notifications.count()

		for note in notifications:
			notes.append(str(note.get_links))
		data = {
			# "item1": "item 1",
			# "item2": True,
			"notifications": notes
		}
		print(data)
		json_data = json.dumps(data)
		print(json_data)
		return HttpResponse(json_data, content_type="application/json")
	else:
		return Http404



