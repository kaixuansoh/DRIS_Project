# 24068022 Soh Kai Xuan
# Generated manually on 2025-06-24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shelters', '0002_create_sample_shelters'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shelter',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='shelter',
            name='longitude',
        ),
    ]
