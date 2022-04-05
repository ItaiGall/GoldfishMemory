import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
import django.contrib.messages as messages
from .forms import SignUpForm, ChangeUserInfoForm, RegisterVehicleForm
from GoldfishMemory_App.models import ParkingSpot, Vehicle
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests

def reCAPTCHA_validation(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()
    #print(result)

def signup_view(request):
    form = SignUpForm()
    vehicle_form = RegisterVehicleForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        vehicle_form = RegisterVehicleForm(request.POST)
        if form.is_valid():
            #reCAPTCHA validation
            reCAPTCHA_validation(request)

            user = form.save()
            #affiliate vehicle with user
            vehicle = vehicle_form.save(commit=False)
            vehicle.affiliated_users = user
            vehicle.save()

            authenticate(username=user.username, password=user.password)
            messages.success(request, 'Account created successfully')
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "A problem occurred during signup. Try again.")
            return render(request, 'accounts/signup.html', {"form": form, "vehicle_form":vehicle_form,
                                                            'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY })
    return render(request, 'accounts/signup.html', {"form":form, "vehicle_form":vehicle_form,
                                                    'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})

def login_view(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #reCaptcha validation
            reCAPTCHA_validation(request)

            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, 'Hello {}! You have been logged in'.format(user.username))
                return redirect('homepage')
            else:
                messages.error(request, 'Login failed!')
        else:
            messages.error(request, 'Login failed!')
    return render(request, 'accounts/login.html', { "form": form, "user":request.user.username,
                                                    'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY })

def logout_view(request):
        logout(request)
        return redirect('homepage')


@login_required(login_url='/accounts/login/')
def change_credentials(request):
    user_form = ChangeUserInfoForm(instance=request.user)
    pw_form = PasswordChangeForm(request.user)
    if request.method == 'POST' and 'change_userinfo' in request.POST:
        user_form = change_userinfo(request)
    elif request.method =='POST' and 'change_password' in request.POST:
        pw_form = change_password(request)
        logout(request)
        return redirect('Accounts_App:login')
    return render(request, 'accounts/change_cred.html', {'user_form': user_form, 'pw_form': pw_form})

@login_required(login_url='/accounts/login/')
def change_password(request):
    pw_form = PasswordChangeForm(request.user)
    pw_change_form = PasswordChangeForm(request.user, request.POST)
    if pw_change_form.is_valid():
        pswrd = pw_change_form.save()
        update_session_auth_hash(request, pswrd)
        messages.success(request, 'Your password was successfully updated!')
        return pw_form
    else:
        messages.error(request, "Error")
        return pw_form

@login_required(login_url='/accounts/login/')
def change_userinfo(request):
    user_form = ChangeUserInfoForm(instance=request.user)
    user_form_changed = ChangeUserInfoForm(request.POST, instance=request.user)
    if user_form_changed.is_valid():
        user = user_form_changed.save()
        user_form.username = user_form_changed.cleaned_data.get('username')
        user_form.email = user_form_changed.cleaned_data.get('email')
        update_session_auth_hash(request, user)
        messages.success(request, 'Your info was successfully updated!')
        return user_form_changed
    else:
        messages.error(request, "Error")
        return user_form

@login_required(login_url='/accounts/login/')
def user_stats(request):
    my_user = request.user
    if my_user:
        #convert UTC timestamp from DB to local timestamp in template
        utcoffset = datetime.datetime.now(datetime.timezone.utc).astimezone().utcoffset()
        if utcoffset:
            my_user.last_login = my_user.last_login + utcoffset
            my_user.date_joined = my_user.date_joined + utcoffset
        #determine the number of db entries of this user
        entries = ParkingSpot.objects.filter(user = my_user).count()
        #get the vehicle affiliated with this user
        my_vehicle = Vehicle.objects.filter(affiliated_users = my_user)
        return render(request, 'accounts/user_stats.html', { 'user': my_user, 'entries': entries, 'my_vehicle':my_vehicle })
    else:
        return render(request, 'accounts/login.html')
