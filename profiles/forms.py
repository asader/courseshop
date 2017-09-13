from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(label='Username или Email')
    password = forms.CharField(widget=forms.PasswordInput())
    # Проверка наличия польз
    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(Q(username=username) | Q(email=username)).exists():
            raise forms.ValidationError("Пользователя %s не существует" %(username))
        return username




class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_repeat = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь %s уже зарегистрирован" %(username))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь %s уже зарегистрирован" %(email))
        return email

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password != password_repeat:
            self._errors["password"] = self.error_class(["Пароль1 не совпадают"])
            self._errors["password_repeat"] = self.error_class(["Пароль2 не совпадают"])
            raise forms.ValidationError("Пароли не совпадают")
            del cleaned_data['password']
            del cleaned_data['password_repeat']
        return cleaned_data