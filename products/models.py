from django.db import models
from django.contrib.auth.models import User
from racks.models import Rack, Shelf


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)
    rack = models.ForeignKey(
        Rack, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='products'
    )
    shelf = models.ForeignKey(
        Shelf, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='products'
    )
    quantity = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['brand', 'name']

    def __str__(self):
        return f"{self.brand} {self.name}"

    @property
    def location_display(self):
        if self.rack and self.shelf:
            return f"Rack {self.rack.name} / Shelf {self.shelf.code}"
        if self.rack:
            return f"Rack {self.rack.name}"
        return "No location assigned"

    @property
    def stock_status(self):
        if self.quantity == 0:
            return 'out'
        if self.quantity <= 3:
            return 'low'
        return 'ok'


class MovementLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    from_rack = models.CharField(max_length=10, blank=True)
    from_shelf = models.CharField(max_length=10, blank=True)
    to_rack = models.CharField(max_length=10, blank=True)
    to_shelf = models.CharField(max_length=10, blank=True)
    notes = models.TextField(blank=True)
    moved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='movements'
    )
    moved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-moved_at']

    def __str__(self):
        return f"{self.product} | {self.from_shelf} → {self.to_shelf} | {self.moved_at:%Y-%m-%d %H:%M}"

    @property
    def from_display(self):
        parts = []
        if self.from_rack:
            parts.append(f"Rack {self.from_rack}")
        if self.from_shelf:
            parts.append(f"Shelf {self.from_shelf}")
        return " → ".join(parts) if parts else "—"

    @property
    def to_display(self):
        parts = []
        if self.to_rack:
            parts.append(f"Rack {self.to_rack}")
        if self.to_shelf:
            parts.append(f"Shelf {self.to_shelf}")
        return " → ".join(parts) if parts else "—"
