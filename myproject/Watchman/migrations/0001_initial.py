# Generated by Django 3.2.7 on 2022-01-05 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Chairman', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_no', models.CharField(max_length=20)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('v_detail', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Watchman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('contact', models.CharField(default='9999999999', max_length=10)),
                ('id_pic', models.FileField(blank=True, null=True, upload_to='media/document')),
                ('profile_pic', models.FileField(default='media/default.png', upload_to='media/images')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Chairman.user')),
            ],
        ),
    ]
