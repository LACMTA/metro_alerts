# -*- coding: utf-8 -*-
import datetime
from django.contrib.gis.db import models 
# TASTYPIE
# CKEDITOR
from ckeditor.fields import RichTextField

from pbinterface import PBtransfer

class Agency(models.Model):
	name = models.TextField()
	url = models.URLField()
	timezone = models.CharField(max_length=255)
	agency_id = models.CharField(max_length=255, null=True, blank=True)
	lang = models.CharField(max_length=2, null=True, blank=True)
	phone = models.CharField(max_length=255, null=True, blank=True)
	fare_url = models.URLField(null=True, blank=True)
	slug = models.SlugField(editable=True,unique=True, help_text='The Slug is a URL-friendly title for an object.')

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('gtfs.views.agency', [self.slug])


class Zone(models.Model):
	""" Define the fare zone""" 
	zone_id = models.CharField(max_length=255, unique=True)

	def __unicode__(self):
		return self.zone_id

class Stop(models.Model):
	"""
	ALTER TABLE gtfs_stop ADD SPATIAL INDEX(geopoint);
	"""
	stop_id = models.CharField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	url = models.URLField()	
	desc = models.TextField(null=True, blank=True)
	geopoint = models.PointField(null=False, blank=False, default=(0,0) )
	code = models.CharField(max_length=255, null=True, blank=True)
	zone = models.ForeignKey(Zone, null=True, blank=True)
	location_type = models.IntegerField(null=True, blank=True) #TODO add choices for 0=blank=Stop and 1=Station
	parent_station = models.ForeignKey('self', null=True, blank=True)  
	objects = models.GeoManager()
											
	def __unicode__(self):
		return self.name

class RouteType(models.Model):
	"""Referential data"""  
	name = models.CharField(max_length=50)
	description = models.TextField()
	value = models.IntegerField(unique=True)
	
	def __unicode__(self):
		return self.name

class Route(models.Model):
	route_id = models.CharField(max_length=255, unique=True)
	agency = models.ForeignKey(Agency, null=True, blank=True)
	short_name = models.CharField(max_length=255, null=True, blank=True)
	long_name = models.CharField(max_length=255, null=True, blank=True)
	desc = models.TextField(null=True, blank=True)
	route_type = models.ForeignKey(RouteType)
	url = models.URLField(null=True, blank=True)
	color = models.CharField(max_length=6, default="FFFFFF")
	text_color = models.CharField(max_length=6, default="000000")
	
	def __unicode__(self):
		return "%s %s" %(self.short_name,self.long_name )

class Service(models.Model):
	service_id = models.CharField(max_length=255, unique=True)

	def __unicode__(self):
		return self.service_id
						  
class Direction(models.Model):
	"""Referential data"""
	name = models.CharField(max_length=20)
	value = models.IntegerField(unique=True)
	
	def __unicode__(self):
		return self.name
								  
class Block(models.Model):
	block_id = models.CharField(max_length=255, unique=True)
	
	def __unicode__(self):
		return self.block_id
														  
class Shape(models.Model):
	shape_id = models.CharField(max_length=255)
	geopoint = models.PointField()
	pt_sequence = models.IntegerField()
	dist_traveled = models.FloatField(null=True, blank=True) 
	objects = models.GeoManager()
	
	def __unicode__(self):
		return self.shape_id
	
class Trip(models.Model):
	route = models.ForeignKey(Route)
	service = models.ForeignKey(Service)
	trip_id = models.CharField(max_length=255, unique=True)
	headsign = models.TextField(null=True, blank=True)
	direction = models.ForeignKey(Direction, null=True, blank=True)
	block = models.ForeignKey(Block, null=True, blank=True)
	shape_id = models.CharField(max_length=255, null=True, blank=True)
	
	def __unicode__(self):
		return self.trip_id

class PickupType(models.Model):
	"""Referential data"""
	name = models.CharField(max_length=255)
	value = models.IntegerField()
	
	def __unicode__(self):
		return self.name

class DropOffType(models.Model):
	"""Referential data"""
	name = models.CharField(max_length=255)
	value = models.IntegerField()
	
	def __unicode__(self):
		return self.name

class StopTime(models.Model):
	trip = models.ForeignKey(Trip)
	arrival_time = models.TimeField()
	departure_time = models.TimeField()
	stop = models.ForeignKey(Stop)
	stop_sequence = models.IntegerField()
	headsign = models.TextField(null=True, blank=True)
	pickup_type = models.ForeignKey(PickupType, null=True, blank=True)
	drop_off_type = models.ForeignKey(DropOffType, null=True, blank=True)
	shape_dist_traveled = models.FloatField(null=True, blank=True)
	
	def __unicode__(self):
		return self.arrival_time

