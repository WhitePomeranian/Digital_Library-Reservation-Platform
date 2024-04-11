from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    last_name = forms.CharField(
        label="姓氏",
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'})
    )

    first_name = forms.CharField(
        label="名字",
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'})
    )

    gender = forms.ChoiceField(
        label="性別",
        choices=[('M', '男'), ('F', '女')],
        widget=forms.RadioSelect(attrs={'style': 'margin-bottom: 10px;'})
    )
   

    birthday = forms.DateField(
        label="生日",
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;', 'placeholder':'YYYY-MM-DD'})
    )
    
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;', 'placeholder':'mail@example.com'})
    )

    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'})
    )

    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'})
    )

    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'})
    )
    
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'gender', 'birthday', 'email', 'username', 'password1', 'password2')


class SignInForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'})
    )