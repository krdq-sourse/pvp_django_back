# Generated by Django 4.1.4 on 2023-03-14 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0008_alter_shophistory_options_alter_shophistory_steamid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shophistory',
            name='item',
            field=models.ForeignKey(default='Add Donate', on_delete=django.db.models.deletion.CASCADE, to='back.product', verbose_name='Предмет'),
        ),
    ]
