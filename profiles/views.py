from django.shortcuts import render, HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import get_user_model, authenticate, login, logout

User = get_user_model()

# Create your views here.
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username_email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # Проверка существования логина или email
        try:
            the_user = User.objects.get(username=username_email)
        except User.DoesNotExist:
            the_user = User.objects.get(email=username_email)
        except:
            the_user = None

        if the_user is not None:
            user = authenticate(username=the_user.username,
                                password=password)
            try:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
            except AttributeError:
                # Пройди регистрацию
                return HttpResponseRedirect('/login/')
        else:
            # Пройди регистрацию
            return HttpResponseRedirect('/register/')

    context = {'form': form}
    return render(request, 'profiles/form.html', context)


def register_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        new_user = User.objects.create_user(username, email, password)
        try:
            if new_user.is_active:
                login(request, new_user)
                return HttpResponseRedirect('/')
        except AttributeError:
            # Пройди регистрацию
            return HttpResponseRedirect('/register/')

    context = {'form': form}
    return render(request, 'profiles/form.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')