from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect

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
		
	except:
		raise Http404

	try:
		obj = Video.objects.get(slug=slug)
		comments = obj.comment_set.all()
		form = CommentForm(request.POST or None)

		context = {
			"obj": obj,
			"comments": comments,
			"form": form,
		}

		# if form.is_valid():
		# 	parent_id = request.POST.get('parent_id')
		# 	parent_comment = None
		# 	if parent_id is not None:
		# 		try:
		# 			parent_comment = Comment.objects.get(id=parent_id)
		# 		except:
		# 			parent_comment = None

		# 	comment_text = form.cleaned_data["comment"]
		# 	new_comment = Comment.objects.create_comment(
		# 		user = request.user,
		# 		path = request.get_full_path(),
		# 		text = comment_text,
		# 		video = obj,
		# 		parent = parent_comment,
		# 		)
		# 	return HttpResponseRedirect(obj.get_absolute_url())


			# obj_instance = form.save(commit=False)
			# obj_instance.path = request.get_full_path()
			# obj_instance.user = request.user
			# obj_instance.video = obj
			# obj_instance.save()

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