from django.db import models


class Rack(models.Model):
    name = models.CharField(max_length=10, unique=True, help_text="e.g. A, B, C")
    category = models.CharField(max_length=100, blank=True, help_text="e.g. Lipsticks, Foundations")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Rack {self.name}"

    @property
    def shelf_count(self):
        return self.shelves.count()

    @property
    def product_count(self):
        return self.products.count()


class Shelf(models.Model):
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name='shelves')
    code = models.CharField(max_length=10, help_text="e.g. A1, A2")
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['code']
        unique_together = ['rack', 'code']

    def __str__(self):
        return self.code

    @property
    def product_count(self):
        return self.products.count()
