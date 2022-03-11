from django import forms
from .models import Order
from customers.models import Customer

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
        self.fields['email'].label = 'email'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        email = self.cleaned_data['email']
        passwrod = self.cleaned_data['password']
        if not Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь не существует')
        user = Customer.objects.filter(email=email).first()
        if user:
            if not user.check_password(passwrod):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = Customer
        fields = ['email', 'password']

class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    email = forms.CharField(required=True, widget=forms.EmailInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Почта'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['first_name'].label = 'Ваше имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['address'].label = 'Адрес'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['net']:
            raise forms.ValidationError('Регистрация для данного домена не возможно')
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('Данная почто уже существует')
        return email

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не сопадают')
        return self.cleaned_data

    class Meta:
        model = Customer
        fields = ['password', 'confirm_password', 'first_name', 'last_name', 'address', 'phone','email', ]
