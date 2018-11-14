from django.conf.urls import url

from users.api import signup, login, update_profile, get_profile

urlpatterns = [
	url(r'^signup/$', signup),
	url(r'^login/$', login),
	url(r'^update_profile/$', update_profile),
	url(r'^get_profile$', get_profile),
]
