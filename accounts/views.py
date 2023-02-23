from django.shortcuts import redirect, render,HttpResponse
from .forms import *
from django.contrib import messages

# Create your views here.


def registerUser(request):
    if request.method == 'POST':
        # Create the user using create_user method
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request,'Passwords do not match. ')
            # return redirect ('registerUser')
        if User.objects.filter(email=email).exists() :
            messages.error(request,'Email already Exist.')
        elif User.objects.filter(username=username).exists():
            messages.error(request,'Username already Exist.')                
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,'User have been register sucessfully')
        return redirect('registerUser')
    return render(request, 'accounts/registerUser.html')
