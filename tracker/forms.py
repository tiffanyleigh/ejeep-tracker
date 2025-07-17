from django import forms

ROUTE_CHOICES = [
    ('Line B', 'Line B'),
    ('Express Line A', 'Express Line A'),
    ('Express Line B', 'Express Line B'),
]

class StartDriveForm(forms.Form):
    ejeep_letter = forms.CharField(label='E-Jeep Letter', max_length=10)
    route = forms.ChoiceField(label='Route', choices=ROUTE_CHOICES)

class PassengerForm(forms.Form):
    passengers_in = forms.IntegerField(label='Passengers In', required=False, min_value=0)
    passengers_out = forms.IntegerField(label='Passengers Out', required=False, min_value=0)

class StopTrackingForm(forms.Form):
    passengers_in = forms.IntegerField(min_value=0, required=False, label="Passengers In")
    passengers_out = forms.IntegerField(min_value=0, required=False, label="Passengers Out")

