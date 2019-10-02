from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth, Group
from .models import UserExtend
from homepage.views import shopplus


# Create your views here.

def login(request):
    return render(request, 'login.html')



def register_verify(request):
    if request.method == 'POST':
        full_name = request.POST['fullname']
        name = full_name.split()
        first_name = name[0]
        last_name = name[1]
        username = request.POST['username']
        email = request.POST['email']
        gender = request.POST['gender']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user_type = request.POST['user_type']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print('username taken')
            elif User.objects.filter(email=email).exists():
                print('email taken')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password1)
                usergroup = Group.objects.get(name=user_type)
                userextend = UserExtend.objects.create(userref=user, gender=gender)
                usergroup.user_set.add(user)
                user.save()
                userextend.save()

                print('user created')
            return redirect('/')
        else:
            print('password wrng')

    else:
        userg = Group.objects.all()
        print(userg)
        return render(request, 'register_form.html', {'userg': userg})


# verify login
def signin_verify(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            usergroup = Group.objects.get(name='vendor')
            if request.user.groups.filter(name=usergroup).exists():
                return shopplus(request)
            else:
                return redirect('/')
        else:
            print('invalid there')
            return redirect('/users/login')
    print('invalid here')
    return redirect('/users/login')



def logout(request):
    auth.logout(request)
    return redirect('/')