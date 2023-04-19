from django.shortcuts import redirect, render,HttpResponse
from accounts.utils import detectUser

from vendor.forms import VendorForm
from .forms import *
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required,user_passes_test
from zwigato.decorators import *


from django.contrib import messages,auth

# Create your views here.


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('custDashboard')
    elif request.method == 'POST':
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

def registerVendor(request):

    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('custDashboard')
    elif request.method == 'POST':
        #store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            # vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            
            # Send verification email
            # mail_subject = 'Please activate your account'
            # email_template = 'accounts/emails/account_verification_email.html'
            # send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Your account has been registered successfully! Please wait for the approval.')
            return redirect ('registerVendor')
        else:
            # print('invalid form')
            print(form.errors)
        
    else:
        form = UserForm()
        v_form = VendorForm()
    
    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html',context)
    


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
        return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
        return render(request, 'accounts/vendorDashboard.html')
