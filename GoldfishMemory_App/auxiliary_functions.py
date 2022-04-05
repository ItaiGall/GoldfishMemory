from django.core import serializers

def convert_queryset_to_json(qs, my_fields=None):
    return serializers.serialize("json", qs, fields=my_fields)