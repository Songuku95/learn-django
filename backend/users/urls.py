from django.conf.urls import url

from users.api import signup, login

urlpatterns = [
	url(r'^signup/$', signup),
	url(r'^login/$', login),
]
