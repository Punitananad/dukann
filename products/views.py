from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, MovementLog
from .forms import ProductForm, MoveProductForm, QuickQuantityForm
from .search_engine import smart_search, fallback_fuzzy
from racks.models import Wall, Rack


@login_required
def dashboard(request):
    total_products = Product.objects.count()
    total_walls = Wall.objects.count()
    total_racks = Rack.objects.count()
    low_stock = Product.objects.filter(quantity__lte=3, quantity__gt=0).count()
    out_of_stock = Product.objects.filter(quantity=0).count()
    recent_movements = MovementLog.objects.select_related('product').order_by('-moved_at')[:8]
    walls = Wall.objects.prefetch_related('racks', 'products').all()

    return render(request, 'dashboard.html', {
        'total_products': total_products,
        'total_walls': total_walls,
        'total_racks': total_racks,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'recent_movements': recent_movements,
        'walls': walls,
    })


@login_required
def search(request):
    q = request.GET.get('q', '').strip()
    products = []
    if q:
        products_qs = Product.objects.select_related('wall', 'rack')
        products = smart_search(products_qs, q)
        if not products:
            products = fallback_fuzzy(products_qs, q)
    return render(request, 'products/search.html', {
        'products': products,
        'q': q,
        'all_walls': Wall.objects.prefetch_related('racks').all(),
    })


@login_required
def search_api(request):
    """AJAX endpoint for live search suggestions."""
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'results': []})

    products_qs = Product.objects.select_related('wall', 'rack').only(
        'id', 'name', 'brand', 'category', 'subcategory',
        'tags', 'search_keywords', 'quantity',
        'wall__name', 'rack__code',
    )

    matched = smart_search(products_qs, q)
    if not matched:
        matched = fallback_fuzzy(products_qs, q)

    results = [
        {
            'id': p.pk,
            'name': p.name,
            'category': p.category,
            'rack': p.wall.name if p.wall else '',
            'shelf': p.rack.code if p.rack else '',
            'url': f'/products/{p.pk}/',
        }
        for p in matched
    ]

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
    wall_id = request.POST.get('new_wall') or (product.wall.pk if product.wall else None)
    form = MoveProductForm(request.POST or None, wall_id=wall_id)

    if request.method == 'POST' and form.is_valid():
        new_wall = form.cleaned_data['new_wall']
        new_rack = form.cleaned_data.get('new_rack')
        notes = form.cleaned_data.get('notes', '')

        MovementLog.objects.create(
            product=product,
            from_rack=product.wall.name if product.wall else '',
            from_shelf=product.rack.code if product.rack else '',
            to_rack=new_wall.name,
            to_shelf=new_rack.code if new_rack else '',
            notes=notes,
            moved_by=request.user,
        )

        product.wall = new_wall
        product.rack = new_rack
        product.save()

        messages.success(
            request,
            f'"{product}" moved to Wall {new_wall.name}'
            + (f' → Rack {new_rack.code}' if new_rack else '')
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
def quick_assign(request, pk):
    """AJAX: assign/change wall+rack for a product without a full page reload."""
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'POST required'}, status=405)

    product = get_object_or_404(Product, pk=pk)
    wall_id = request.POST.get('wall') or None
    rack_id = request.POST.get('rack') or None

    old_wall = product.wall.name if product.wall else ''
    old_rack = product.rack.code if product.rack else ''

    new_wall = get_object_or_404(Wall, pk=wall_id) if wall_id else None
    new_rack = get_object_or_404(Rack, pk=rack_id) if rack_id else None

    MovementLog.objects.create(
        product=product,
        from_rack=old_wall,
        from_shelf=old_rack,
        to_rack=new_wall.name if new_wall else '',
        to_shelf=new_rack.code if new_rack else '',
        notes=request.POST.get('notes', ''),
        moved_by=request.user,
    )

    product.wall = new_wall
    product.rack = new_rack
    product.save(update_fields=['wall', 'rack', 'updated_at'])

    return JsonResponse({
        'ok': True,
        'wall': new_wall.name if new_wall else '',
        'rack': new_rack.code if new_rack else '',
        'location_display': product.location_display,
    })


@login_required
def movement_history(request):
    movements = MovementLog.objects.select_related('product', 'moved_by').all()
    q = request.GET.get('q', '').strip()
    if q:
        movements = movements.filter(
            Q(product__name__icontains=q) | Q(product__brand__icontains=q)
        )
    return render(request, 'products/history.html', {'movements': movements, 'q': q})
