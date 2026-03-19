from django.db import models


class Wall(models.Model):
    name = models.CharField(max_length=10, unique=True, help_text="e.g. A, B, C")
    category = models.CharField(max_length=100, blank=True, help_text="e.g. Lipsticks, Foundations")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Wall {self.name}"

    @property
    def rack_count(self):
        return self.racks.count()

    @property
    def product_count(self):
        return self.products.count()


class Rack(models.Model):
    wall = models.ForeignKey(Wall, on_delete=models.CASCADE, related_name='racks')
    code = models.CharField(max_length=10, help_text="e.g. A1, A2")
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['code']
        unique_together = ['wall', 'code']

    def __str__(self):
        return self.code

    @property
    def product_count(self):
        return self.products.count()