class Calendar(models.Model):
	service = models.ForeignKey(Service)
	monday = models.IntegerField()
	tuesday = models.IntegerField()
	wednesday = models.IntegerField()
	thursday = models.IntegerField()
	friday = models.IntegerField()
	saturday = models.IntegerField()
	sunday = models.IntegerField()
	start_date = models.DateField()
	end_date = models.DateField()				  
	
	def __unicode__(self):
		return self.start_date

class ExceptionType(models.Model):
	"""Referential data"""
	name = models.CharField(max_length=255)
	value = models.IntegerField()
	
	def __unicode__(self):
		return self.name

class CalendarDate(models.Model):
	service = models.ForeignKey(Service)
	date = models.DateField()
	exception_type = models.ForeignKey(ExceptionType)
	
	def __unicode__(self):
		return self.date

class Fare(models.Model):
	fare_id = models.CharField(max_length=255, unique=True)
													
	def __unicode__(self):
		return self.fare_id

class PaymentMethod(models.Model):
	name = models.CharField(max_length=50)
	value = models.IntegerField()
	
	def __unicode__(self):
		return self.name
	
class FareAttribute(models.Model):
	fare = models.ForeignKey(Fare)
	price = models.FloatField()
	currency = models.CharField(max_length=3)
	payment_method = models.ForeignKey(PaymentMethod)
	transfers = models.IntegerField(null=True, blank=True)
	transfer_duration = models.IntegerField(null=True, blank=True) # duration in seconds
	
	def __unicode__(self):
		return self.price

class FareRule(models.Model):
	fare = models.ForeignKey(Fare)
	route = models.ForeignKey(Route, null=True, blank=True)
	origin = models.ForeignKey(Zone, null=True, blank=True, related_name="origin")
	destination = models.ForeignKey(Zone, null=True, blank=True, related_name="destination")
	contains = models.ForeignKey(Zone, null=True, blank=True, related_name="contains")
	
	def __unicode__(self):
		return "%s-%s" %(self.origin,self.destination)

class Frequency(models.Model):
	trip = models.ForeignKey(Trip)
	start_time = models.TimeField()
	end_time = models.TimeField()
	headway_secs = models.IntegerField()
	exact_times = models.IntegerField(null=True, blank=True)
	
	def __unicode__(self):
		return "%s-%s" %(self.start_time,self.end_time)

class Transfer(models.Model):
	from_stop = models.ForeignKey(Stop, related_name="from_stop")
	to_stop = models.ForeignKey(Stop, related_name="to_stop")
	transfer_type = models.IntegerField()
	min_transfer_time = models.IntegerField(null=True, blank=True)
	
	def __unicode__(self):
		return "%s-%s" %(self.from_stop,self.to_stop)

UNKNOWN_CAUSE=0
OTHER_CAUSE=1
TECHNICAL_PROBLEM=2
STRIKE=3
ACCIDENT=4
HOLIDAY=5
MAINTENANCE=6
CONSTRUCTION=7
POLICE_ACTIVITY=8
MEDICAL_EMERGENCY=9
DEMONSTRATION=10
WEATHER=11

CAUSES=(
	(UNKNOWN_CAUSE,'UNKNOWN_CAUSE'),
	(OTHER_CAUSE,'OTHER_CAUSE'),
	(TECHNICAL_PROBLEM,'TECHNICAL_PROBLEM'),
	(STRIKE,'STRIKE'),
	(ACCIDENT,'ACCIDENT'),
	(HOLIDAY,'HOLIDAY'),
	(MAINTENANCE,'MAINTENANCE'),
	(CONSTRUCTION,'CONSTRUCTION'),
	(POLICE_ACTIVITY,'POLICE_ACTIVITY'),
	(MEDICAL_EMERGENCY,'MEDICAL_EMERGENCY'),
	(DEMONSTRATION,'DEMONSTRATION'),
	(WEATHER,'WEATHER'),
)

NO_SERVICE=0
REDUCED_SERVICE=1
SIGNIFICANT_DELAYS=2
DETOUR=3
ADDITIONAL_SERVICE=4
MODIFIED_SERVICE=5
OTHER_EFFECT=6
UNKNOWN_EFFECT=7
STOP_MOVED=8

