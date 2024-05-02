from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import ProductionLogForm, ProductionLog, MachineLogForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from datetime import datetime, time, timedelta, date
from .models import Machine, ProductionLog
from django.http import JsonResponse
import random
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist




def login_view(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('machine_log')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def add_production_log(request):
    if request.method == 'POST':
        # production =ProductionLog.object.all()
        form = ProductionLogForm(request.POST)
        if form.is_valid():
            production_log = form.save()
            # Calculate OEE here
            return redirect('machine_log')  # Redirect to a success page
    else:
        form = ProductionLogForm()
    return render(request,'index.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to home page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def machine_log(request):
    if request.method == 'POST':
        form = MachineLogForm(request.POST)
        if form.is_valid():
            machine_log = form.save()
            return redirect('add_production_log')
        
    else:
        form = MachineLogForm()
    return render (request, 'machine.html', {'form' : form})    


@csrf_exempt
def simulate_machine(request):
    if request.method == 'GET':
        machine = Machine.objects.get(machine_name="CNC")

        available_time_per_shift = 8
        ideal_cycle_time = 5
        num_shifts = 3
        num_products_per_shift = 100

        for shift in range (1,num_shifts+1):
            available_operating_time = available_time_per_shift*60*num_products_per_shift

            for product_num in range (1,num_products_per_shift+1):
                start_time = datetime.now()
                end_time = start_time + timedelta(minutes=random.uniform(ideal_cycle_time-1,ideal_cycle_time+1))    
                duration= (end_time-start_time).total_seconds() / 3600 

                actual_output = 1

                if duration == ideal_cycle_time:
                    good_product=1
                    bad_product=0
                else:
                    good_product=0
                    bad_product=1

                ProductionLog.objects.create(
                    cycle_no=f"CN00{product_num}",
                    unique_id=f"UID00{product_num}",
                    material_name="Material",
                    machine=machine,
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration)
                #     actual_output=actual_output,
                #     good_product=good_product,
                #     bad_product=bad_product,
                # )    
                
        return JsonResponse({"message" :"Machine simulation data generated successfully."})
    else:
        return JsonResponse ({"error": "Only POST request are allowed"})


# def calculate_oee(request,available_time_per_shift, ideal_cycle_time, production_logs):
def calculate_oee(request):
    if request.method == 'GET':
        production_logs=ProductionLog.objects.all()
        available_time_per_shift=8*60
        ideal_cycle_time=5
        
        total_shifts = len(production_logs)
        total_available_time = available_time_per_shift * total_shifts  # Total available time in minutes
        total_actual_output = sum(log.actual_output for log in production_logs)
        total_good_products = sum(log.good_product for log in production_logs)
        total_products_produced = sum(log.actual_output for log in production_logs)

        # Calculate Availability
        available_operating_time = total_actual_output * ideal_cycle_time
        unplanned_downtime = total_available_time - available_operating_time
        availability = (total_available_time - unplanned_downtime) / total_available_time * 100

        # Calculate Performance
        performance = (ideal_cycle_time * total_actual_output) / available_operating_time * 100

        # Calculate Quality
        quality = (total_good_products / total_products_produced) * 100

        # Calculate OEE
        oee = availability * performance * quality / 10000  # Divide by 10000 to get percentage

        # return oee
        return JsonResponse({'oee': oee})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def add_production_entry(request):
    # Assuming machine_name is provided and exists in the database
    if request.method== 'GET':
        machine_name="CNC",
        start_time=datetime(2024, 4, 28, 8, 0),  # Example start time
        end_time=datetime(2024, 4, 28, 16, 0),   # Example end time
        actual_output=100,  # Example actual output
        good_product=90,
        duration=0
        machine = Machine.objects.get(machine_name="CNC")
        # Creating a new production log entry
        production_log = ProductionLog.objects.create(
            machine=machine,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            actual_output=actual_output,
            good_product=good_product
            # total_product=actual_output  # Assuming all produced products are accounted for
        )
        return production_log
        # return JsonResponse({"production_log": production_log})

# Add a production entry
# production_log_entry = add_production_entry(
#     machine_name="CNC",
#     start_time=datetime(2024, 4, 28, 8, 0),  # Example start time
#     end_time=datetime(2024, 4, 28, 16, 0),   # Example end time
#     actual_output=100,  # Example actual output
#     good_product=90,
#     duration=0  # Example good product count
# )

# Calculate OEE
# oee = calculate_oee(request='GET',available_time_per_shift=8*60, ideal_cycle_time=5, production_logs=ProductionLog.objects.all() )
# print("OEE:", oee)



# def calculate_oee(request):
#     if request.method == 'GET':

#         try:
#             machine = Machine.objects.get(machine_name="CNC")
#         except ObjectDoesNotExist:
#             print(f"Machine CNC does not exist in the database.")
#             return None
#         # machine = Machine.objects.get(machine_name=machine_name)
#         total_shifts = 3  # Assuming 3 shifts in a day

#         # Initialize variables to calculate Availability, Performance, and Quality
#         total_available_time = 8 * 60 * total_shifts  # Total available time in minutes
#         total_planned_downtime = 0
#         total_ideal_cycle_time = 5
#         total_actual_output = 0
#         total_good_products = 0
#         total_products_produced = 0

#         # Retrieve production logs for the machine
#         production_logs = ProductionLog.objects.filter(machine=1)

#         for log in production_logs:
#     # Calculate planned downtime (unplanned downtime not considered in this simulation)
#             total_planned_downtime += (log.end_time - log.start_time).total_seconds() / 3600
                    
#             # Calculate actual output and good products
#             total_actual_output += log.actual_output
#             total_good_products += log.good_product

#             # Count total products produced
#             total_products_produced += 1
        
        
        
#         # for log in production_logs:
#         #     # Calculate planned downtime (unplanned downtime not considered in this simulation)
#         #     total_planned_downtime += (log.end_time - log.start_time).total_seconds() / 3600
            
#         #     # Calculate actual output and good products
#         #     total_actual_output += log.actual_output
#         #     total_good_products += log.good_product

#         #     # Count total products produced
#         #     total_products_produced += 1

#         # Calculate Availability
#         availability = (total_available_time - total_planned_downtime) / total_available_time * 100

#         # Calculate Performance
#         performance = (total_ideal_cycle_time * total_actual_output) / total_available_time * 100

#         # Calculate Quality
#         quality = (total_good_products / total_products_produced) * 100

#         # Calculate OEE
#         oee = availability * performance * quality / 10000  # Divide by 10000 to get percentage

#         return oee

# Example usage:
    # machine_name = Machine.machine_name
# machine_name = "CNC"
# oee = calculate_oee(machine_name)
# print(f"OEE for {machine_name}: {oee}%")
      


# def oeeFormula(request, pk):
#     if request.method == 'POST':
#         machineObj= ProductionLog.objects.get(id=pk)
       
       
       

#     machine_startTime = machineObj.start_time
#     machine_endTime = machineObj.end_time

#     available_time_per_shift = 8
#     ideal_cycle_time = 5
#     num_shifts = 3
#     num_products_per_shift = 100

#     availableOperatingTime = (num_products_per_shift)*(ideal_cycle_time)
#     unplannedDownTime = (available_time_per_shift-availableOperatingTime)

    
    



        












# def oeeFormula(request):
#     if request.method == 'GET':
#         form = ProductionLogForm()
#         formField = form.start_time
#         hour = range(00, 24)
#         minute = range(00, 60)
#         availableTime = range(0,8)
#         NoofProducts = ProductionLog.material_name
#         idealCycleTime = 
#         availOperatingTime = NoofProducts * idealCycleTime
#         unplannedDowntime = availableTime - availOperatingTime
#         availability = (((availableTime - unplannedDowntime ) / availableTime) * 100)/100

#     if request.method == 'POST':
#         currentDateTime = datetime.now()
#         currentHourObj = datetime.strftime((currentDateTime)+ '8', "%H") 
#         currentMinuteObj = datetime.strftime((currentDateTime)+'0', "%M")    