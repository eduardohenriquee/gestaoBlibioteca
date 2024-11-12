from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView 
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
import csv
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
    success_message = "Livro adicionado com sucesso!"

class ProductUpdate(SuccessMessageMixin, UpdateView): 
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    success_message = "Livro atualizado com sucesso!"

class ProductDelete(SuccessMessageMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
    success_message = "Livro deletado com sucesso!"

def export_books_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="livros.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'Descrição', 'Preço', 'Status'])

    status = request.GET.get('status')

    if status:
        products = Product.objects.filter(status=status)
    else:
        products = Product.objects.all()

    for product in products:
        writer.writerow([product.name, product.description, product.price, product.status])

    return response



def reserve_book(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.status == 'disponivel':
        product.status = 'emprestado'
        product.save()
        messages.success(request, 'Livro reservado com sucesso!')
    else:
        messages.error(request, 'Este livro não está disponível para reserva.')
    return redirect('product_list')

@permission_required('products.add_product')
def adicionar_produto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        
        Product.objects.create(
            name=nome,
            description=descricao,
            price=preco
        )
        return redirect('product_list')
    
    return render(request, 'products/adicionar.html')

@permission_required('products.delete_product')
def deletar_produto(request, produto_id):
    produto = get_object_or_404(Product, id=produto_id)
    
    if request.method == 'POST':
        produto.delete()
        return redirect('product_list')
    
    return render(request, 'products/confirmar_delete.html', {'produto': produto})

@login_required
def listar_produtos(request):
    produtos = Product.objects.all()
    context = {
        'produtos': produtos,
        'pode_adicionar': request.user.has_perm('products.add_product'),
        'pode_deletar': request.user.has_perm('products.delete_product')
    }
    return render(request, 'products/listar.html', context) 