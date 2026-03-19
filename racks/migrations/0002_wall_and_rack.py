from django.db import migrations


class Migration(migrations.Migration):
    """
    Rename Rack→Wall, Shelf→Rack at both DB and state level.
    This renames tables (racks_rack→racks_wall, racks_shelf→racks_rack)
    and the FK column (rack_id→wall_id in the new racks_rack table).
    All existing data is preserved.
    """

    dependencies = [
        ('racks', '0001_initial'),
    ]

    operations = [
        # Step 1: Rack model → Wall  (renames table racks_rack → racks_wall)
        migrations.RenameModel('Rack', 'Wall'),

        # Step 2: Shelf model → Rack  (renames table racks_shelf → racks_rack)
        migrations.RenameModel('Shelf', 'Rack'),

        # Step 3: Rack.rack FK field → Rack.wall
        #         (renames column rack_id → wall_id in racks_rack table)
        migrations.RenameField('Rack', 'rack', 'wall'),

        # Step 4: Fix unique_together to use the new field name
        migrations.AlterUniqueTogether('Rack', unique_together={('wall', 'code')}),
    ]
