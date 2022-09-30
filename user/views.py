
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, AccountUpdateForm
from django.contrib.auth.models import User, auth
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = RegistrationForm(request.GET)
        context = { 'form' : form}
        return render(request, 'user/register.html', context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            EmailOrUsername = form.cleaned_data.get('EmailOrUsername')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            try:
                found_username = User.objects.get(email=EmailOrUsername)
                user = auth.authenticate(username=found_username, password=password )

            except:
                user = auth.authenticate(username=EmailOrUsername, password=password )

            
            if user is not None:
                auth.login(request, user)
                messages.success(request,'Login Successful!')
                return redirect('home')
            else:
                messages.warning(request, 'Invalid Credentials!')
                return redirect('login')
    else:

        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})


def logout(request):
    if request.method== "POST":
        auth.logout(request)
        messages.warning(request, 'Logged out!')
        return redirect('home')
    else:
        return render(request, 'user/logout.html')


def account(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AccountUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                if form.has_changed():
                    form.save()
                    messages.success(request, 'Account has been updated!')
                    return redirect('account')
                else:
                    messages.info(request, 'No changes')
                    return redirect('account')
            else:
                messages.warning(request, 'There is something wrong with your form data!')
                return redirect('home')
        else:
            form = AccountUpdateForm(instance=request.user)
            context = { 'form' : form}
            return render(request, 'user/account.html', context)
    else:
        return redirect('login')
