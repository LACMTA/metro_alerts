from django.contrib.gis import admin
from django import forms

from gtfs.models import Alert, Agency, Zone, Stop, RouteType, Route, Service, Direction
from gtfs.models import Block, Shape, Trip, PickupType, DropOffType, StopTime, Calendar, ExceptionType
from gtfs.models import CalendarDate, Fare, PaymentMethod, FareAttribute, FareRule, Frequency, Transfer
									
#admin.site.register(Stop, admin.OSMGeoAdmin) 
#admin.site.register(Shape, admin.OSMGeoAdmin)

"""
class AlertAdmin(admin.TabularInline):
	fields = ('routes','stops',)
	def formfield_for_dbfield(self, db_field, **kwargs):
		formfield = super(AlertAdmin, self).formfield_for_dbfield(db_field, **kwargs)
		if db_field.name == 'stops':
			# dirty trick so queryset is evaluated and cached in .choices
			formfield.choices = formfield.choices
		return formfield
"""


class AlertForm(forms.ModelForm):
	model = Alert

class AlertAdmin(admin.ModelAdmin):
	"""
	class Alert(models.Model):
		# Collapsed TimeRange (we'll convert to utime in the view)
		start = models.DateTimeField()
		end = models.DateTimeField()
		# models.IntegerField(('causes'), choices=CAUSES, default=1)
		# cause = EnumField(choices=CAUSES)
		# effect = EnumField(choices=EFFECTS)
		cause = models.IntegerField(('causes'), choices=CAUSES, default=UNKNOWN_CAUSE)
		effect = models.IntegerField(('effects'), choices=EFFECTS, default=NO_SERVICE)
		url = models.URLField(default="http://www.metro.net/")
		header_text = models.CharField(max_length=80, default="")
		description_text = models.CharField(max_length=4000)
		# entities
		routes = models.ManyToManyField(Route, null=True, blank=True)
		trips = models.ManyToManyField(Trip, null=True, blank=True)
		stops = models.ManyToManyField(Stop, null=True, blank=True)
	"""
	fieldsets = (
		("Alert condition start and end", {'fields': (
					('start',),
					('end',), 
		)}),
		("Cause and effect for this alert", {'fields': (
					('cause',),
					('effect',), 
		)}),
		("Alert title, description, and explanatory page on Metro.net", {'fields': (
					'header_text', 
					'description_text', 
					'url', 
		)}),
		("Effected entities", {'fields': (
					'routes', 
					# 'trips', 
					'stops', 
		)}),
		)
	list_display = ('header_text','start','end', 'cause','effect',)
	search_fields = ('header_text','description_text',)
	filter_horizontal = ('routes','stops','trips',)
	form = AlertForm
	list_filter = ['cause','effect',]


admin.site.register(Alert,AlertAdmin)
admin.site.register(Agency)
admin.site.register(Zone)
admin.site.register(RouteType)				  
admin.site.register(Route)
admin.site.register(Service)
admin.site.register(Direction)
admin.site.register(Block)
admin.site.register(Trip)
admin.site.register(PickupType)
admin.site.register(DropOffType)
admin.site.register(StopTime)
admin.site.register(Calendar)
admin.site.register(ExceptionType)
admin.site.register(CalendarDate)
admin.site.register(Fare)
admin.site.register(PaymentMethod)
admin.site.register(FareAttribute)
admin.site.register(FareRule)
admin.site.register(Frequency)  
admin.site.register(Transfer)

