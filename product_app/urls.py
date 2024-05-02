from django.urls import path
from .views import add_production_log, login_view, machine_log, register_view, simulate_machine, calculate_oee, add_production_entry

urlpatterns = [
    path('', login_view, name='login'),
    path('register_view', register_view, name='register_view'),
    path('add_production_log/', add_production_log, name='add_production_log' ),
    path('machine_log', machine_log, name='machine_log'),
    path('simulate_machine', simulate_machine, name='simulate_machine'),
    path('calculate_oee', calculate_oee, name='calculate_oee'),
    path('add_production_entry', add_production_entry, name='add_production_entry'),
]
