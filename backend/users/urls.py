from django.conf.urls import url

from users.api import signup

urlpatterns = [
	url(r'^signup/$', signup),
]
