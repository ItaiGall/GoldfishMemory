from django.core import serializers
import datetime
import pytz

def convert_queryset_to_json(qs, my_fields=None):
    return serializers.serialize("json", qs, fields=my_fields)

def getUTCTimestamp(time_string):
    return datetime.datetime.strptime(time_string, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=pytz.UTC)

def getLocalTimestamp(utc_datetime):
    float_datetime = utc_datetime.timestamp()
    return datetime.datetime.fromtimestamp(float_datetime)

def getCurrentTimezone():
    return datetime.datetime.now().astimezone().tzinfo
