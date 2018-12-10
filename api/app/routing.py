from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
	url(r'^lights/(?P<id>[0-9]+)/$', consumers.LightSocketConsumer),
	url(r'^lights/config/$', consumers.LightNameConsumer)
]
