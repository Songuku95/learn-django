"""configurations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, static
from member import settings

from member.views import user_api, event_api, comment_api, like_api, participant_api
urlpatterns = [
	url(r'^api/user/pre_signup/$', user_api.pre_signup),
	url(r'^api/user/signup/$', user_api.signup),
	url(r'^api/user/pre_login/$', user_api.pre_login),
	url(r'^api/user/login/$', user_api.login),
	url(r'^api/user/update_profile/$', user_api.update_profile),
	url(r'^api/user/get_profile/$', user_api.get_profile),
	url(r'^api/user/get_infos/$', user_api.get_infos),
	url(r'^api/upload_image/$', user_api.upload_image),

	url(r'^api/event/get_detail/', event_api.get_event_detail),
	url(r'^api/event/get_ids/', event_api.search_event),
	url(r'^api/event/get_infos/', event_api.get_event_infos),

	url(r'^api/event/comment/create/', comment_api.create),
	url(r'^api/event/comment/get_ids/', comment_api.get_comment_ids),
	url(r'^api/event/comment/get_details/', comment_api.get_comment_details),

	url(r'api/event/like/update/', like_api.update_like),
	url(r'api/event/like/get_ids/', like_api.get_event_likers),

	url(r'api/event/participant/update/', participant_api.update_participant),
	url(r'api/event/participant/get_ids/', participant_api.get_event_participants),
]


urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
