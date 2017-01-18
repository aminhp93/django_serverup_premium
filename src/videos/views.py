from django.shortcuts import render, Http404

from .models import Video

# Create your views here.
def video_list(request):
	queryset = Video.objects.all()

	context = {
		"queryset": queryset,

	}
	return render(request, "video_list.html", context)

def video_detail(request, id):
	try:
		obj = Video.objects.get(id=id)
		context = {
			"obj": obj,

		}
		return render(request, "video_detail.html", context)
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