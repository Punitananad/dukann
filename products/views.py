from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Sum
from .models import Product, MovementLog
from .forms import ProductForm, MoveProductForm, QuickQuantityForm
from racks.models import Rack, Shelf


@login_required
def dashboard(request):
    total_products = Product.objects.count()
    total_racks = Rack.objects.count()
    total_shelves = Shelf.objects.count()
    low_stock = Product.objects.filter(quantity__lte=3, quantity__gt=0).count()
    out_of_stock = Product.objects.filter(quantity=0).count()
    recent_movements = MovementLog.objects.select_related('product').order_by('-moved_at')[:8]
    racks = Rack.objects.prefetch_related('shelves', 'products').all()

    return render(request, 'dashboard.html', {
        'total_products': total_products,
        'total_racks': total_racks,
        'total_shelves': total_shelves,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'recent_movements': recent_movements,
        'racks': racks,
    })


@login_required
def search(request):
    q = request.GET.get('q', '').strip()
    products = []
    if q:
        products = Product.objects.select_related('rack', 'shelf').filter(
            Q(name__icontains=q) |
            Q(brand__icontains=q) |
            Q(category__icontains=q)
        )
    return render(request, 'products/search.html', {'products': products, 'q': q})


@login_required
def search_api(request):
    """AJAX endpoint for live search suggestions."""
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'results': []})

    products = Product.objects.select_related('rack', 'shelf').filter(
        Q(name__icontains=q) |
        Q(brand__icontains=q) |
        Q(category__icontains=q)
    )[:12]

    results = []
    for p in products:
        results.append({
            'id': p.pk,
            'name': p.name,
            'brand': p.brand,
            'category': p.category,
            'rack': p.rack.name if p.rack else '',
            'shelf': p.shelf.code if p.shelf else '',
            'quantity': p.quantity,
            'stock_status': p.stock_status,
            'url': f'/products/{p.pk}/',
        })

    return JsonResponse({'results': results})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    movements = product.movements.all()[:20]
    qty_form = QuickQuantityForm(initial={'quantity': product.quantity})
    return render(request, 'products/detail.html', {
        'product': product,
        'movements': movements,
        'qty_form': qty_form,
    })


@login_required
def product_add(request):
    form = ProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        product = form.save()
        messages.success(request, f'Product "{product}" added successfully.')
        return redirect('product_detail', pk=product.pk)
    return render(request, 'products/form.html', {'form': form, 'title': 'Add Product'})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Product "{product}" updated.')
        return redirect('product_detail', pk=product.pk)
    return render(request, 'products/form.html', {
        'form': form,
        'title': f'Edit: {product}',
        'product': product,
    })


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = str(product)
        product.delete()
        messages.success(request, f'"{name}" deleted.')
        return redirect('search')
    return render(request, 'products/confirm_delete.html', {'product': product})


@login_required
def product_move(request, pk):
    product = get_object_or_404(Product, pk=pk)
    rack_id = request.POST.get('new_rack') or (product.rack.pk if product.rack else None)
    form = MoveProductForm(request.POST or None, rack_id=rack_id)

    if request.method == 'POST' and form.is_valid():
        new_rack = form.cleaned_data['new_rack']
        new_shelf = form.cleaned_data.get('new_shelf')
        notes = form.cleaned_data.get('notes', '')

        # Log the movement
        MovementLog.objects.create(
            product=product,
            from_rack=product.rack.name if product.rack else '',
            from_shelf=product.shelf.code if product.shelf else '',
            to_rack=new_rack.name,
            to_shelf=new_shelf.code if new_shelf else '',
            notes=notes,
            moved_by=request.user,
        )

        product.rack = new_rack
        product.shelf = new_shelf
        product.save()

        messages.success(
            request,
            f'"{product}" moved to Rack {new_rack.name}'
            + (f' → Shelf {new_shelf.code}' if new_shelf else '')
        )
        return redirect('product_detail', pk=product.pk)

    return render(request, 'products/move.html', {'product': product, 'form': form})


@login_required
def update_quantity(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = QuickQuantityForm(request.POST)
        if form.is_valid():
            product.quantity = form.cleaned_data['quantity']
            product.save()
            messages.success(request, f'Quantity updated to {product.quantity}.')
    return redirect('product_detail', pk=product.pk)


@login_required
def movement_history(request):
    movements = MovementLog.objects.select_related('product', 'moved_by').all()
    q = request.GET.get('q', '').strip()
    if q:
        movements = movements.filter(
            Q(product__name__icontains=q) | Q(product__brand__icontains=q)
        )
    return render(request, 'products/history.html', {'movements': movements, 'q': q})
