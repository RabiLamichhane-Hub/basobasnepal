from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Province, Municipality, District
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from allauth.socialaccount.models import SocialAccount
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json


# Create your views here.

def startup(request):
    return render(request, 'startup.html')

def home(request):
    rooms = Room.objects.all()  # Shows latest rooms first
    districts = Room.objects.values_list('district', flat=True).distinct()
    return render(request, 'home.html', {
        'rooms': rooms,
        'districts': districts,
        'user': request.user
    })

def filter_rooms(request):
    district = request.GET.get('district', None)

    if district:
        rooms = Room.objects.filter(district=district)
    else:
        rooms = Room.objects.all()

    rooms_data = []
    for room in rooms:
        rooms_data.append({
            'pk': room.pk,
            'location_municipality': room.municipality,
            'location_ward_num': room.ward_num,
            'location_district': room.district,
            'num_of_rooms_available': room.num_of_rooms_available,
            'photo_url': room.photos.url if room.photos else '',
            'is_owner': request.user == room.owner,
        })

    return JsonResponse({'rooms': rooms_data})

@login_required(login_url='custom_login')
def landlord(request):
    provinces = Province.objects.all()

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            
            # Assign foreign keys
            province_id = request.POST.get('province')
            district_id = request.POST.get('district')
            municipality_id = request.POST.get('municipality')

            if province_id and district_id and municipality_id:
                room.province = Province.objects.get(pk=province_id)
                room.district = District.objects.get(pk=district_id)
                room.municipality = Municipality.objects.get(pk=municipality_id)
                room.owner = request.user
                room.save()
                return redirect('home')  # ✅ success!
        else:
            print(form.errors)  # 🔍 see validation issues in console

    else:
        form = RoomForm()

    return render(request, 'landlord.html', {
        'form': form,
        'provinces': provinces
    })

def description(request, pk):
    rooms = get_object_or_404(Room, pk= pk)
    return render(request, 'description.html', {'rooms': rooms})

@login_required
def delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        response = request.POST.get('response')

        if response == 'yes':
            room.delete()
            return redirect('home')
        elif response == 'no':
            return redirect('home')
    return render(request, 'delete.html', {'room':room})

def edit(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home') # Or wherever you want to redirect after success
    else:
        form = RoomForm(instance=room)

    # Fetch all possible options for the client-side filtering
    districts = list(District.objects.values('id', 'name', 'province_id'))
    municipalities = list(Municipality.objects.values('id', 'name', 'district_id'))

    context = {
        'form': form,
        'room': room, # Pass the whole room object for easy access
        'districts_json': json.dumps(districts),
        'municipalities_json': json.dumps(municipalities),
    }
    return render(request, 'edit.html', context)


def custom_login(request):
    return render(request, 'login.html')

def logout_confirm(request):
    return render(request, 'logout.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')

@login_required
def profile(request):
    try:
        # Get social account info (Google)
        social_account = SocialAccount.objects.get(user=request.user, provider='google')
        picture_url = social_account.extra_data.get('picture')
    except SocialAccount.DoesNotExist:
        picture_url = None  # fallback if user didn’t log in via Google

    return render(request, 'profile.html', {
        'user': request.user,
        'picture_url': picture_url
    })

def load_districts(request):
    province_id = request.GET.get('province_id')
    districts = []
    if province_id:
        districts = list(District.objects.filter(province_id=province_id).values('id', 'name'))
    return JsonResponse(districts, safe=False)

def load_municipalities(request):
    district_id = request.GET.get('district_id')
    municipalities = []
    if district_id:
        municipalities = list(Municipality.objects.filter(district_id=district_id).values('id', 'name'))
    return JsonResponse(municipalities, safe=False)