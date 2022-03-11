import stripe
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import DetailView, View
from .models import Category, Product, Customer, Cart, CartProduct, Order
from .mixins import CartMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from .forms import *
from .utils import recalc_cart
from django.db import transaction
from django.contrib.auth import authenticate, login

class HomeBaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        return render(request, 'mainapp/base.html', {'categories': categories, 'products': products, 'cart': self.cart})


class ProductDetailView(CartMixin, DetailView):

    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'mainapp/product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs.get('slug'))
        products = Product.objects.filter(category=category)
        return render(request, 'mainapp/category_detail.html', {'products': products, 'category': category})

class AddtoCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Товар успешно добавлен')
        return HttpResponseRedirect('/cart/')

class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Товар успешно удален')
        return HttpResponseRedirect('/cart/')

class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories,
        }

        return render(request, 'mainapp/cart.html', context)

class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product = product
        )
        cart_product.quality = int(request.POST.get('qty'))
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Количество изменено')
        return HttpResponseRedirect('/cart/')

class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        stripe.api_key = "sk_test_51IvmpHFwUowpEFtOjp3PDwRp4G8JG6y0HGQBaCQGPfFb81J8R9PuqFHyIXk05MWiT1qcZTbEmhS0Go0Na3hfvbRT003Glrvi7M"

        intent = stripe.PaymentIntent.create(
            amount=int(self.cart.total_price * 100),
            currency='rub',
            # Verify your integration in this guide by including this parameter
            metadata={'integration_check': 'accept_a_payment'},
        )
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form,
            'client_secret': intent.client_secret,
        }

        return render(request, 'mainapp/checkout.html', context)

class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Заказ принят. Менеджер свяжется с вами для подтверждения заказа')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')

class PayedOnlineOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        new_order = Order()
        new_order.customer = customer
        new_order.first_name = customer.user.first_name
        new_order.last_name = customer.user.last_name
        new_order.phone = customer.phone
        new_order.address = customer.address
        new_order.buying_type = Order.BUYING_TYPE_SELF
        new_order.save()
        self.cart.in_order = True
        self.cart.save()
        new_order.cart = self.cart
        new_order.status = Order.STATUS_PAYED
        new_order.save()
        customer.orders.add(new_order)
        return JsonResponse({'status': 'payed'})

class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories, 'cart': self.cart}

        return render(request, 'mainapp/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'mainapp/login.html', {'form': form, 'cart': self.cart})

class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories, 'cart': self.cart}

        return render(request, 'mainapp/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(user=new_user,
                                    phone=form.cleaned_data['phone'],
                                    address=form.cleaned_data['address'])
            return HttpResponseRedirect('/login/')
        return render(request, 'mainapp/register.html', {'form': form, 'cart': self.cart})

class ProfileView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        categories = Category.objects.all()
        return render(request, 'mainapp/profile.html', {'orders': orders, 'cart': self.cart, 'categories': categories})

class SearchingView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        filters = {
            'title__icontains': request.GET.get('q'),
            'sale': request.GET.get('sale')
        }
        if 'sale' in filters.keys() and filters.get('sale') == 'on':
            filters['sale'] = True
        else:
            filters.pop('sale')
        products = Product.objects.filter(**filters)
        return render(request, 'mainapp/base.html', {'products': products})
