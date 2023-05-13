from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from user.models import *


# noinspection SpellCheckingInspection
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логин'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Фамилия'}))
    patronymic = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Отчество'}))
    group = forms.ModelChoiceField(queryset=Groups.objects.all(), empty_label='Выбирите группу', required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Подтвердите пароль'}))

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)

        if commit:
            user.save()
            group = self.cleaned_data['group']
            if group:
                group_teacher = Students(id_user=user, id_group=group)
                group_teacher.save()

        return user

    class Meta:
        model = CustomUser
        fields = ('username', 'last_name', 'first_name', 'patronymic', 'group', 'email', 'password1', 'password2')


class AuthorizationUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
