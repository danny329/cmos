from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth, Group
from .models import UserExtend
import sweetify
from homepage.views import shopplus



# Create your views here.

def login(request):
    try:
        if request.user.is_authenticated:
            return redirect('/')
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                usergroup = Group.objects.get(name='vendor')
                if request.user.groups.filter(name=usergroup).exists():
                    sweetify.success(request, 'Log in Successful! \n hello, ' + str(request.user))
                    return redirect('/vendor_home/')
                else:
                    sweetify.success(request, 'Log in Successful! \n hello, ' + str(request.user))
                    return redirect('/')
            else:
                sweetify.error(request, 'User doesn\'t exist - register to CMOS ')

        return render(request, 'login.html')
    except Exception as e:
        print(e)

def register_verify(request):
    try:
        if request.user.is_authenticated:
            return redirect('/')
        userg = Group.objects.all()
        print(userg)
        if request.method == 'POST':
            full_name = request.POST['fullname']
            name = full_name.split(" ", 2)
            first_name = name[0]
            try:
                name[1].exists()
                last_name = name[1]
            except Exception as e:
                last_name = ''
            username = request.POST['username']
            email = request.POST['email']
            gender = request.POST['gender']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            user_type = request.POST['user_type']
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    sweetify.error(request, ' Username taken ')
                    return render(request, 'register_form.html', {'userg': userg})
                if User.objects.filter(email=email).exists():
                    sweetify.error(request, ' Email already registered... ')
                    return render(request, 'register_form.html', {'userg': userg})
                else:
                    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                    email=email, password=password1)
                    usergroup = Group.objects.get(name=user_type)
                    userextend = UserExtend.objects.create(userref=user, gender=gender)
                    if user_type == 'vendor':
                        userextend.acceptance = 'DENY'
                    usergroup.user_set.add(user)
                    user.save()
                    userextend.save()
                    sweetify.success(request, 'User creation Successful!')
                    return redirect('/users/login/')
            else:
                sweetify.error(request, 'password not matching ')
        return render(request, 'register_form.html', {'userg': userg})
    except Exception as e:
        print(e)



def logout(request):
    try:
        if request.user.is_authenticated:
            auth.logout(request)
        return redirect('/')
    except Exception as e:
        print(e)
