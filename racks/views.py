from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Wall, Rack
from .forms import WallForm, WallWithRacksForm, RackForm, BulkRackForm


@login_required
def wall_list(request):
    walls = Wall.objects.prefetch_related('racks').all()
    return render(request, 'racks/wall_manager.html', {'walls': walls})


@login_required
def wall_add(request):
    form = WallWithRacksForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        wall = form.save()
        rack_count = form.cleaned_data.get('rack_count') or 0
        created = 0
        for i in range(1, rack_count + 1):
            code = f"{wall.name}{i}"
            Rack.objects.get_or_create(wall=wall, code=code)
            created += 1
        if created:
            messages.success(request, f'Wall {wall.name} created with {created} rack(s).')
        else:
            messages.success(request, f'Wall {wall.name} created. Add racks using the + button.')
        return redirect('wall_list')
    return render(request, 'racks/wall_form.html', {'form': form, 'title': 'Add Wall'})


@login_required
def wall_edit(request, pk):
    wall = get_object_or_404(Wall, pk=pk)
    form = WallForm(request.POST or None, instance=wall)
    if request.method == 'POST' and form.is_valid():
        wall = form.save()
        messages.success(request, f'Wall {wall.name} updated.')
        return redirect('wall_list')
    return render(request, 'racks/wall_edit_form.html', {'form': form, 'title': f'Edit Wall {wall.name}', 'wall': wall})


@login_required
def wall_delete(request, pk):
    wall = get_object_or_404(Wall, pk=pk)
    if request.method == 'POST':
        name = wall.name
        wall.delete()
        messages.success(request, f'Wall {name} deleted.')
        return redirect('wall_list')
    return render(request, 'racks/wall_confirm_delete.html', {'wall': wall})


@login_required
def rack_add(request):
    wall_id = request.GET.get('wall')
    initial = {}
    if wall_id:
        initial['wall'] = wall_id
    form = RackForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        rack = form.save()
        messages.success(request, f'Rack {rack.code} added to Wall {rack.wall.name}.')
        return redirect('wall_list')
    return render(request, 'racks/rack_form.html', {'form': form, 'title': 'Add Rack'})


@login_required
def rack_edit(request, pk):
    rack = get_object_or_404(Rack, pk=pk)
    form = RackForm(request.POST or None, instance=rack)
    if request.method == 'POST' and form.is_valid():
        rack = form.save()
        messages.success(request, f'Rack {rack.code} updated.')
        return redirect('wall_list')
    return render(request, 'racks/rack_form.html', {'form': form, 'title': f'Edit Rack {rack.code}', 'rack': rack})


@login_required
def rack_delete(request, pk):
    rack = get_object_or_404(Rack, pk=pk)
    if request.method == 'POST':
        code = rack.code
        wall_name = rack.wall.name
        rack.delete()
        messages.success(request, f'Rack {code} removed from Wall {wall_name}.')
        return redirect('wall_list')
    return render(request, 'racks/rack_confirm_delete.html', {'rack': rack})


@login_required
def rack_bulk_add(request):
    wall_id = request.GET.get('wall')
    initial = {}
    if wall_id:
        initial['wall'] = wall_id
    form = BulkRackForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        wall = form.cleaned_data['wall']
        count = form.cleaned_data['count']
        created = 0
        existing = set(wall.racks.values_list('code', flat=True))
        for i in range(1, count + 1):
            code = f"{wall.name}{i}"
            if code not in existing:
                Rack.objects.create(wall=wall, code=code)
                created += 1
        messages.success(request, f'Created {created} rack(s) for Wall {wall.name}.')
        return redirect('wall_list')
    return render(request, 'racks/rack_bulk_form.html', {'form': form, 'title': 'Bulk Add Racks'})


@login_required
def label_generator(request):
    wall_id = request.GET.get('wall')
    walls = Wall.objects.prefetch_related('racks').all()
    selected_walls = walls
    if wall_id:
        selected_walls = walls.filter(pk=wall_id)
    return render(request, 'racks/labels.html', {
        'walls': walls,
        'selected_walls': selected_walls,
        'wall_id': wall_id,
    })


def racks_by_wall(request, wall_pk):
    """AJAX endpoint: returns racks for a given wall as JSON."""
    racks = Rack.objects.filter(wall_id=wall_pk).values('id', 'code')
    return JsonResponse({'shelves': list(racks)})
