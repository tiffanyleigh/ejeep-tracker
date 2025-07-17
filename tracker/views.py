from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import StartDriveForm, PassengerForm
from .models import DriveSession, StopLog
from .forms import StopTrackingForm
from .routes import ROUTES


ROUTES = {
    'Express Line B': [
        'Areté',
        'Bellarmine Hall',
        'Junior High School',
        'Senior High School FLC',
        'Bellarmine Hall',
        'Social Development Complex (SDC)'
    ],
    'Line B': [
        'Areté',
        'Xavier Hall',
        'Cervini Hall',
        'Junior High School',
        'Senior High School FLC',
        'Bellarmine Hall',
        'Social Development Complex (SDC)'
    ],
    'Express Line A': [
        'Grade School',
        'JSEC',
        'Old Library',
        'Xavier Hall',
        'Cervini Hall',
        'Old Communications Building',
        'Hagdan na Bato'
    ]
}

def landing(request):
    return render(request, 'tracker/landing.html')

@login_required
def dashboard(request):
    return render(request, 'tracker/driver_dashboard.html', {'driver': request.user})

@login_required
def start_drive(request):
    if request.method == 'POST':
        ejeep_letter = request.POST.get('ejeep_letter')
        route = request.POST.get('route')
        session = DriveSession.objects.create(
            driver=request.user,
            ejeep_letter=ejeep_letter,
            route=route,
            current_stop_index=0,
            in_transit=True  
        )
        return redirect('drive_route', session_id=session.id)
    return render(request, 'tracker/start_drive.html')

@login_required
def drive_route(request, session_id):
    session = get_object_or_404(DriveSession, id=session_id)
    stops = ROUTES[session.route]
    current_stop_index = session.current_stop_index % len(stops)
    current_stop = stops[current_stop_index]
    next_stop = stops[(current_stop_index + 1) % len(stops)]

    if request.method == 'POST':
        if request.POST.get('action') == 'end-route':
            return redirect('dashboard')
        form = PassengerForm(request.POST)
        if form.is_valid():
            passengers_in = form.cleaned_data['passengers_in'] or 0
            passengers_out = form.cleaned_data['passengers_out'] or 0
            arrived_time = timezone.now()

            session.passengers_in += passengers_in
            session.passengers_out += passengers_out

            current_net_passengers = session.passengers_in - session.passengers_out

            StopLog.objects.create(
                drive_session=session,
                stop_name=current_stop,
                arrived_at=arrived_time,
                departed_at=arrived_time,
                passengers_in=passengers_in,
                passengers_out=passengers_out,
                net_passengers=current_net_passengers,
                driver_name=request.user.get_full_name() if hasattr(request.user, 'get_full_name') else str(request.user)
            )


            session.current_stop_index = (current_stop_index + 1) % len(stops)
            session.save()

            return redirect('drive_route', session_id=session.id)

    else:
        form = PassengerForm()

    net_passengers = session.passengers_in - session.passengers_out
    return render(request, 'tracker/track_stop.html', {
        'form': form,
        'session': session,
        'current_stop': current_stop,
        'next_stop': next_stop,
        'net_passengers': net_passengers,
    })


from django.http import HttpResponse

@login_required
def change_route(request):
    return HttpResponse("Change Route page (not implemented yet).")

@login_required
def track_stop(request):
    session = get_object_or_404(DriveSession, driver=request.user, in_transit__in=[True, False])

    route_stops = ROUTES.get(session.route, [])
    current_index = session.current_stop_index

    if current_index >= len(route_stops):
        return render(request, 'tracker/track_stop.html', {
            'session': session,
            'current_stop': "Route Complete",
            'next_stop': "N/A",
            'form': None,
        })

    current_stop = route_stops[current_index]
    next_stop = route_stops[current_index + 1] if current_index + 1 < len(route_stops) else "End of Route"

    if request.method == 'POST':
        if not session.in_transit:
            # Departing current stop
            session.in_transit = True
            session.save()
        else:
            # Arrived at stop: log data and move to next stop
            form = StopTrackingForm(request.POST)
            if form.is_valid():
                StopLog.objects.create(
                    driver=request.user,
                    ejeep_letter=session.ejeep_letter,
                    route=session.route,
                    stop_name=current_stop,
                    arrived_at=session.started_at,
                    departed_at=now(),
                    passengers_in=form.cleaned_data['passengers_in'],
                    passengers_out=form.cleaned_data['passengers_out'],
                    net_passengers=form.cleaned_data['passengers_in'] - form.cleaned_data['passengers_out']
                )
                session.current_stop_index += 1
                session.in_transit = False
                session.started_at = now()
                session.save()
        return redirect('track_stop')

    form = StopTrackingForm()

    return render(request, 'tracker/track_stop.html', {
        'session': session,
        'current_stop': current_stop,
        'next_stop': next_stop,
        'form': form,
    })

