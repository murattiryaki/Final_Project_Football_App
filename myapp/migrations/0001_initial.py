# Generated by Django 2.1.15 on 2024-06-18 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='fixture',
            name='stadium',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Stadium'),
        ),
        migrations.AddField(
            model_name='fixture',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Team'),
        ),
    ]
