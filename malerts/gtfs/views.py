import json
from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.views.generic.base import TemplateView
from django.http import Http404

from gtfs.models import Alert, CAUSES, EFFECTS
# Create your views here.
from tastypie.api import Api
from gtfs.api import AlertResource
v1 = Api("v1")
v1.register(AlertResource())

def getutctimestamp():
	import calendar, time
	return calendar.timegm( time.gmtime() )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def alerts_json(request,template_name="gtfs/index.json"):
	epoch_now = getutctimestamp()
	local_now = datetime.fromtimestamp(int(epoch_now))
	allalerts = Alert.objects.filter(end__gte=local_now)

	return render_to_response(template_name,{
		"allalerts":			allalerts,
		"timestamp":			epoch_now,
		"CAUSES":				CAUSES, 
		"EFFECTS":				EFFECTS,
		},
		context_instance=RequestContext(request))


def alerts_ascii(request,template_name="gtfs/index.ascii"):
	epoch_now = getutctimestamp()
	local_now = datetime.fromtimestamp(int(epoch_now))
	allalerts = Alert.objects.filter(end__gte=local_now)

	return render_to_response(template_name,{
		"allalerts":			allalerts,
		"timestamp":			epoch_now,
		"CAUSES":				CAUSES,
		"EFFECTS":				EFFECTS,
		},
		context_instance=RequestContext(request),
		mimetype="text/plain; charset=utf-8")

"""
def alerts_pb(request):
	from gtfs.gtfs_realtime_pb2 import Alert as PBAlert
	utcnow = datetime.utcnow()
	timestamp = utcnow.strftime('%s')
	allalerts = Alert.objects.filter(end__gte=utcnow)
	alert = Alert.objects.get(id=1)
	# record = Record.objects.get(id = 4767)
	allalerts_pb = alert.toProtoBuf(PBAlert())
	# print allalerts_pb

	return render_to_response(template_name,{
		"allalerts":			allalerts,
		"timestamp":			timestamp,
		"CAUSES":				CAUSES,
		"EFFECTS":				EFFECTS,
		},
		context_instance=RequestContext(request),
		mimetype="text/plain; charset=utf-8")
"""

def alerts_html(request,template_name="gtfs/index.html"):
	epoch_now = getutctimestamp()
	local_now = datetime.fromtimestamp(int(epoch_now))
	allalerts = Alert.objects.filter(end__gte=local_now)

	return render_to_response(template_name,{
		"allalerts":			allalerts,
		"timestamp":			epoch_now,
		"CAUSES":				CAUSES, 
		"EFFECTS":				EFFECTS,
		},
		context_instance=RequestContext(request),
		mimetype="text/html; charset=utf-8")

class IndexView(TemplateView):
    template_name = 'gtfs/index.html'

class DetailView(TemplateView):
	template_name = 'gtfs/index.html'

	def get_detail(self, pk):
		tr = v1.canonical_resource_for('alert')

		try:
			alert = tr.cached_obj_get(pk=pk)
		except Alert.DoesNotExist:
			raise Http404

		bundle = tr.full_dehydrate(tr.build_bundle(obj=alert))
		data = bundle.data
		return data

	def get_context_data(self, **kwargs):
		base = super(DetailView, self).get_context_data(**kwargs)
		base['data'] = self.get_detail(base['params']['pk'])
		return base
