from django import forms
from .models import ProductionLog, Machine

class ProductionLogForm(forms.ModelForm):
    class Meta:
        model = ProductionLog
        fields = ['cycle_no', 'unique_id', 'material_name', 'machine', 'start_time', 'end_time', 'duration']


        
class MachineLogForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['machine_name', 'machine_serial_no']