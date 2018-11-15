from django.conf.urls import url

from events import event_api, like_api, participant_api, comment_api

urlpatterns = [
	url(r'^create/$', event_api.create_event),
	url(r'^update/$', event_api.update_event),
	url(r'^get_detail/$', event_api.get_event_detail),
	url(r'^image/update/', event_api.update_image_status),
	url(r'^get_ids/$', event_api.search_event),
	url(r'^get_list/', event_api.get_event_list),

	url(r'^like/$', like_api.update_like),
	url(r'^get_likers/$', like_api.get_event_likers),

	url(r'^participate/$', participant_api.update_participant),
	url(r'^get_participants/$', participant_api.get_event_participants),

	url(r'^comment/create/$', comment_api.create),
	url(r'^comment/get_ids/$', comment_api.get_comment_ids),
	url(r'^comment/get_details/$', comment_api.get_comment_details),
	url(r'^comment/delete/$', comment_api.delete),
]
