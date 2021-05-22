from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View
from .models import Notebook, SmartPhone, Category, LatestProducts, Customer, Cart, CartProduct
from .mixins import CategoryDetailMixin, CartMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

class HomeBaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_category_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_mainpage('notebook', 'smartphone')
        return render(request, 'mainapp/base.html', {'categories': categories, 'products': products, 'cart': self.cart})


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': SmartPhone,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'mainapp/product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'mainapp/category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context

class AddtoCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        if created:
            self.cart.products.add(cart_product)
        self.cart.save()
        messages.add_message(request, messages.INFO, 'Товар успешно добавлен')
        return HttpResponseRedirect('/cart/')

class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        self.cart.save()
        messages.add_message(request, messages.INFO, 'Товар успешно удален')
        return HttpResponseRedirect('/cart/')

class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_category_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories,
        }

        return render(request, 'mainapp/cart.html', context)

class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        cart_product.quality = int(request.POST.get('qty'))
        cart_product.save()
        self.cart.save()
        messages.add_message(request, messages.INFO, 'Количество изменено')
        return HttpResponseRedirect('/cart/')
