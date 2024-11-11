from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.urls import reverse_lazy
import csv
from django.http import HttpResponse
from .models import Product
from .forms import ProductForm

class ProductList(ListView): 
    model = Product

class ProductDetail(DetailView): 
    model = Product

class ProductCreate(SuccessMessageMixin, CreateView): 
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    success_message = "Product successfully created!"

class ProductUpdate(SuccessMessageMixin, UpdateView): 
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    success_message = "Product successfully updated!"

class ProductDelete(SuccessMessageMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
    success_message = "Product successfully deleted!"


def export_books_csv(request):
    # Configuração para a resposta HTTP
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="livros.csv"'

    # Criando o escritor de CSV
    writer = csv.writer(response)
    writer.writerow(['Nome', 'Descrição', 'Preço'])

    # Obtendo todos os produtos
    products = Product.objects.all()

    # Escrevendo os dados dos produtos no arquivo CSV
    for product in products:
        writer.writerow([product.name, product.description, product.price])

    return response
