from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404

from .models import Video, Category

# Create your views here.
def category_list(request):
	objs = Category.objects.all()

	context = {
		"objs": objs,

	}
	return render(request, "category_list.html", context)

@login_required
def video_detail(request, cat_slug, slug):
	try:
		cat = Category.objects.get(slug=cat_slug)
	except:
		Http404

	try:
		obj = Video.objects.get(slug=slug)
		print(obj.get_share_message())
		context = {
			"obj": obj,

		}
		return render(request, "video_detail.html", context)
	except:
		raise Http404

@login_required
def category_detail(request, cat_slug):
	try:
		obj = Category.objects.get(slug=cat_slug)
		videos = obj.video_set.all()
		context = {
			"obj": obj,
			"videos": videos,
		}
		return render(request, "category_detail.html", context)
	except:
		raise Http404

def video_edit(request):
	context = {
	
	}
	return render(request, "video_edit.html", context)

def video_delete(request):
	context = {
	
	}
	return render(request, "video_delete.html", context)