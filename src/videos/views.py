from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404

from .models import Video, Category
from comments.models import Comment
from comments.forms import CommentForm
# Create your views here.
def category_list(request):
	objs = Category.objects.all()

	context = {
		"objs": objs,

	}
	return render(request, "category_list.html", context)

@login_required
def video_detail(request, cat_slug, slug):
	# path = request.get_full_path()
	# comments = Comment.objects.filter(path=path)
	try:
		cat = Category.objects.get(slug=cat_slug)
		print("test")
	except:
		raise Http404

	try:
		obj = Video.objects.get(slug=slug)
		print(obj)
		comments = obj.comment_set.all()
		print(comments)
		form = CommentForm(request.POST or None)

		context = {
			"obj": obj,
			"comments": comments,
			"form": form,
		}

		if form.is_valid():
			obj_instance = form.save(commit=False)
			print(obj_instance, "fasd")
			obj_instance.path = request.get_full_path()
			obj_instance.user = request.user
			obj_instance.video = obj
			obj_instance.save()
			print("d")

		return render(request, "video_detail.html", context)
	except:
		raise Http404

@login_required
def category_detail(request, cat_slug):
	try:
		obj = Category.objects.get(slug=cat_slug)
		videos = obj.video_set.all()
		form = CommentForm(request.POST or None)
			
		context = {
			"obj": obj,
			"videos": videos,
		}
		return render(request, "category_detail.html", context)
	except:
		raise Http404

# def video_edit(request):
# 	context = {
	
# 	}
# 	return render(request, "video_edit.html", context)

# def video_delete(request):
# 	context = {
	
# 	}
# 	return render(request, "video_delete.html", context)