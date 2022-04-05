from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from .forms import SaveParkingSpotForm
from .models import ParkingSpot
from django.views.generic import ListView, DetailView
from django.conf import settings
from .auxiliary_functions import convert_queryset_to_json
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .random_characters import RndStr
import json
from django.http import JsonResponse
import django.contrib.messages as messages
import datetime
import pytz

def index(request):
    if request.session.has_key("open_session"):
        session_data = convert_queryset_to_json(ParkingSpot.objects.filter(pk = int(request.session.get("open_session"))), ('my_latitude', 'my_longitude', 'my_address'))
        return render(request, 'homepage.html', context={ 'user': request.user.username, "open_session":session_data,
                                                          'maps_api_key':settings.GOOGLE_MAPS_API_KEY})
    else:
        return render(request, 'homepage.html', context={ 'user': request.user.username, 'maps_api_key':settings.GOOGLE_MAPS_API_KEY })

@login_required(login_url='/accounts/login/')
@csrf_protect
def create_parking_spot(request):
    current_user = request.user
    if request.method == 'POST':
        data = json.loads(request.POST["myJSON"])
        ps = SaveParkingSpotForm()
        #save as commit=False to populate the form with json data before saving in DB
        finalform = ps.save(commit=False)
        finalform.user = current_user
        finalform.slug= RndStr() + str(int(datetime.datetime.now().timestamp()))
        finalform.start_parking = getUTCTimestamp(data.get("timestamp"))
        finalform.my_timezone = settings.TIME_ZONE  = data.get('timezone', 'UTC')
        finalform.my_latitude = float(data.get('latitude', 0))
        finalform.my_longitude = float(data.get('longitude', 0))
        finalform.my_geolocation = str(finalform.my_latitude)+","+str(finalform.my_longitude)
        finalform.my_address = data.get('MyAddress')
        finalform.save()
        #Clear session storage before saving entry id in session data for use after app reload
        try:
            del request.session["open_session"]
        except:
            pass
        finally:
            request.session["open_session"] = str(ParkingSpot.objects.filter(user = current_user).last().pk)

        #return the object id to client for further update of stop_parking and duration
        ps = ParkingSpot.objects.latest('start_parking')
        myId = ps.pk
        messages.success(request, "Time and location of your parking spot have been recorded successfully")
        return JsonResponse({'status': 'Parking spot added!', 'id': str(myId) })
    else:
        messages.error(request, "An error occurred")
        return JsonResponse({'status': 'Unsuccessful' })
    return HttpResponseBadRequest('Invalid request')

#Enter stop parking time and compute parking duration to turn record into closed and archived event
@login_required(login_url='/accounts/login/')
@csrf_protect
def finalize_parking_spot(request):
    if request.method == 'POST':
        data = json.loads(request.POST["myJSON2"])
        record_id = int(data.get("record_to_be_closed"))
        if record_id != 0:
            my_record = ParkingSpot.objects.get(pk=record_id)
            stoptime = getUTCTimestamp(data.get("timestamp"))
            my_record.stop_parking = stoptime
            my_record.parking_duration = (stoptime - my_record.start_parking)
            my_record.save()
        #delete current session data
        try:
            del request.session["open_session"]
        except KeyError:
            pass
        messages.success(request, "You have successfully recorded the time of departure. Record complete.")
        return JsonResponse({'status': 'Parking spot finalized' })
    else:
        messages.error(request, "An error occurred")
        return JsonResponse({'status': 'Unsuccessful'})

class PSListView(LoginRequiredMixin, ListView):
    login_url = 'accounts/login/'
    model = ParkingSpot
    paginate_by = 15
    context_object_name = 'my_ps_list'

    def get_queryset(self):
        return ParkingSpot.objects.filter(user = self.request.user, is_deleted = False).reverse()[:101]

    # Pass google maps api key from settings to template
    def get_context_data(self, **kwargs):
        context = super(PSListView, self).get_context_data(**kwargs)
        context['maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context


class PSDetailView(LoginRequiredMixin, DetailView):
    login_url = 'accounts/login/'
    model = ParkingSpot

    #Pass google maps api key from settings to template
    def get_context_data(self, **kwargs):
        context = super(PSDetailView, self).get_context_data(**kwargs)
        context['maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context

def getUTCTimestamp(time_string):
    return datetime.datetime.strptime(time_string, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=pytz.UTC)

