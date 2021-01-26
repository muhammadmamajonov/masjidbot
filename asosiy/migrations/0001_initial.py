# Generated by Django 3.1.4 on 2021-01-16 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HaftaKunlari',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomi', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='NamozVaqti',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sana', models.DateField()),
                ('tong', models.TimeField()),
                ('quyosh', models.TimeField()),
                ('peshin', models.TimeField()),
                ('asr', models.TimeField()),
                ('shom', models.TimeField()),
                ('xufton', models.TimeField()),
                ('hafta_kuni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asosiy.haftakunlari')),
            ],
        ),
    ]
