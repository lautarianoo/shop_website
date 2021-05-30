from django import forms
from .models import Order
from django.contrib.auth.models import User

class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'


    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        )

class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        passwrod = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь не существует')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(passwrod):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']
