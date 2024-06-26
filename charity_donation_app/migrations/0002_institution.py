# Generated by Django 5.0.5 on 2024-05-08 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity_donation_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[(0, 'fundacja'), (1, 'organizacja pozarządowa'), (2, 'zbiórka lokalna')], default=0)),
                ('categories', models.ManyToManyField(to='charity_donation_app.category')),
            ],
        ),
    ]
