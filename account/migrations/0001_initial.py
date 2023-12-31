# Generated by Django 4.2.5 on 2023-10-11 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机号')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
            ],
        ),
    ]
