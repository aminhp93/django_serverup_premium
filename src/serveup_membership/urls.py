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

from serveup_membership.views import home, staff_home
from accounts.views import auth_login, auth_logout
from videos.views import video_detail, category_list, category_detail
from comments.views import comment_thread, comment_create

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    # url(r'', TemplateView.as_view(template_name='base.html'), name='home')
    url(r'^staff/$', staff_home, name='staff'),
    url(r'^login/$', auth_login, name='login'),
    url(r'^logout/$', auth_logout, name='logout'),
    url(r'^projects/$', category_list, name='projects'),
    # url(r'^projects/(?P<id>\d+)/$', video_detail, name="video_detail"),
    url(r'^projects/(?P<cat_slug>[\w-]+)/$', category_detail, name="project_detail"),
    url(r'^projects/(?P<cat_slug>[\w-]+)/(?P<slug>[\w-]+)/$', video_detail, name="video_detail"),
    url(r'^comment/(?P<id>\d+)$', comment_thread, name="comment_thread"),
    url(r'^comment/create$', comment_create, name="comment_create"),


]

    