# Generated by Django 5.1.1 on 2024-09-21 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_role',
            field=models.CharField(choices=[('coach', 'Coach'), ('agent', 'Agent')], default='Coach', max_length=10),
        ),
    ]
