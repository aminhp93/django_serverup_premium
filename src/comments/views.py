from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect

from notifications.signals import notify

from videos.models import Video

from .models import Comment
from .forms import CommentForm

# Create your views here.
@login_required
def comment_thread(request, id):
	comment = Comment.objects.get(id=id)
	form = CommentForm()

	context = {
		"comment": comment,
		"form": form,
	}
	return render(request, "comment_thread.html", context)

def comment_create(request):
	if request.method == "POST" and request.user.is_authenticated:
		parent_id = request.POST.get('parent_id')
		video_id = request.POST.get('video_id')
		origin_path = request.POST.get('origin_path')

		try:
			video = Video.objects.get(id=video_id)
		except:
			video = None

		parent_comment = None
		if parent_id is not None:
			try:
				parent_comment = Comment.objects.get(id=parent_id)
			except:
				parent_comment = None

			if parent_comment.video is not None:
				video = parent_comment.video

		form = CommentForm(request.POST)

		if form.is_valid():
			comment_text = form.cleaned_data["comment"]

			if parent_comment is not None:
				new_comment = Comment.objects.create_comment(
					user = request.user,
					path = parent_comment.get_origin,
					text = comment_text,
					video = video,
					parent = parent_comment,
					)
				notify.send(request.user, recipient=parent_comment.user, action="responed to user")
				messages.success(request, "Thank", extra_tags='alert-warning')
				return HttpResponseRedirect(parent_comment.get_absolute_url())
			else:
				new_comment = Comment.objects.create_comment(
					user = request.user,
					path = origin_path,
					text = comment_text,
					video = video,
					)
				notify.send(request.user, recipient=request.user, action="new comment added")
				messages.success(request, "Thank")
				return HttpResponseRedirect(new_comment.get_absolute_url())
		else:
			messages.error(request, "There was an error")
			return HttpResponseRedirect(origin_path)

	else:
		raise Http404