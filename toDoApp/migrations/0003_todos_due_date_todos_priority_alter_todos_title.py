# Generated by Django 5.1.4 on 2025-07-20 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toDoApp', '0002_todos_created_at_todos_description_todos_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='todos',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='todos',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low', max_length=10),
        ),
        migrations.AlterField(
            model_name='todos',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
