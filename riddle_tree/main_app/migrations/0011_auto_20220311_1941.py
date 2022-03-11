# Generated by Django 3.2.12 on 2022-03-11 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_remove_question_final_question_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Описание акции')),
                ('max_users', models.PositiveIntegerField(verbose_name='Максимальное количество пользователей')),
            ],
        ),
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=8, null=True, verbose_name='Промокод')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.sale', verbose_name='Скидка')),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='promocode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.promocode', verbose_name='Промокод'),
        ),
    ]