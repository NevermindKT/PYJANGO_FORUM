from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    username = forms.CharField(max_length=150, required=True, label="Никнейм")
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            Profile.objects.filter(user=user).update(
                date_of_birth=self.cleaned_data["date_of_birth"]
            )
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            raise forms.ValidationError("Неверный никнейм или пароль")

        cleaned_data["user"] = user
        return cleaned_data