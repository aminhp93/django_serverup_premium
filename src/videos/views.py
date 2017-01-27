from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect, get_object_or_404

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
	
	cat = get_object_or_404(Category, slug=cat_slug)
	obj = get_object_or_404(Video, slug=slug)
	if request.user.is_authenticated() or obj.has_preview:
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
	else:
		next_url = obj.get_absolute_url()
		return HttpResponseRedirect("{}?next={}".format(reverse("login"), next_url))


@login_required
def category_detail(request, cat_slug):
	obj = get_object_or_404(Category, slug=cat_slug)
	videos = obj.video_set.all()			
	context = {
		"obj": obj,
		"videos": videos,
	}
	return render(request, "category_detail.html", context)
