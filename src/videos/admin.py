from django.contrib import admin
from .models import Video, Category, TaggedItem
# Register your models here.

class VideoAdmin(admin.ModelAdmin):
	list_display = ["__str__", "slug"]
	# fields = ["title"]
	prepopulated_fields = {'slug': ('title',)}
	class Meta:
		model = Video

admin.site.register(Video, VideoAdmin)
admin.site.register(Category)
admin.site.register(TaggedItem)