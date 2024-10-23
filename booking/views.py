from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import CustomUser, Shift, Slot, PatientBooking
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import logout

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']  # Assuming you have this in your form
        user = CustomUser.objects.create_user(email=email, password=password, role=role)
        return redirect('user_panel')  # Redirect to the user panel after signup
    return render(request, 'booking/signup.html')  # Render your signup template

def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_panel')
    return render(request, 'booking/signin.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('signin')

@login_required
def add_shift(request):
    if request.method == "POST":
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        interval = int(request.POST['interval'])
        shift = Shift.objects.create(doctor=request.user, start_time=start_time, end_time=end_time, interval=interval)

        # Create slots based on the shift
        current_time = timezone.datetime.combine(timezone.now().date(), shift.start_time)
        end_time = timezone.datetime.combine(timezone.now().date(), shift.end_time)
        while current_time < end_time:
            Slot.objects.create(shift=shift, time=current_time.time())
            current_time += timezone.timedelta(minutes=interval)

        return redirect('doctor_panel')
    return render(request, 'booking/add_shift.html')

@login_required
def receptionist_panel(request):
    if request.user.role != 'Receptionist':
        return redirect('signin')

    slots = Slot.objects.filter(shift__doctor=request.user)  # Get slots for the doctor
    return render(request, 'booking/receptionist_panel.html', {'slots': slots})

@login_required
def book_slot(request, slot_id):
    if request.method == "POST":
        patient_name = request.POST['patient_name']
        slot = Slot.objects.get(id=slot_id)
        if not slot.is_booked:
            PatientBooking.objects.create(patient_name=patient_name, slot=slot)
            slot.is_booked = True
            slot.save()
        return redirect('receptionist_panel')

@login_required
def doctor_panel(request):
    if request.user.role != 'Doctor':
        return redirect('signin')
    shifts = Shift.objects.filter(doctor=request.user)
    return render(request, 'booking/doctor_panel.html', {'shifts': shifts})



def user_panel(request):
    return render(request, 'booking/user_panel.html')  # Render your user panel template