EFFECTS=(
	(NO_SERVICE,'NO_SERVICE'),
	(REDUCED_SERVICE,'REDUCED_SERVICE'),
	(SIGNIFICANT_DELAYS,'SIGNIFICANT_DELAYS'),
	(DETOUR,'DETOUR'),
	(ADDITIONAL_SERVICE,'ADDITIONAL_SERVICE'),
	(MODIFIED_SERVICE,'MODIFIED_SERVICE'),
	(OTHER_EFFECT,'OTHER_EFFECT'),
	(UNKNOWN_EFFECT,'UNKNOWN_EFFECT'),
	(STOP_MOVED,'STOP_MOVED'),
)

"""
['ACCIDENT',
 'ACTIVE_PERIOD_FIELD_NUMBER',
 'ADDITIONAL_SERVICE',
 'ByteSize',
 'CAUSE_FIELD_NUMBER',
 'CONSTRUCTION',
 'Clear',
 'ClearExtension',
 'ClearField',
 'CopyFrom',
 'DEMONSTRATION',
 'DESCRIPTION_TEXT_FIELD_NUMBER',
 'DESCRIPTOR',
 'DETOUR',
 'EFFECT_FIELD_NUMBER',
 'Extensions',
 'FindInitializationErrors',
 'FromString',
 'HEADER_TEXT_FIELD_NUMBER',
 'HOLIDAY',
 'HasExtension',
 'HasField',
 'INFORMED_ENTITY_FIELD_NUMBER',
 'IsInitialized',
 'ListFields',
 'MAINTENANCE',
 'MEDICAL_EMERGENCY',
 'MODIFIED_SERVICE',
 'MergeFrom',
 'MergeFromString',
 'NO_SERVICE',
 'OTHER_CAUSE',
 'OTHER_EFFECT',
 'POLICE_ACTIVITY',
 'ParseFromString',
 'REDUCED_SERVICE',
 'RegisterExtension',
 'SIGNIFICANT_DELAYS',
 'STOP_MOVED',
 'STRIKE',
 'SerializePartialToString',
 'SerializeToString',
 'SetInParent',
 'TECHNICAL_PROBLEM',
 'UNKNOWN_CAUSE',
 'UNKNOWN_EFFECT',
 'URL_FIELD_NUMBER',
 'WEATHER',
 'active_period',
 'cause',
 'description_text',
 'effect',
 'header_text',
 'informed_entity',
 'url']
"""
class Alert(models.Model):
	pb_rows = {'start': 'active_period.start', 'end': 'active_period.end', 'cause': 'cause', 'effect': 'effect'}
	# Collapsed TimeRange (we'll convert to utime in the view)
	start = models.DateTimeField(default=datetime.datetime.now)
	end = models.DateTimeField(default=datetime.datetime.now)
	# models.IntegerField(('causes'), choices=CAUSES, default=1)
	# cause = EnumField(choices=CAUSES)
	# effect = EnumField(choices=EFFECTS)
	cause = models.IntegerField(('causes'), choices=CAUSES, default=UNKNOWN_CAUSE)
	effect = models.IntegerField(('effects'), choices=EFFECTS, default=NO_SERVICE)
	url = models.URLField(default="http://www.metro.net/alerts")
	header_text = models.CharField(max_length=80, default="")
	# description_text = models.TextField(max_length=1000, null=True, blank=True)
	description_text = models.CharField(blank=True, verbose_name='Text description', max_length=1000, )
	# entities
	routes = models.ManyToManyField(Route, null=True, blank=True)
	trips = models.ManyToManyField(Trip, null=True, blank=True)
	stops = models.ManyToManyField(Stop, null=True, blank=True)
	
	def __unicode__(self):
		return self.header_text

	def causeText(self):
		return CAUSES[self.cause][1]

	def effectText(self):
		return EFFECTS[self.effect][1]

	def active_period(self):
		time_range = {
			'start': self.start.strftime('%s'),
			'end':	self.end.strftime('%s')
			}
		return (time_range)

	def fromProtoBuf(self, pb2, attrs = None):
		if not attrs:
			attrs = self.pb_rows
		for attr in attrs:
			setattr(self, attr, getattr(pb2, attrs[attr]))

	def toProtoBuf(self, pb2, attrs = None):
		if not attrs:
			attrs = self.pb_rows
		for attr in attrs.keys():
			setattr(pb2, attrs[attr], getattr(self, attr))
		return pb2

"""
class EntitySelector(models.Model):
	agency_id = Column(String(15))
	route_id = Column(String(10))
	route_type = Column(Integer)
	stop_id = Column(String(10))

	# Collapsed TripDescriptor
	trip_id = Column(String(10))
	trip_route_id = Column(String(10))
	trip_start_time = Column(String(8))
	trip_start_date = Column(String(10))

	alert_id = Column(Integer, ForeignKey('alerts.oid'))
"""
