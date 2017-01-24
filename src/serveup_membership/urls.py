"""serveup_membership URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from serveup_membership.views import home, staff_home
from accounts.views import auth_login, auth_logout
from videos.views import video_detail, category_list, category_detail
from comments.views import comment_thread, comment_create
from notifications.views import all, read, get_notifications_ajax

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    # url(r'', TemplateView.as_view(template_name='base.html'), name='home')
    url(r'^staff/$', staff_home, name='staff'),
    url(r'^projects/$', category_list, name='projects'),
    # url(r'^projects/(?P<id>\d+)/$', video_detail, name="video_detail"),
    url(r'^projects/(?P<cat_slug>[\w-]+)/$', category_detail, name="project_detail"),
    url(r'^projects/(?P<cat_slug>[\w-]+)/(?P<slug>[\w-]+)/$', video_detail, name="video_detail"),
]
# auth login/logout
urlpatterns += [
    url(r'^login/$', auth_login, name='login'),
    url(r'^logout/$', auth_logout, name='logout'),
]
# Comment Thread
urlpatterns += [
    url(r'^comment/(?P<id>\d+)$', comment_thread, name="comment_thread"),
    url(r'^comment/create$', comment_create, name="comment_create"),
]
# Notifications
urlpatterns += [
    url(r'^notifications/$', all, name="notifications_all"),
    url(r'^notifications/ajax/$', get_notifications_ajax, name="notifications_ajax"),
    url(r'^notifications/read/(?P<id>\d+)/$', read, name="notifications_read"),
    
]
    
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



