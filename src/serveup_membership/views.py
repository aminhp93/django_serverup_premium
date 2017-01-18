from django.shortcuts import render
from videos.models import Video


def home(request):
	videos = Video.objects.all()
	embeds = []

	for video in videos:
		embeds.append("{}".format(video.embed_code))

	context = {
		"videos": videos,
		"number": videos.count(),
		"embeds": embeds,
	}
	return render(request, "home.html", context)

