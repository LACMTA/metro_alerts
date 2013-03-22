from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.cache import SimpleCache,NoCache

from django.conf import settings
from gtfs.models import Alert

class BackboneCompatibleResource(ModelResource):
	class Meta:
		always_return_data = True

	def alter_list_data_to_serialize(self, request, data):
		return data["objects"]

class AlertResource(BackboneCompatibleResource):
	class Meta:
		queryset = Alert.objects.all()
		serializer = Serializer(formats=['json', 'jsonp'])
		if settings.DEBUG:
			cache = NoCache()
		else:
			cache = SimpleCache()
