import http
from django.views import generic
from django.shortcuts import render
from product.models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice

from product.models import Variant, Product, ProductVariantPrice
from product.filter import ProductFilter

from django_filters.views import FilterView

from django.http import Http404
from django.http import JsonResponse
import json


class ProductList(FilterView):
    template_name = 'products/list.html'
    model = Product

    context_object_name = 'product_list'
    ordering = ["created_at"]

    filterset_class = ProductFilter

    paginate_by = 3
    paginate_orphans = 1

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)

        context['product'] = True
        context['pvp'] = ProductVariantPrice.objects.all()

        return context

    def paginate_queryset(self, queryset, page_size):
        try:
            return super(ProductList, self).paginate_queryset(queryset, page_size)
        except Http404:
            self.kwargs['page'] = 1
            return super(ProductList, self).paginate_queryset(queryset, page_size)


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        print(data)

        # # SAVE PRODUCT
        title = data['title']
        sku = data['sku']
        description = data['description']

        product = Product.objects.create(
            title=title,
            sku=sku,
            description=description
        )
        product.save()

        # # SAVE IMAGE

        product_image = data['product_image']
        try:
            product_image = product_image[0]
        except:
            product_image = ""

        productImage = ProductImage.objects.create(
            product=product,
            file_path=product_image
        )
        productImage.save()

        # # SAVE ProductVariant

        variant = Variant.objects.all()
        print('VARIENTS', variant[0])

        try:

            size = data['product_variant'][0]['tags'][0]
            color = data['product_variant'][1]['tags'][0]
            style = data['product_variant'][2]['tags'][0]

        except:
            size = ''
            color = ''
            style = ''

        pv1 = ProductVariant.objects.create(
            variant_title=size,
            variant=variant[0],
            product=product
        )
        pv1.save()

        pv2 = ProductVariant.objects.create(
            variant_title=color,
            variant=variant[1],
            product=product
        )
        pv2.save()

        pv3 = ProductVariant.objects.create(
            variant_title=style,
            variant=variant[2],
            product=product
        )
        pv3.save()

        # # SAVE ProductVariantPrice

        try:
            price = data['product_variant_prices'][0]['price']
            stock = data['product_variant_prices'][0]['stock']
        except:
            price = 0
            stock = 0
        pvp = ProductVariantPrice.objects.create(
            product_variant_one=pv1,
            product_variant_two=pv2,
            product_variant_three=pv3,
            price=price,
            stock=stock,
            product=product)
        pvp.save()

        return JsonResponse({"status": 'Success'})

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
