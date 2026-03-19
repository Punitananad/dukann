import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    1. Rename product.rack (FK→Wall) → product.wall
    2. Rename product.shelf (FK→Rack) → product.rack
    3. Explicit AlterField to fix FK lazy-reference after case-sensitive RenameModel bug
    4. Make brand optional (blank=True)
    5. Sort by name instead of brand+name
    """

    dependencies = [
        ('products', '0002_alter_product_category'),
        ('racks', '0002_wall_and_rack'),
    ]

    operations = [
        # Rename rack→wall  (renames column rack_id → wall_id in products_product)
        migrations.RenameField('Product', 'rack', 'wall'),

        # Rename shelf→rack  (renames column shelf_id → rack_id in products_product)
        migrations.RenameField('Product', 'shelf', 'rack'),

        # Explicitly reset FK targets — Django's RenameModel uses case-sensitive replace
        # so 'racks.shelf' never becomes 'racks.rack' without this explicit fix.
        migrations.AlterField(
            model_name='product',
            name='wall',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='products', to='racks.wall',
            ),
        ),
        migrations.AlterField(
            model_name='product',
            name='rack',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='products', to='racks.rack',
            ),
        ),

        # Make brand optional
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, default='', max_length=100),
        ),

        # Update ordering to sort by name only
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name']},
        ),
    ]
