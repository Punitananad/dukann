from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Rack, Shelf
from .forms import RackForm, ShelfForm, BulkShelfForm


@login_required
def rack_list(request):
    racks = Rack.objects.prefetch_related('shelves').all()
    return render(request, 'racks/rack_list.html', {'racks': racks})


@login_required
def rack_add(request):
    form = RackForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        rack = form.save(commit=False)
        rack.name = rack.name.upper()
        rack.save()
        messages.success(request, f'Rack {rack.name} created successfully.')
        return redirect('rack_list')
    return render(request, 'racks/rack_form.html', {'form': form, 'title': 'Add Rack'})


@login_required
def rack_edit(request, pk):
    rack = get_object_or_404(Rack, pk=pk)
    form = RackForm(request.POST or None, instance=rack)
    if request.method == 'POST' and form.is_valid():
        rack = form.save(commit=False)
        rack.name = rack.name.upper()
        rack.save()
        messages.success(request, f'Rack {rack.name} updated.')
        return redirect('rack_list')
    return render(request, 'racks/rack_form.html', {'form': form, 'title': f'Edit Rack {rack.name}', 'rack': rack})


@login_required
def rack_delete(request, pk):
    rack = get_object_or_404(Rack, pk=pk)
    if request.method == 'POST':
        name = rack.name
        rack.delete()
        messages.success(request, f'Rack {name} deleted.')
        return redirect('rack_list')
    return render(request, 'racks/rack_confirm_delete.html', {'rack': rack})


@login_required
def shelf_list(request):
    rack_id = request.GET.get('rack')
    racks = Rack.objects.all()
    shelves = Shelf.objects.select_related('rack').all()
    selected_rack = None
    if rack_id:
        selected_rack = get_object_or_404(Rack, pk=rack_id)
        shelves = shelves.filter(rack=selected_rack)
    return render(request, 'racks/shelf_list.html', {
        'shelves': shelves,
        'racks': racks,
        'selected_rack': selected_rack,
    })


@login_required
def shelf_add(request):
    rack_id = request.GET.get('rack')
    initial = {}
    if rack_id:
        initial['rack'] = rack_id
    form = ShelfForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        shelf = form.save(commit=False)
        shelf.code = shelf.code.upper()
        shelf.save()
        messages.success(request, f'Shelf {shelf.code} added to Rack {shelf.rack.name}.')
        return redirect('shelf_list')
    return render(request, 'racks/shelf_form.html', {'form': form, 'title': 'Add Shelf'})


@login_required
def shelf_bulk_add(request):
    form = BulkShelfForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        rack = form.cleaned_data['rack']
        count = form.cleaned_data['count']
        created = 0
        for i in range(1, count + 1):
            code = f"{rack.name}{i}"
            shelf, is_new = Shelf.objects.get_or_create(rack=rack, code=code)
            if is_new:
                created += 1
        messages.success(request, f'Created {created} shelf/shelves for Rack {rack.name}.')
        return redirect('shelf_list')
    return render(request, 'racks/shelf_bulk_form.html', {'form': form, 'title': 'Bulk Add Shelves'})


@login_required
def shelf_edit(request, pk):
    shelf = get_object_or_404(Shelf, pk=pk)
    form = ShelfForm(request.POST or None, instance=shelf)
    if request.method == 'POST' and form.is_valid():
        shelf = form.save(commit=False)
        shelf.code = shelf.code.upper()
        shelf.save()
        messages.success(request, f'Shelf {shelf.code} updated.')
        return redirect('shelf_list')
    return render(request, 'racks/shelf_form.html', {'form': form, 'title': f'Edit Shelf {shelf.code}', 'shelf': shelf})


@login_required
def shelf_delete(request, pk):
    shelf = get_object_or_404(Shelf, pk=pk)
    if request.method == 'POST':
        code = shelf.code
        shelf.delete()
        messages.success(request, f'Shelf {code} deleted.')
        return redirect('shelf_list')
    return render(request, 'racks/shelf_confirm_delete.html', {'shelf': shelf})


@login_required
def label_generator(request):
    rack_id = request.GET.get('rack')
    racks = Rack.objects.prefetch_related('shelves').all()
    selected_racks = racks
    if rack_id:
        selected_racks = racks.filter(pk=rack_id)
    return render(request, 'racks/labels.html', {
        'racks': racks,
        'selected_racks': selected_racks,
        'rack_id': rack_id,
    })


def shelves_by_rack(request, rack_pk):
    """AJAX endpoint: returns shelves for a given rack as JSON."""
    shelves = Shelf.objects.filter(rack_id=rack_pk).values('id', 'code')
    return JsonResponse({'shelves': list(shelves)})
