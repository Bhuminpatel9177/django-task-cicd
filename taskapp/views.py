from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import requests
from .models import *
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
import random
import string
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        gender = requests.get(f'https://api.genderize.io/?name={first_name}').json()['gender']
        print(gender)
        error = {}
        if not first_name:
            error["first_name"]="First Name field is required"

        last_name = request.POST.get('last_name')
        if not last_name:
            error["last_name"]="Last Name field is required"

        email = request.POST.get('email')
        if not email:
            error["email"]="Email field is required"

        mobile = request.POST.get('mobile')
        if not mobile:
            error["mobile"]="Mobile field is required"

        dob = request.POST.get('dob')
        if not dob:
            error["dob"]="Date Of Birth field is required"

        password = request.POST.get('password')
        if not password:
            error["password"]="Password field is required"

        cpassword = request.POST.get('cpassword')
        if not cpassword:
            error["cpassword"]="Confirm Password field is required"
        elif password != cpassword:
            error["cpassword"] = "Password Does Not Same" 

        hobbies = request.POST.getlist('hobbies[]')
        print(hobbies)
        hobbie = ','.join(hobbies)
        # if password != cpassword:
        #     error["cpassword"] = "Password Does Not Same" 

        if not hobbies:
            error["hobbies"]="Hobbies field is required"

        if bool(error):
            print("Called")
            return JsonResponse({"error": True, "statusCode": 422, "message": "failed", "errors": error}, status=422)

        print(first_name, last_name, email, mobile, dob, password, cpassword, hobbies)
        

        date_of_birth = datetime.strptime(str(dob), "%Y-%m-%d")
        current_date = datetime.strptime(str(datetime.now()).split(' ')[0], "%Y-%m-%d")

        # Calculate the age
        age = current_date.year - date_of_birth.year - ((current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day))
        print("Data: ", first_name, last_name, email, mobile, email, password,dob,hobbies, age)

        username = first_name + last_name
        if len(CustomUser.objects.filter(email=email)) == 0 :
            user = CustomUser.objects.create_user(username = first_name + last_name, first_name=first_name,last_name=last_name,mobile=mobile ,email=email,gender=gender, dob=dob,password=password)
            extra = ExtraField.objects.create(customuser=user, age=age, hobbies=hobbie)

            return redirect('login')
            # return JsonResponse({'success': True, 'message': 'Successfully created', 'url': '/admin/supervisor_create/'}, status=200)

        error['email'] = 'Email is already exist'
        return JsonResponse({"error": False, "statusCode": 422, "errors": error}, status=422)

    return render(request, 'register.html')


def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    return otp


def send_otp_email(email, otp_code):
    subject = 'Your OTP for login'
    message = f'Your OTP is: {otp_code}'
    send_mail(subject, message, 'bhumin.thinktanker@gmail.com', [email])

flag_otp = False

@csrf_exempt
def login(request):
    global flag_otp
    if request.method == 'POST':
        error = {}
        email = request.POST.get('email')
        verify_email = CustomUser.objects.filter(email=email).count()


        if not email:
            error["email"] = "Email field is required"
            return JsonResponse({"error": True, "statusCode": 422, "message": "failed", "errors": error}, status=422)
        elif verify_email == 0:
            error["email"] = "Email is Not Verified"
            return JsonResponse({"error": True, "statusCode": 422, "message": "failed", "errors": error}, status=422)

        # Assuming password validation logic here
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        

        if not password:
            error["password"] = "Password field is required"
            return JsonResponse({"error": True, "statusCode": 422, "message": "failed", "errors": error}, status=422)
        elif user is None:
            error["password"] = "Invalid credentials"
            return JsonResponse({"error": True, "statusCode": 422, "message": "failed", "errors": error}, status=422)
        elif user and flag_otp == False:
            otp = generate_otp()

            otp_ver = CustomUser.objects.get(email=email)
            otp_ver.otp = otp
            otp_ver.save()

            send_otp_email(email, otp)
            flag_otp =  True
            print(flag_otp)
            error["otp"] = "OTP field is required"                              
            return JsonResponse({"error": True, "statusCode": 422, "message": "failed", "errors": error}, status=422)
        elif flag_otp == True:
            print(flag_otp)
            print("CAlled")
            otp_r = request.POST.get('otp')
            if not otp_r:                  
                error["otp"] = "Must OTP field is required"                              
                return JsonResponse({"error": True, "statusCode": 422, "message": "failed", "errors": error}, status=422)
            else:
                if CustomUser.objects.get(email=email).otp == otp_r:
                    flag_otp = False
                    try:
                        error.pop('otp', None)
                        print("called_otp")
                    except:
                        pass
                else:
                    error["otp"] = "OTP TO SAHI DAL"  
                    return JsonResponse({"error": True, "statusCode": 422, "message": "failed", "errors": error}, status=422)                            

        # return JsonResponse({"error": True, "statusCode": 422, "message": "failed", "errors": error}, status=422)
            
        if bool(error):
            return JsonResponse({"error": True, "statusCode": 422, "message": "failed", "errors": error}, status=422)
        
        
    return render(request, 'login.html')


def users_data(request):

    users = ExtraField.objects.select_related('customuser').all()

    paginator = Paginator(users,2)

    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except EmptyPage:
        users = paginator.page(paginator.num_page)
    except PageNotAnInteger:
        users = paginator.page(1)

    return render(request, 'user_data.html', {"users":users})

def logout(request):
    auth_logout(request)
    return redirect('login')