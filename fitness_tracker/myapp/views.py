from django.shortcuts import render,redirect 
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth import get_user_model ,authenticate ,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from decimal import Decimal
from .models import ModuleCompletion
from datetime import datetime
import matplotlib.pyplot as plt
from datetime import timedelta
from django.utils import timezone
from datetime import date
import io
import base64

# Create your views here.
def index(request):
    return render(request,'home.html')
def contact(request):
    return render(request,'contact.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Use the authenticate() function to check the username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            # Redirect to a success page or home page
            return redirect('dashboard')
        else:
            # Authentication failed, show an error message
            messages.error(request, 'Invalid username or password. Please try again.')

    # Render the login template
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        # Retrieve user input from the form
        username = request.POST['username']
        password = request.POST['pass1']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        height = request.POST['height']
        weight = request.POST['weight']
        age = request.POST['age']
        email = request.POST['email'] 
        phone_number = request.POST['phoneNumber']
        gender = request.POST.get('gender')
        date_of_birth = request.POST['dob']  # Add this line

        # Create a new User
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name,email=email)
        user.save()

        # Create a UserProfile associated with the user
        user_profile = UserProfile(user=user, height=height, weight=weight, age=age, phone_number=phone_number, gender=gender, date_of_birth=date_of_birth)  # Add date_of_birth
        user_profile.save()

        messages.success(request,"User Created Successfully!!")
        return redirect('login')
    return render(request,'signup.html')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from .models import UserProfile

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    # Retrieve user-specific data from the UserProfile model
    user_profile = UserProfile.objects.get(user=request.user)  # Assuming UserProfile is linked to User using a OneToOneField
    weight_kg = user_profile.weight
    height_ft = user_profile.height
    bmi = ((weight_kg * Decimal('2.20462')) / ((height_ft * Decimal('12')) ** 2)) * Decimal('703')
    if request.method=="POST":
        if request.POST.get("form_type")=='stepsForm':
            numberOfSteps = request.POST['numberOfSteps'] 
            current_date = datetime.now().date()  
            daily_data, created = DailyData.objects.get_or_create(
                user=request.user,
                date=current_date,
                defaults={'steps': numberOfSteps}
            )

            if not created:
                # If the record already exists, update the steps
                daily_data.steps = numberOfSteps
                daily_data.save()

        if request.POST.get("form_type")=='caloriesForm':
            calories_burned = request.POST['Calories-burned'] 
            calories_intake = request.POST['Calories-intake']
            current_date = datetime.now().date()  
            daily_data, created = DailyData.objects.get_or_create(
                user=request.user,
                date=current_date,
                defaults={'calories_burned': calories_burned,
                          'calories_intake':calories_intake }
            )

            if not created:
                daily_data.calories_burned = calories_burned
                daily_data.calories_intake = calories_intake
                daily_data.save()


    end_date = datetime.now().date() 
    start_date = end_date - timedelta(days=6)  # 7 days ago

    daily_data = DailyData.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).order_by('date')
    dates = [entry.date for entry in daily_data]

    steps = [entry.steps for entry in daily_data]
    Calories_burned =[entry.calories_burned for entry in daily_data]
    Calories_intake =[entry.calories_intake for entry in daily_data]
    # Pass the user_profile data to the template
    plt.figure(figsize=(10, 6))  # Set the figure size
    c = ['b', 'g', 'r', 'c', 'orange', 'y', 'k']
    plt.bar(dates, steps,  alpha=0.7 , color=c)  # Create a bar chart
    plt.title('Last 7 Days Steps')
    plt.xlabel('Date')
    plt.ylabel('Steps')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.figure(figsize=(10, 6))  # Set the figure size
    plt.plot(dates, Calories_burned, label='Calories Burned', color='green')
    plt.plot(dates, Calories_intake, label='Calories Intake', color='red')
    plt.title('Last 7 Days Calories Burned/Intake')
    plt.xlabel('Date')
    plt.ylabel('Calories')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    
    buf1.seek(0)
    plot_chart = base64.b64encode(buf1.read()).decode('utf-8')
    buf1.close()
    context = {
        'user_profile': user_profile,
        'bmi': bmi,
        'user_first_name': request.user.first_name,
        'plot_data' : plot_data,
        'plot_data2' : plot_chart,
    }


    return render(request, 'dashboard.html', context)
@login_required


def exercise_view(request):
    # Retrieve all ModuleCompletion objects for the current user
    module_completions = ModuleCompletion.objects.filter(
        user=request.user,
        completed_date=date.today() 

    )
    

    # Get a list of completed modules
    completed_modules = [completion.module for completion in module_completions]
    
    # Define a list of all module names (modify this list according to your modules)
    all_modules = ['module1', 'module2', 'module3', 'module4', 'module5', 'module6']

    # Create a dictionary to store module completion status
    module_status = {}

    # Populate the dictionary with module names and completion status
    for module in all_modules:
        module_status[module] = module in completed_modules
    print(module_status)
    context = {
        'user_first_name': request.user.first_name,
        'module1_status': module_status['module1'],
        'module2_status': module_status['module2'],
        'module3_status': module_status['module3'],
        'module4_status': module_status['module4'],
        'module5_status': module_status['module5'],
        'module6_status': module_status['module6'],
    }

    return render(request, 'exercise.html', context)

    
from django.http import JsonResponse


def mark_as_completed(request, module_id):
    
    if request.user.is_authenticated:
        # Check if the user is logged in
        try:
            today = date.today()
            module_completion = ModuleCompletion.objects.get(user=request.user, module=module_id,completed_date=today)
            module_completion.completed = True
            module_completion.save()
            return JsonResponse({"message": "Module marked as completed"})
        except ModuleCompletion.DoesNotExist:
            # If the record does not exist, create a new one
            ModuleCompletion.objects.create(user=request.user, module=module_id, completed=True,completed_date=today)
            return JsonResponse({"message": "Module marked as completed"})
    else:
        return JsonResponse({"error": "User is not authenticated"})
@login_required
def update_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        if 'height' in request.POST:
            height = request.POST['height']
            user_profile.height = height
        if 'weight' in request.POST:
            weight = request.POST['weight']
            user_profile.weight = weight
        if 'age' in request.POST:
            age = request.POST['age']
            user_profile.age = age
        
        
        
        user_profile.save()
        return redirect('dashboard')
    return render(request,'update.html')